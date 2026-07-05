#!/usr/bin/env node
import fs from 'node:fs/promises';
import Handlebars from 'handlebars';
import YAML from 'yaml';
import { loadConfig } from '../tests/helpers/config.js';

const args = parseArgs(process.argv.slice(2));
const config = await loadConfig(args.config || '.a11y/a11y.config.yml');
const report = await readJson('.a11y/report.json', null);
const openIssuesRaw = await readYaml('.a11y/open-issues.yml', { issues: [], openIssues: [], exceptions: [] });
const normalizedIssues = normalizeIssues(openIssuesRaw);
const normalizedExceptions = normalizeExceptions(openIssuesRaw);
const template = await fs.readFile('templates/accessibility-statement.de.md.hbs', 'utf8');

const blocking = normalizedIssues.filter(i => ['critical', 'serious'].includes(String(i.impact || '').toLowerCase()) && i.status !== 'fixed');
const advisory = normalizedIssues.filter(i => !['critical', 'serious'].includes(String(i.impact || '').toLowerCase()) && i.status !== 'fixed');
const status = config.statement?.statusOverride || (blocking.length ? 'teilweise vereinbar' : 'vorläufig teilweise vereinbar, bis die manuelle Prüfung abgeschlossen ist');
const legalProfile = config.legal?.profile || '';
const legalExample = Array.isArray(config.legal?.examples)
  ? config.legal.examples.find(example => example.id === legalProfile)
  : null;

const data = {
  today: new Date().toLocaleDateString(config.site?.locale || 'de-AT', { year: 'numeric', month: '2-digit', day: '2-digit' }),
  generatedAt: new Date().toISOString(),
  site: config.site || {},
  legal: config.legal || {},
  legalExample: legalExample || {},
  hasLegalExample: Boolean(legalExample),
  statement: config.statement || {},
  status,
  reportSummary: report?.summary || {},
  blockingIssues: blocking.slice(0, 20),
  advisoryIssues: advisory.slice(0, 20),
  structuredIssueCount: normalizedIssues.length,
  exceptionIssues: normalizedExceptions,
  hitl: config.hitl || {},
  hasBlockingIssues: blocking.length > 0,
  hasAdvisoryIssues: advisory.length > 0,
  knownNonAccessibleContent: config.statement?.knownNonAccessibleContent || [],
  disproportionateBurden: mergeConfiguredAndStructured(config.statement?.disproportionateBurden || [], normalizedExceptions.filter(item => item.reasonCategory === 'disproportionate_burden')),
  outsideScope: mergeConfiguredAndStructured(config.statement?.outsideScope || [], normalizedExceptions.filter(item => ['outside_scope', 'third_party_content', 'archived_content'].includes(item.reasonCategory))),
  plannedRemediation: config.statement?.plannedRemediation || [],
  additionalLegalNotes: config.statement?.additionalLegalNotes || []
};

Handlebars.registerHelper('or', (a, b) => a || b);
Handlebars.registerHelper('json', value => JSON.stringify(value, null, 2));

const output = Handlebars.compile(template)(data);
await fs.mkdir('.a11y', { recursive: true });
await fs.writeFile('.a11y/accessibility-statement-draft.de.md', output);
console.log('Statement draft written: .a11y/accessibility-statement-draft.de.md');


function normalizeIssues(raw) {
  const structured = Array.isArray(raw?.openIssues) ? raw.openIssues.map(normalizeStructuredIssue) : [];
  const legacy = Array.isArray(raw?.issues) ? raw.issues.map(normalizeLegacyIssue) : [];
  const map = new Map();
  for (const issue of [...structured, ...legacy]) {
    if (!issue?.id) continue;
    if (!map.has(issue.id)) map.set(issue.id, issue);
  }
  return [...map.values()];
}

function normalizeStructuredIssue(issue) {
  const severity = issue.impact?.severity || issue.impact || 'moderate';
  const wcagLabel = issue.wcag?.id ? `${issue.wcag.id} ${issue.wcag.title || ''}`.trim() : (Array.isArray(issue.wcag?.ids) ? issue.wcag.ids.join(', ') : '');
  const affectedPages = issue.affected?.pageStates || issue.affected?.pages || issue.affectedPages || [];
  const plannedFix = issue.remediation?.plannedFix || issue.plannedFix || '';
  return {
    id: issue.id,
    source: issue.source || 'structured-open-issues',
    title: issue.title || wcagLabel || issue.id,
    impact: String(severity).toLowerCase(),
    status: issue.status || 'open',
    wcag: wcagLabel,
    affectedPages,
    file: issue.affected?.file || issue.file || '',
    line: issue.affected?.line || issue.line || '',
    plannedFix,
    publicText: issue.statement?.publicText || '',
    category: issue.statement?.category || issue.statementCategory || 'non_conformance',
    humanReviewRequired: Boolean(issue.humanReviewRequired),
  };
}

function normalizeLegacyIssue(issue) {
  return {
    id: issue.id,
    source: issue.source || 'legacy-open-issues',
    title: issue.title || issue.help || issue.id,
    impact: String(issue.impact || issue.severity || 'moderate').toLowerCase(),
    status: issue.status || 'open',
    wcag: Array.isArray(issue.wcagTags) ? issue.wcagTags.join(', ') : '',
    affectedPages: issue.affectedPages || issue.pages || [],
    file: issue.file || '',
    line: issue.line || '',
    plannedFix: issue.plannedFix || '',
    publicText: issue.publicText || '',
    category: issue.statementCategory || 'non_conformance',
    humanReviewRequired: Boolean(issue.humanReviewRequired),
  };
}

function normalizeExceptions(raw) {
  if (!Array.isArray(raw?.exceptions)) return [];
  return raw.exceptions.map(item => ({
    id: item.id || '',
    title: item.title || '',
    reasonCategory: item.reasonCategory || item.category || '',
    publicText: item.publicText || item.statement?.publicText || item.title || '',
    accessibleAlternative: item.accessibleAlternative || item.alternative || '',
    reviewDate: item.reviewDate || '',
  }));
}

function mergeConfiguredAndStructured(configured, structured) {
  const structuredText = structured.map(item => {
    const parts = [item.publicText || item.title];
    if (item.accessibleAlternative) parts.push(`Alternative: ${item.accessibleAlternative}`);
    if (item.reviewDate) parts.push(`Prüfdatum: ${item.reviewDate}`);
    return parts.filter(Boolean).join(' — ');
  }).filter(Boolean);
  return [...configured, ...structuredText];
}

async function readJson(file, fallback) {
  try { return JSON.parse(await fs.readFile(file, 'utf8')); }
  catch (error) { if (error.code === 'ENOENT') return fallback; throw error; }
}

async function readYaml(file, fallback) {
  try { return YAML.parse(await fs.readFile(file, 'utf8')) || fallback; }
  catch (error) { if (error.code === 'ENOENT') return fallback; throw error; }
}

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--config') result.config = argv[++i];
  }
  return result;
}
