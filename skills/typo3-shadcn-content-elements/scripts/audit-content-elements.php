#!/usr/bin/env php
<?php

declare(strict_types=1);

use Symfony\Component\Yaml\Yaml;

$root = $argv[1] ?? getcwd();
$root = rtrim($root, DIRECTORY_SEPARATOR);
$autoload = $root . '/vendor/autoload.php';

if (!is_file($autoload)) {
    fwrite(STDERR, "Missing vendor/autoload.php in {$root}\n");
    exit(2);
}

require $autoload;

$elementsRoot = $root . '/ContentBlocks/ContentElements';
if (!is_dir($elementsRoot)) {
    fwrite(STDERR, "Missing ContentBlocks/ContentElements in {$root}\n");
    exit(2);
}

$systemFields = [
    'uid' => true,
    'pid' => true,
    'CType' => true,
    'colPos' => true,
    'sys_language_uid' => true,
    'relations' => true,
    'systemProperties' => true,
];

$summary = [
    'elements' => 0,
    'missingConfig' => 0,
    'missingFrontend' => 0,
    'missingPreview' => 0,
    'missingIcon' => 0,
    'missingLabels' => 0,
    'templatesWithUndeclaredTopFields' => 0,
    'templatesWithUnusedTopFields' => 0,
    'templatesWithCollectionIssues' => 0,
    'fieldsMissingDefaults' => 0,
];

$elements = [];

foreach (glob($elementsRoot . '/*', GLOB_ONLYDIR) ?: [] as $dir) {
    $name = basename($dir);
    $summary['elements']++;

    $configFile = $dir . '/config.yaml';
    $frontendFile = $dir . '/templates/frontend.html';
    $previewFile = $dir . '/templates/backend-preview.fluid.html';
    $iconFile = $dir . '/assets/icon.svg';
    $labelsFile = $dir . '/language/labels.xlf';

    $entry = [
        'name' => $name,
        'typeName' => null,
        'missing' => [],
        'declaredTopFields' => [],
        'usedTopFields' => [],
        'undeclaredTopFields' => [],
        'unusedTopFields' => [],
        'fieldsMissingDefaults' => [],
        'collectionIssues' => [],
    ];

    foreach ([
        'config' => $configFile,
        'frontend' => $frontendFile,
        'preview' => $previewFile,
        'icon' => $iconFile,
        'labels' => $labelsFile,
    ] as $key => $file) {
        if (!is_file($file)) {
            $entry['missing'][] = $key;
            $summary['missing' . ucfirst($key)] = ($summary['missing' . ucfirst($key)] ?? 0) + 1;
        }
    }

    if (!is_file($configFile) || !is_file($frontendFile)) {
        $elements[] = $entry;
        continue;
    }

    $config = Yaml::parseFile($configFile);
    $entry['typeName'] = $config['typeName'] ?? null;

    $topFields = [];
    $fieldTypes = [];
    $nestedFields = [];

    foreach (($config['fields'] ?? []) as $field) {
        if (!isset($field['identifier'])) {
            continue;
        }

        $identifier = (string)$field['identifier'];
        $topFields[$identifier] = $field;
        $fieldTypes[$identifier] = $field['type'] ?? (($field['useExistingField'] ?? false) ? 'Existing' : null);

        if (in_array($field['type'] ?? null, ['Select', 'Checkbox', 'Radio'], true) && !array_key_exists('default', $field)) {
            $entry['fieldsMissingDefaults'][] = $identifier;
        }

        foreach (($field['fields'] ?? []) as $child) {
            if (isset($child['identifier'])) {
                $nestedFields[$identifier][(string)$child['identifier']] = $child;
            }
        }
    }

    $template = file_get_contents($frontendFile) ?: '';
    $templateForFields = preg_replace('#<(script|style)\b[^>]*>.*?</\1>#is', '', $template) ?? $template;

    $usedTop = [];
    preg_match_all('/data\.([A-Za-z_][A-Za-z0-9_]*)/', $templateForFields, $matches);
    foreach ($matches[1] as $field) {
        $usedTop[$field] = true;
    }

    preg_match_all('/\{data\s*->\s*f:render\.text\(field:\s*[\'"]([A-Za-z_][A-Za-z0-9_]*)[\'"]/', $templateForFields, $matches);
    foreach ($matches[1] as $field) {
        $usedTop[$field] = true;
    }

    preg_match_all('/each="\{data\.([A-Za-z_][A-Za-z0-9_]*)\}"\s+as="([A-Za-z_][A-Za-z0-9_]*)"/', $templateForFields, $loops, PREG_SET_ORDER);
    foreach ($loops as $loop) {
        [, $field, $variable] = $loop;
        $usedTop[$field] = true;

        if (($fieldTypes[$field] ?? null) !== 'Collection') {
            if (($fieldTypes[$field] ?? null) !== 'File') {
                $entry['collectionIssues'][$field][] = 'looped field is not Collection or File';
            }
            continue;
        }

        $usedNested = [];
        preg_match_all('/' . preg_quote($variable, '/') . '\.([A-Za-z_][A-Za-z0-9_]*)/', $templateForFields, $nestedMatches);
        foreach ($nestedMatches[1] as $nestedField) {
            $usedNested[$nestedField] = true;
        }

        preg_match_all('/\{' . preg_quote($variable, '/') . '\s*->\s*f:render\.text\(field:\s*[\'"]([A-Za-z_][A-Za-z0-9_]*)[\'"]/', $templateForFields, $renderMatches);
        foreach ($renderMatches[1] as $nestedField) {
            $usedNested[$nestedField] = true;
        }

        $declaredNested = array_keys($nestedFields[$field] ?? []);
        $undeclaredNested = array_values(array_diff(array_keys($usedNested), $declaredNested));
        $unusedNested = array_values(array_diff($declaredNested, array_keys($usedNested)));

        if ($undeclaredNested !== []) {
            $entry['collectionIssues'][$field]['undeclaredNestedFields'] = $undeclaredNested;
        }
        if ($unusedNested !== []) {
            $entry['collectionIssues'][$field]['unusedNestedFields'] = $unusedNested;
        }
    }

    $declaredTop = array_keys($topFields);
    $entry['declaredTopFields'] = $declaredTop;
    $entry['usedTopFields'] = array_keys($usedTop);
    $entry['undeclaredTopFields'] = array_values(array_filter(
        array_diff(array_keys($usedTop), $declaredTop),
        static fn(string $field): bool => !isset($systemFields[$field])
    ));
    $entry['unusedTopFields'] = array_values(array_diff($declaredTop, array_keys($usedTop)));

    if ($entry['undeclaredTopFields'] !== []) {
        $summary['templatesWithUndeclaredTopFields']++;
    }
    if ($entry['unusedTopFields'] !== []) {
        $summary['templatesWithUnusedTopFields']++;
    }
    if ($entry['collectionIssues'] !== []) {
        $summary['templatesWithCollectionIssues']++;
    }
    if ($entry['fieldsMissingDefaults'] !== []) {
        $summary['fieldsMissingDefaults']++;
    }

    $elements[] = $entry;
}

ksort($summary);
usort($elements, static fn(array $a, array $b): int => $a['name'] <=> $b['name']);

echo json_encode([
    'root' => $root,
    'summary' => $summary,
    'elements' => $elements,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . PHP_EOL;
