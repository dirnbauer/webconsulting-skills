#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { glob } from 'glob';
import YAML from 'yaml';
import { loadConfig } from '../tests/helpers/config.js';

const args = parseArgs(process.argv.slice(2));
const config = await loadConfig(args.config || '.a11y/a11y.config.yml');
const files = await glob('.a11y/raw/*.json', { nodir: true });
const templateLint = await readJson('.a11y/template-lint.json', { findings: [] });
const existingOpenIssues = await readYaml('.a11y/open-issues.yml', null);
const rawScans = [];
const customChecks = [];

for (const file of files) {
  const data = await readJson(file, null);
  if (!data) continue;
  if (data.result) rawScans.push(data);
  else if (data.keyboard || data.reflow || data.targetSize || data.focusStyle) customChecks.push(data);
}

const issueMap = new Map();
for (const scan of rawScans) {
  for (const violation of scan.result?.violations || []) {
    const key = violation.id;
    if (!issueMap.has(key)) {
      issueMap.set(key, {
        id: violation.id,
        impact: violation.impact || 'unknown',
        help: violation.help,
        description: violation.description,
        helpUrl: violation.helpUrl,
        tags: violation.tags || [],
        occurrences: 0,
        pages: [],
        templates: new Set(),
        components: new Set(),
        selectors: new Set(),
        html: []
      });
    }
    const issue = issueMap.get(key);
    issue.occurrences += (violation.nodes || []).length;
    issue.pages.push({ url: scan.url, stateName: scan.stateName, count: (violation.nodes || []).length });
    for (const node of violation.nodes || []) {
      for (const target of node.target || []) issue.selectors.add(String(target));
      if (node.html) issue.html.push(node.html.replace(/\s+/g, ' ').slice(0, 300));
      if (node.typo3?.template) issue.templates.add(node.typo3.template);
      if (node.typo3?.component) issue.components.add(node.typo3.component);
    }
  }
}

const issues = [...issueMap.values()].map(issue => ({
  ...issue,
  pages: mergePages(issue.pages),
  templates: [...issue.templates].sort(),
  components: [...issue.components].sort(),
  selectors: [...issue.selectors].slice(0, 25),
  html: [...new Set(issue.html)].slice(0, 5)
})).sort((a, b) => impactScore(b.impact) - impactScore(a.impact) || b.occurrences - a.occurrences || a.id.localeCompare(b.id));

const report = {
  generatedAt: new Date().toISOString(),
  site: config.site,
  legal: config.legal,
  summary: {
    scannedStates: rawScans.length,
    scannedUrls: [...new Set(rawScans.map(s => s.url))].length,
    axeIssueTypes: issues.length,
    axeOccurrences: issues.reduce((sum, issue) => sum + issue.occurrences, 0),
    templateStaticFindings: templateLint.findings?.length || 0,
    customChecks: customChecks.length
  },
  issues,
  customChecks: summarizeCustom(customChecks),
  templateFindings: templateLint.findings || [],
  hitlRequired: config.hitl?.required || []
};

await fs.mkdir('.a11y', { recursive: true });
await fs.writeFile('.a11y/report.json', JSON.stringify(report, null, 2));
await fs.writeFile('.a11y/report.md', renderMarkdown(report));
await fs.writeFile('.a11y/open-issues.yml', YAML.stringify(renderOpenIssues(report, existingOpenIssues)));
console.log(`Report written: .a11y/report.md (${report.summary.axeIssueTypes} axe issue types)`);

function mergePages(pages) {
  const map = new Map();
  for (const page of pages) {
    const key = `${page.url} :: ${page.stateName}`;
    map.set(key, { ...page, count: (map.get(key)?.count || 0) + page.count });
  }
  return [...map.values()].sort((a, b) => a.url.localeCompare(b.url));
}

function impactScore(impact) {
  return { minor: 1, moderate: 2, serious: 3, critical: 4 }[impact] || 0;
}

function summarizeCustom(customChecks) {
  return customChecks.map(check => ({
    url: check.url,
    horizontalOverflow: Boolean(check.reflow?.hasHorizontalOverflow),
    smallTargets: check.targetSize?.smallTargets?.length || 0,
    possibleMissingFocusStyle: check.focusStyle?.possibleMissingFocusStyle?.length || 0,
    keyboardSteps: check.keyboard?.steps?.length || 0,
    needsHumanReview: Boolean(check.keyboard?.needsHumanReview || check.targetSize?.needsHumanReview || check.focusStyle?.needsHumanReview)
  }));
}

function renderOpenIssues(report, existing = null) {
  const generatedLegacy = [];
  const generatedStructured = [];

  for (const issue of report.issues) {
    generatedLegacy.push({
      id: `AXE-${issue.id}`,
      source: 'axe-core',
      title: issue.help,
      impact: issue.impact,
      wcagTags: issue.tags.filter(t => /^wcag/.test(t)),
      occurrences: issue.occurrences,
      affectedPages: issue.pages.slice(0, 10).map(p => `${p.url} (${p.stateName}, ${p.count})`),
      affectedTemplates: issue.templates,
      affectedComponents: issue.components,
      status: 'open',
      owner: '',
      plannedFix: '',
      statementCategory: 'non_conformance',
      humanReviewRequired: false
    });
    generatedStructured.push({
      id: `AXE-${issue.id}`,
      source: 'axe-core',
      title: issue.help,
      humanReviewRequired: false,
      wcag: {
        tags: issue.tags.filter(t => /^wcag/.test(t)),
        ids: wcagIdsFromTags(issue.tags),
        conformanceTarget: report.legal?.targetStandard || 'WCAG 2.2 AA'
      },
      affected: {
        pages: issue.pages.slice(0, 10).map(p => p.url),
        pageStates: issue.pages.slice(0, 10).map(p => `${p.url} (${p.stateName}, ${p.count})`),
        selectors: issue.selectors || [],
        typo3: {
          templates: issue.templates || [],
          components: issue.components || []
        }
      },
      evidence: {
        actual: issue.description || issue.help,
        expected: 'Fix the automated accessibility violation and re-test the same page state.',
        htmlSamples: issue.html || [],
        helpUrl: issue.helpUrl || null
      },
      impact: {
        severity: issue.impact || 'unknown',
        userImpact: ''
      },
      remediation: {
        responsible: '',
        plannedFix: '',
        due: null
      },
      statement: {
        includeInAccessibilityStatement: true,
        category: 'non_conformance',
        publicText: '',
        alternative: ''
      },
      status: 'open',
      created: report.generatedAt.slice(0, 10),
      updated: report.generatedAt.slice(0, 10)
    });
  }

  for (const finding of report.templateFindings) {
    generatedLegacy.push({
      id: `TPL-${finding.id}-${finding.line}`,
      source: 'template-static',
      title: finding.message,
      impact: finding.severity,
      file: finding.file,
      line: finding.line,
      status: 'open',
      owner: '',
      plannedFix: '',
      statementCategory: 'non_conformance',
      humanReviewRequired: finding.severity !== 'serious'
    });
    generatedStructured.push({
      id: `TPL-${finding.id}-${finding.line}`,
      source: 'template-static',
      title: finding.message,
      humanReviewRequired: finding.severity !== 'serious',
      wcag: {
        tags: [],
        ids: [],
        conformanceTarget: report.legal?.targetStandard || 'WCAG 2.2 AA'
      },
      affected: {
        pages: [],
        selectors: [],
        typo3: {
          templates: [finding.file],
          components: []
        },
        file: finding.file,
        line: finding.line
      },
      evidence: {
        actual: finding.message,
        expected: 'Fix the TYPO3 template/static accessibility pattern and re-test.'
      },
      impact: {
        severity: finding.severity || 'moderate',
        userImpact: ''
      },
      remediation: {
        responsible: '',
        plannedFix: '',
        due: null
      },
      statement: {
        includeInAccessibilityStatement: true,
        category: 'non_conformance',
        publicText: '',
        alternative: ''
      },
      status: 'open',
      created: report.generatedAt.slice(0, 10),
      updated: report.generatedAt.slice(0, 10)
    });
  }

  for (const item of report.customChecks) {
    if (item.horizontalOverflow || item.smallTargets || item.possibleMissingFocusStyle) {
      generatedLegacy.push({
        id: `CUSTOM-${slug(item.url)}`,
        source: 'custom-browser-checks',
        title: 'Custom browser checks need review',
        impact: item.horizontalOverflow ? 'serious' : 'warning',
        affectedPages: [item.url],
        details: item,
        status: 'open',
        owner: '',
        plannedFix: '',
        statementCategory: 'non_conformance',
        humanReviewRequired: true
      });
      generatedStructured.push({
        id: `CUSTOM-${slug(item.url)}`,
        source: 'custom-browser-checks',
        title: 'Custom browser checks need review',
        humanReviewRequired: true,
        wcag: {
          tags: [],
          ids: [],
          conformanceTarget: report.legal?.targetStandard || 'WCAG 2.2 AA'
        },
        affected: {
          pages: [item.url],
          selectors: [],
          typo3: { templates: [], components: [] }
        },
        evidence: {
          actual: JSON.stringify(item),
          expected: 'Human reviewer confirms whether this is a WCAG failure and maps it to a specific checkpoint.'
        },
        impact: {
          severity: item.horizontalOverflow ? 'serious' : 'moderate',
          userImpact: ''
        },
        remediation: {
          responsible: '',
          plannedFix: '',
          due: null
        },
        statement: {
          includeInAccessibilityStatement: true,
          category: 'non_conformance',
          publicText: '',
          alternative: ''
        },
        status: 'open',
        created: report.generatedAt.slice(0, 10),
        updated: report.generatedAt.slice(0, 10)
      });
    }
  }

  const preservedStructured = preserveManualStructuredIssues(existing);
  const preservedLegacy = preserveManualLegacyIssues(existing);
  const exceptions = Array.isArray(existing?.exceptions) ? existing.exceptions : [];

  return {
    schemaVersion: '1.0.0',
    generatedAt: report.generatedAt,
    site: {
      name: report.site?.name || '',
      baseUrl: report.site?.baseUrl || '',
      productionUrl: report.site?.productionUrl || '',
      legalProfile: report.legal?.profile || '',
      conformanceTarget: report.legal?.targetStandard || 'WCAG 2.2 AA'
    },
    assessment: {
      status: 'partially_compliant',
      lastTested: report.generatedAt.slice(0, 10),
      methods: [
        'Automated scan with Playwright and axe-core',
        'TYPO3 Fluid/SCSS/JS template review',
        'Manual WCAG 2.2 AA checkpoint review when documented in this file'
      ],
      manualReviewSessionFiles: existing?.assessment?.manualReviewSessionFiles || []
    },
    targetStandard: report.legal?.targetStandard || 'WCAG 2.2 AA',
    issues: [...generatedLegacy, ...preservedLegacy],
    openIssues: [...generatedStructured, ...preservedStructured],
    exceptions
  };
}

function preserveManualStructuredIssues(existing) {
  if (!Array.isArray(existing?.openIssues)) return [];
  return existing.openIssues.filter(issue => !isGeneratedSource(issue?.source));
}

function preserveManualLegacyIssues(existing) {
  if (!Array.isArray(existing?.issues)) return [];
  return existing.issues.filter(issue => !isGeneratedSource(issue?.source));
}

function isGeneratedSource(source) {
  return ['axe-core', 'template-static', 'custom-browser-checks'].includes(String(source || ''));
}

function wcagIdsFromTags(tags = []) {
  const ids = [];
  for (const tag of tags) {
    const match = String(tag).match(/^wcag(\d)(\d)(\d)$/);
    if (match) ids.push(`${match[1]}.${match[2]}.${match[3]}`);
  }
  return [...new Set(ids)].sort();
}

function renderMarkdown(report) {
  const lines = [];
  lines.push(`# Accessibility report: ${report.site?.name || 'TYPO3 site'}`);
  lines.push('', `Generated: ${report.generatedAt}`, '');
  lines.push('## Summary', '');
  lines.push(`- Scanned URLs: ${report.summary.scannedUrls}`);
  lines.push(`- Scanned page states: ${report.summary.scannedStates}`);
  lines.push(`- Axe issue types: ${report.summary.axeIssueTypes}`);
  lines.push(`- Axe occurrences: ${report.summary.axeOccurrences}`);
  lines.push(`- Template/static findings: ${report.summary.templateStaticFindings}`);
  lines.push('', '> Automated results do not prove full WCAG conformance. Use the HITL checklist before publishing a final Erklärung zur Barrierefreiheit.', '');

  lines.push('## Axe findings', '');
  if (!report.issues.length) lines.push('No automated axe violations found in scanned states.', '');
  for (const issue of report.issues) {
    lines.push(`### ${issue.impact.toUpperCase()} — ${issue.id}: ${issue.help}`);
    lines.push('', issue.description || '', '');
    if (issue.tags?.length) lines.push(`Tags: ${issue.tags.join(', ')}`, '');
    lines.push(`Occurrences: ${issue.occurrences}`, '');
    if (issue.components.length) lines.push(`Components: ${issue.components.join(', ')}`, '');
    if (issue.templates.length) lines.push(`Templates: ${issue.templates.join(', ')}`, '');
    lines.push('Affected pages:');
    for (const page of issue.pages.slice(0, 12)) lines.push(`- ${page.url} (${page.stateName}): ${page.count}`);
    if (issue.helpUrl) lines.push('', `Help: ${issue.helpUrl}`);
    lines.push('');
  }

  lines.push('## Custom browser checks', '');
  if (!report.customChecks.length) lines.push('No custom check artifacts found.', '');
  for (const check of report.customChecks) {
    lines.push(`- ${check.url}: horizontalOverflow=${check.horizontalOverflow}, smallTargets=${check.smallTargets}, possibleMissingFocusStyle=${check.possibleMissingFocusStyle}, keyboardSteps=${check.keyboardSteps}`);
  }
  lines.push('');

  lines.push('## Template/static findings', '');
  if (!report.templateFindings.length) lines.push('No static template findings found.', '');
  for (const finding of report.templateFindings.slice(0, 100)) {
    lines.push(`- **${finding.severity}** ${finding.file}:${finding.line} — ${finding.message}`);
  }
  lines.push('');

  lines.push('## Required human review', '');
  for (const item of report.hitlRequired || []) lines.push(`- ${item}`);
  lines.push('');
  return lines.join('\n');
}

async function readJson(file, fallback) {
  try {
    return JSON.parse(await fs.readFile(file, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') return fallback;
    throw error;
  }
}


async function readYaml(file, fallback) {
  try {
    return YAML.parse(await fs.readFile(file, 'utf8')) || fallback;
  } catch (error) {
    if (error.code === 'ENOENT') return fallback;
    throw error;
  }
}

function slug(input) {
  return String(input || 'page').replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').slice(0, 60).toLowerCase() || 'page';
}

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--config') result.config = argv[++i];
  }
  return result;
}
