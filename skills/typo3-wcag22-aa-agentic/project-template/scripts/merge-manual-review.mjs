#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { glob } from 'glob';
import YAML from 'yaml';

const args = parseArgs(process.argv.slice(2));
const openIssuesPath = args.output || '.a11y/open-issues.yml';
const existing = await readYaml(openIssuesPath, emptyDoc());
const inputFiles = await resolveInputFiles(args);

if (!inputFiles.length) {
  console.error('No manual review files found. Use --file path/to/export.yml or place exports in .a11y/manual-review/.');
  process.exit(1);
}

const target = normalizeDoc(existing);
const seen = new Set((target.openIssues || []).map(issue => issue.id));
let added = 0;
let addedExceptions = 0;

for (const file of inputFiles) {
  const doc = await readAny(file);
  const converted = convertManualDoc(doc, file);
  for (const issue of converted.openIssues) {
    if (!issue.id || seen.has(issue.id)) continue;
    target.openIssues.push(issue);
    seen.add(issue.id);
    added++;
  }
  for (const item of converted.exceptions) {
    target.exceptions.push(item);
    addedExceptions++;
  }
  if (!target.assessment.manualReviewSessionFiles.includes(file)) {
    target.assessment.manualReviewSessionFiles.push(file);
  }
}

target.generatedAt = new Date().toISOString();
target.assessment.lastTested = new Date().toISOString().slice(0, 10);
await fs.mkdir(path.dirname(openIssuesPath), { recursive: true });
await fs.writeFile(openIssuesPath, YAML.stringify(target));
console.log(`Merged ${added} manual issues and ${addedExceptions} exceptions into ${openIssuesPath}`);

function emptyDoc() {
  return {
    schemaVersion: '1.0.0',
    generatedAt: new Date().toISOString(),
    site: { name: '', baseUrl: '', productionUrl: '', legalProfile: '', conformanceTarget: 'WCAG 2.2 AA' },
    assessment: { status: 'partially_compliant', lastTested: '', methods: [], manualReviewSessionFiles: [] },
    openIssues: [],
    exceptions: [],
    issues: []
  };
}

function normalizeDoc(doc) {
  const normalized = { ...emptyDoc(), ...(doc || {}) };
  normalized.site = { ...emptyDoc().site, ...(doc?.site || {}) };
  normalized.assessment = { ...emptyDoc().assessment, ...(doc?.assessment || {}) };
  normalized.openIssues = Array.isArray(doc?.openIssues) ? doc.openIssues : [];
  normalized.exceptions = Array.isArray(doc?.exceptions) ? doc.exceptions : [];
  normalized.issues = Array.isArray(doc?.issues) ? doc.issues : [];
  normalized.assessment.manualReviewSessionFiles = Array.isArray(normalized.assessment.manualReviewSessionFiles) ? normalized.assessment.manualReviewSessionFiles : [];
  if (!normalized.assessment.methods.includes('Manual WCAG 2.2 AA checkpoint review with Chrome helper')) {
    normalized.assessment.methods.push('Manual WCAG 2.2 AA checkpoint review with Chrome helper');
  }
  return normalized;
}

async function resolveInputFiles(args) {
  if (args.file) return [args.file];
  const dir = args.dir || '.a11y/manual-review';
  return (await glob(`${dir}/**/*.{yml,yaml,json}`, { nodir: true })).sort();
}

async function readAny(file) {
  const raw = await fs.readFile(file, 'utf8');
  if (/\.json$/i.test(file)) return JSON.parse(raw);
  return YAML.parse(raw);
}

async function readYaml(file, fallback) {
  try { return YAML.parse(await fs.readFile(file, 'utf8')) || fallback; }
  catch (error) { if (error.code === 'ENOENT') return fallback; throw error; }
}

function convertManualDoc(doc, file) {
  if (Array.isArray(doc?.openIssues)) {
    return { openIssues: doc.openIssues, exceptions: Array.isArray(doc.exceptions) ? doc.exceptions : [] };
  }
  if (Array.isArray(doc?.results)) {
    return {
      openIssues: doc.results
        .filter(result => ['fail', 'cannot_determine', 'needs_expert_review'].includes(result.status))
        .map((result, index) => sessionResultToIssue(doc, result, file, index)),
      exceptions: []
    };
  }
  return { openIssues: [], exceptions: [] };
}

function sessionResultToIssue(session, result, file, index) {
  const date = new Date().toISOString().slice(0, 10);
  const id = `A11Y-MANUAL-${date.replaceAll('-', '')}-${String(index + 1).padStart(3, '0')}`;
  return {
    id,
    source: 'manual-review-chrome-helper',
    title: `${result.id} ${result.title}`,
    humanReviewRequired: true,
    wcag: {
      id: result.id,
      title: result.title,
      level: result.level,
      conformanceTarget: session.conformanceTarget || 'WCAG 2.2 AA'
    },
    affected: {
      pages: session.page?.url ? [session.page.url] : [],
      pageTitle: session.page?.title || '',
      selectors: [],
      typo3: {
        templates: result.typo3 && result.typo3.includes('/') ? [result.typo3] : [],
        components: result.typo3 && !result.typo3.includes('/') ? [result.typo3] : []
      }
    },
    evidence: {
      actual: result.evidence || `Manual review status: ${result.status}`,
      expected: result.expected || '',
      manualReviewFile: file
    },
    impact: {
      severity: result.severity || 'serious',
      userImpact: ''
    },
    remediation: {
      responsible: '',
      plannedFix: '',
      due: null
    },
    statement: {
      includeInAccessibilityStatement: true,
      category: result.statementCategory || 'non_conformance',
      publicText: result.expected || '',
      alternative: ''
    },
    status: 'open',
    created: date,
    updated: date
  };
}

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--file') result.file = argv[++i];
    else if (argv[i] === '--dir') result.dir = argv[++i];
    else if (argv[i] === '--output') result.output = argv[++i];
  }
  return result;
}
