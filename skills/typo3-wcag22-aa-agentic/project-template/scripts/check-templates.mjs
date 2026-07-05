#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { glob } from 'glob';
import { loadConfig } from '../tests/helpers/config.js';

const args = parseArgs(process.argv.slice(2));
const config = await loadConfig(args.config || '.a11y/a11y.config.yml');
const roots = config.typo3?.sitepackagePaths || [];
const findings = [];

const checks = [
  {
    id: 'fluid-img-missing-alt',
    severity: 'serious',
    files: ['**/*.{html,fluid}'],
    pattern: /<img\b(?!(?=[^>]*\balt\s*=))[^>]*>/gi,
    message: 'Image without alt attribute. Add meaningful alt text or alt="" for decorative images.'
  },
  {
    id: 'fluid-positive-tabindex',
    severity: 'serious',
    files: ['**/*.{html,fluid,js,ts}'],
    pattern: /tabindex\s*=\s*["']?[1-9][0-9]*/gi,
    message: 'Positive tabindex creates fragile keyboard order. Use DOM order or tabindex="0" only when unavoidable.'
  },
  {
    id: 'fluid-clickable-div-span',
    severity: 'warning',
    files: ['**/*.{html,fluid}'],
    pattern: /<(div|span)\b[^>]*(onclick|@click|data-action)[^>]*>/gi,
    message: 'Clickable div/span detected. Prefer button or link with keyboard support.'
  },
  {
    id: 'fluid-placeholder-only-input',
    severity: 'warning',
    files: ['**/*.{html,fluid}'],
    pattern: /<input\b(?=[^>]*\bplaceholder\s*=)(?![^>]*(\baria-label\s*=|\baria-labelledby\s*=|\bid\s*=))[^>]*>/gi,
    message: 'Input appears to rely on placeholder without clear programmatic label. Check label association.'
  },
  {
    id: 'scss-focus-outline-none',
    severity: 'serious',
    files: ['**/*.{css,scss,sass,less}'],
    pattern: /outline\s*:\s*(0|none)\s*;?/gi,
    message: 'Focus outline removed. Ensure a visible replacement focus style exists.'
  },
  {
    id: 'link-generic-text',
    severity: 'warning',
    files: ['**/*.{html,fluid}'],
    pattern: />\s*(hier klicken|mehr|weiter|read more|click here)\s*</gi,
    message: 'Generic link text. Make the link purpose understandable from link text or accessible name.'
  },
  {
    id: 'aria-hidden-focusable-risk',
    severity: 'warning',
    files: ['**/*.{html,fluid,js,ts}'],
    pattern: /aria-hidden\s*=\s*["']true["'][^>]*(href=|tabindex=|<button|role=["']button)/gi,
    message: 'Possible focusable content hidden from assistive technology. Review aria-hidden usage.'
  }
];

for (const root of roots) {
  try {
    const stat = await fs.stat(root);
    if (!stat.isDirectory()) continue;
  } catch {
    continue;
  }
  for (const check of checks) {
    for (const pattern of check.files) {
      const files = await glob(path.join(root, pattern), { nodir: true, ignore: ['**/node_modules/**', '**/vendor/**', '**/.Build/**'] });
      for (const file of files) {
        const text = await fs.readFile(file, 'utf8').catch(() => '');
        for (const match of text.matchAll(check.pattern)) {
          const line = lineNumber(text, match.index || 0);
          findings.push({
            id: check.id,
            severity: check.severity,
            file,
            line,
            message: check.message,
            excerpt: String(match[0]).replace(/\s+/g, ' ').slice(0, 220)
          });
        }
      }
    }
  }
}

await fs.mkdir('.a11y', { recursive: true });
await fs.writeFile('.a11y/template-lint.json', JSON.stringify({ generatedAt: new Date().toISOString(), findings }, null, 2));
await fs.writeFile('.a11y/template-lint.md', renderMarkdown(findings));
console.log(`Template/static findings: ${findings.length} -> .a11y/template-lint.md`);

function lineNumber(text, index) {
  return text.slice(0, index).split('\n').length;
}

function renderMarkdown(findings) {
  const lines = ['# TYPO3 template/static accessibility findings', '', `Generated: ${new Date().toISOString()}`, '', `Findings: ${findings.length}`, ''];
  if (!findings.length) {
    lines.push('No static findings found by the bundled regex checks. This does not prove accessibility conformance.');
    return lines.join('\n');
  }
  const byFile = Map.groupBy ? Map.groupBy(findings, f => f.file) : groupBy(findings, f => f.file);
  for (const [file, items] of byFile.entries()) {
    lines.push(`## ${file}`, '');
    for (const item of items) {
      lines.push(`- **${item.severity}** ${item.id} at line ${item.line}: ${item.message}`);
      lines.push(`  - \`${item.excerpt.replace(/`/g, '\\`')}\``);
    }
    lines.push('');
  }
  return lines.join('\n');
}

function groupBy(items, fn) {
  const map = new Map();
  for (const item of items) {
    const key = fn(item);
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(item);
  }
  return map;
}

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--config') result.config = argv[++i];
  }
  return result;
}
