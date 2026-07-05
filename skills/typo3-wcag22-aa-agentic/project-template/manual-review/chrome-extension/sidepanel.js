const CHECKPOINT_URL = chrome.runtime.getURL('data/wcag22-aa-checkpoints.json');
const state = {
  tab: null,
  pageKey: null,
  data: null,
  review: {},
  scan: null,
  focusOrder: [],
};

const $ = (selector) => document.querySelector(selector);
const checklist = $('#checklist');
const template = $('#checkpoint-template');

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

function safeFilePart(value) {
  return String(value || 'page').replace(/^https?:\/\//, '').replace(/[^a-z0-9_.-]+/gi, '-').replace(/^-+|-+$/g, '').slice(0, 90) || 'page';
}

function yamlScalar(value) {
  if (value === null || value === undefined || value === '') return 'null';
  const s = String(value);
  if (/^[a-zA-Z0-9_.:/@ -]+$/.test(s) && !s.includes('#') && !s.includes(': ')) return JSON.stringify(s);
  return JSON.stringify(s);
}

function toYaml(value, indent = 0) {
  const sp = ' '.repeat(indent);
  if (Array.isArray(value)) {
    if (value.length === 0) return '[]';
    return value.map((item) => {
      if (item && typeof item === 'object') {
        const nested = toYaml(item, indent + 2);
        return `${sp}- ${nested.startsWith(' '.repeat(indent + 2)) ? '\n' + nested : nested}`;
      }
      return `${sp}- ${yamlScalar(item)}`;
    }).join('\n');
  }
  if (value && typeof value === 'object') {
    const entries = Object.entries(value).filter(([, v]) => v !== undefined);
    if (entries.length === 0) return '{}';
    return entries.map(([key, val]) => {
      if (Array.isArray(val)) {
        if (val.length === 0) return `${sp}${key}: []`;
        return `${sp}${key}:\n${toYaml(val, indent + 2)}`;
      }
      if (val && typeof val === 'object') {
        return `${sp}${key}:\n${toYaml(val, indent + 2)}`;
      }
      return `${sp}${key}: ${yamlScalar(val)}`;
    }).join('\n');
  }
  return `${sp}${yamlScalar(value)}`;
}

async function downloadText(filename, text, mime = 'application/octet-stream') {
  const blob = new Blob([text], { type: `${mime};charset=utf-8` });
  const url = URL.createObjectURL(blob);
  await chrome.downloads.download({ url, filename, saveAs: true });
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

async function activeTab() {
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  return tabs[0] || null;
}

function pageStorageKey(tab) {
  const url = tab?.url || 'unknown';
  return `wcagManualReview:v1:${url}`;
}

async function loadCheckpoints() {
  const response = await fetch(CHECKPOINT_URL);
  state.data = await response.json();
}

async function loadPageReview() {
  if (!state.pageKey) return;
  const data = await chrome.storage.local.get(state.pageKey);
  state.review = data[state.pageKey] || {};
  $('#reviewer').value = state.review.__meta?.reviewer || '';
  $('#legal-profile').value = state.review.__meta?.legalProfile || 'at-public-wzg';
}

async function savePageReview() {
  if (!state.pageKey) return;
  state.review.__meta = {
    reviewer: $('#reviewer').value.trim(),
    legalProfile: $('#legal-profile').value,
    pageUrl: state.tab?.url || null,
    pageTitle: state.tab?.title || null,
    updated: new Date().toISOString(),
  };
  await chrome.storage.local.set({ [state.pageKey]: state.review });
}

async function connectPage() {
  state.tab = await activeTab();
  if (!state.tab?.id) throw new Error('No active tab found.');
  state.pageKey = pageStorageKey(state.tab);
  $('#page-meta').textContent = `${state.tab.title || 'Untitled'} — ${state.tab.url || ''}`;
  await chrome.scripting.executeScript({ target: { tabId: state.tab.id }, files: ['content.js'] });
  await loadPageReview();
  renderChecklist();
}

async function sendToPage(message) {
  if (!state.tab?.id) await connectPage();
  try {
    return await chrome.tabs.sendMessage(state.tab.id, message);
  } catch (error) {
    await chrome.scripting.executeScript({ target: { tabId: state.tab.id }, files: ['content.js'] });
    return chrome.tabs.sendMessage(state.tab.id, message);
  }
}

function checkpointStatus(id) {
  return state.review[id]?.status || 'not_tested';
}

function getFilteredCheckpoints() {
  const query = $('#search').value.trim().toLowerCase();
  const status = $('#status-filter').value;
  const level = $('#level-filter').value;
  return state.data.checkpoints.filter((cp) => {
    const review = state.review[cp.id] || {};
    const haystack = [cp.id, cp.title, cp.level, cp.principle, cp.guideline, cp.reviewFocus, cp.question, review.evidence, review.expected, review.typo3].join(' ').toLowerCase();
    if (query && !haystack.includes(query)) return false;
    if (status !== 'all' && checkpointStatus(cp.id) !== status) return false;
    if (level !== 'all' && cp.level !== level) return false;
    return true;
  });
}

function renderChecklist() {
  if (!state.data) return;
  checklist.textContent = '';
  const cps = getFilteredCheckpoints();
  let lastGroup = '';
  for (const cp of cps) {
    const group = `${cp.principle} — ${cp.guideline}`;
    if (group !== lastGroup) {
      const h = document.createElement('h2');
      h.className = 'group-title';
      h.textContent = group;
      checklist.append(h);
      lastGroup = group;
    }
    const node = template.content.firstElementChild.cloneNode(true);
    const review = state.review[cp.id] || {};
    node.dataset.id = cp.id;
    node.dataset.status = review.status || 'not_tested';
    node.querySelector('h2').textContent = `${cp.id} ${cp.title}`;
    node.querySelector('.meta').textContent = `Level ${cp.level} · added in WCAG ${cp.addedIn} · ${cp.automation}`;
    node.querySelector('.official').href = cp.officialUnderstandingUrl;
    node.querySelector('.question').textContent = cp.question;
    node.querySelector('.focus').textContent = `Review focus: ${cp.reviewFocus}`;
    node.querySelector('.status').value = review.status || 'not_tested';
    node.querySelector('.severity').value = review.severity || (cp.level === 'A' ? 'serious' : 'moderate');
    node.querySelector('.statement-category').value = review.statementCategory || 'non_conformance';
    node.querySelector('.evidence').value = review.evidence || '';
    node.querySelector('.expected').value = review.expected || '';
    node.querySelector('.typo3').value = review.typo3 || '';
    for (const input of node.querySelectorAll('select, textarea, input')) {
      input.addEventListener('change', () => updateCheckpointFromNode(cp.id, node));
      input.addEventListener('input', () => updateCheckpointFromNode(cp.id, node));
    }
    checklist.append(node);
  }
  if (cps.length === 0) {
    const p = document.createElement('p');
    p.textContent = 'No checkpoints match the current filters.';
    checklist.append(p);
  }
}

async function updateCheckpointFromNode(id, node) {
  state.review[id] = {
    ...(state.review[id] || {}),
    status: node.querySelector('.status').value,
    severity: node.querySelector('.severity').value,
    statementCategory: node.querySelector('.statement-category').value,
    evidence: node.querySelector('.evidence').value.trim(),
    expected: node.querySelector('.expected').value.trim(),
    typo3: node.querySelector('.typo3').value.trim(),
    updated: new Date().toISOString(),
  };
  node.dataset.status = state.review[id].status;
  await savePageReview();
}

function renderScanSummary(scan) {
  if (!scan) return;
  const root = $('#scan-summary');
  const duplicateIds = scan.duplicateIds?.length || 0;
  root.innerHTML = `
    <strong>Page helper scan:</strong>
    <ul>
      <li>Title: ${escapeHtml(scan.title || 'missing')}</li>
      <li>HTML lang: ${escapeHtml(scan.htmlLang || 'missing')}</li>
      <li>Headings: ${scan.headings.length} (${scan.headings.filter(h => h.level === 1).length} H1)</li>
      <li>Landmarks/regions: ${scan.landmarks.length}</li>
      <li>Images: ${scan.images.total}; missing alt: ${scan.images.missingAlt.length}; empty alt: ${scan.images.emptyAlt.length}</li>
      <li>Form controls: ${scan.forms.controls}; potentially unlabeled: ${scan.forms.unlabeled.length}</li>
      <li>Links: ${scan.links.total}; generic/empty suspects: ${scan.links.suspect.length}</li>
      <li>Focusable elements: ${scan.focusable.total}; small targets: ${scan.focusable.smallTargets.length}</li>
      <li>Duplicate IDs: ${duplicateIds}</li>
      <li>Iframes: ${scan.iframes.total}; missing title: ${scan.iframes.missingTitle.length}</li>
      <li>Videos: ${scan.media.videos}; videos without caption track: ${scan.media.videosWithoutCaptionTrack}</li>
    </ul>`;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch]));
}

function makeSessionExport() {
  const results = state.data.checkpoints.map((cp) => ({
    id: cp.id,
    title: cp.title,
    level: cp.level,
    guideline: cp.guideline,
    status: checkpointStatus(cp.id),
    severity: state.review[cp.id]?.severity || null,
    statementCategory: state.review[cp.id]?.statementCategory || null,
    evidence: state.review[cp.id]?.evidence || null,
    expected: state.review[cp.id]?.expected || null,
    typo3: state.review[cp.id]?.typo3 || null,
  }));
  return {
    schemaVersion: '1.0.0',
    tool: 'TYPO3 WCAG 2.2 AA Manual Review Helper',
    exportedAt: new Date().toISOString(),
    reviewer: $('#reviewer').value.trim() || null,
    legalProfile: $('#legal-profile').value,
    page: {
      title: state.tab?.title || null,
      url: state.tab?.url || null,
    },
    conformanceTarget: state.data.conformanceTarget,
    counts: state.data.counts,
    scan: state.scan,
    focusOrder: state.focusOrder,
    results,
  };
}

function makeIssuesExport() {
  const pageUrl = state.tab?.url || null;
  const pageTitle = state.tab?.title || null;
  const failures = state.data.checkpoints.filter((cp) => ['fail', 'cannot_determine', 'needs_expert_review'].includes(checkpointStatus(cp.id)));
  const openIssues = failures.map((cp, index) => {
    const review = state.review[cp.id] || {};
    const suffix = String(index + 1).padStart(3, '0');
    return {
      id: `A11Y-MANUAL-${todayIso().replaceAll('-', '')}-${suffix}`,
      title: review.expected ? `${cp.id} ${cp.title}` : `${cp.id} ${cp.title} needs review/fix`,
      source: 'manual-review-chrome-helper',
      humanReviewRequired: true,
      wcag: {
        id: cp.id,
        title: cp.title,
        level: cp.level,
        conformanceTarget: 'WCAG 2.2 AA',
        officialUnderstandingUrl: cp.officialUnderstandingUrl,
      },
      affected: {
        pages: pageUrl ? [pageUrl] : [],
        pageTitle,
        selectors: [],
        typo3: {
          components: review.typo3 && !review.typo3.includes('/') ? [review.typo3] : [],
          templates: review.typo3 && review.typo3.includes('/') ? [review.typo3] : [],
        },
      },
      evidence: {
        actual: review.evidence || 'Manual review marked this checkpoint as failing or undecided. Add concrete evidence before publishing.',
        expected: review.expected || cp.question,
        reviewFocus: cp.reviewFocus,
      },
      impact: {
        severity: review.severity || (cp.level === 'A' ? 'serious' : 'moderate'),
        userImpact: '',
      },
      remediation: {
        responsible: '',
        plannedFix: '',
        due: null,
      },
      statement: {
        includeInAccessibilityStatement: true,
        category: review.statementCategory || 'non_conformance',
        publicText: review.expected || '',
        alternative: '',
      },
      status: 'open',
      created: todayIso(),
      updated: todayIso(),
    };
  });
  return {
    schemaVersion: '1.0.0',
    site: {
      name: '',
      baseUrl: '',
      productionUrl: '',
      legalProfile: $('#legal-profile').value,
      conformanceTarget: 'WCAG 2.2 AA',
    },
    assessment: {
      status: 'partially_compliant',
      lastTested: todayIso(),
      methods: [
        'Automated scan with Playwright and axe-core',
        'TYPO3 Fluid/SCSS/JS template review',
        'Manual WCAG 2.2 AA checkpoint review with Chrome helper',
      ],
      manualReviewSessionFiles: [],
    },
    openIssues,
    exceptions: [],
  };
}

function makeCodexPrompt() {
  const session = makeSessionExport();
  return `Use the TYPO3 WCAG 2.2 AA accessibility skill.\n\nInput: I exported a manual review session from the Chrome helper. Merge all failing, undecided, and expert-review items into .a11y/open-issues.yml. Do not free-write the accessibility statement. Generate it only from .a11y/open-issues.yml and documented exceptions.\n\nTasks:\n1. Read the manual review JSON/YAML export.\n2. Map each issue to TYPO3 Fluid/SCSS/JS/TCA/RTE files where possible.\n3. Fix confirmed template/code issues.\n4. Keep semantic/editorial issues as human-review items.\n5. Run npm run a11y:all.\n6. Regenerate .a11y/report.md and .a11y/accessibility-statement-draft.de.md.\n\nPage: ${session.page.url || 'unknown'}\nLegal profile: ${session.legalProfile}\nConformance target: WCAG 2.2 AA\n`;
}

async function initEvents() {
  $('#connect').addEventListener('click', async () => {
    await connectPage();
  });
  $('#scan').addEventListener('click', async () => {
    state.scan = await sendToPage({ type: 'wcag-helper-scan' });
    renderScanSummary(state.scan);
    await savePageReview();
  });
  for (const [id, kind] of [
    ['highlight-headings', 'headings'],
    ['highlight-landmarks', 'landmarks'],
    ['highlight-images', 'images'],
    ['highlight-forms', 'forms'],
    ['highlight-links', 'links'],
    ['highlight-focusables', 'focusables'],
    ['highlight-targets', 'small-targets'],
  ]) {
    $(`#${id}`).addEventListener('click', () => sendToPage({ type: 'wcag-helper-highlight', kind }));
  }
  $('#clear-highlights').addEventListener('click', () => sendToPage({ type: 'wcag-helper-clear' }));
  $('#start-focus').addEventListener('click', () => sendToPage({ type: 'wcag-helper-focus-start' }));
  $('#stop-focus').addEventListener('click', () => sendToPage({ type: 'wcag-helper-focus-stop' }));
  $('#get-focus').addEventListener('click', async () => {
    const result = await sendToPage({ type: 'wcag-helper-focus-get' });
    state.focusOrder = result?.focusOrder || [];
    $('#scan-summary').insertAdjacentHTML('beforeend', `<p><strong>Focus order entries:</strong> ${state.focusOrder.length}</p>`);
  });
  $('#search').addEventListener('input', renderChecklist);
  $('#status-filter').addEventListener('change', renderChecklist);
  $('#level-filter').addEventListener('change', renderChecklist);
  $('#reviewer').addEventListener('input', savePageReview);
  $('#legal-profile').addEventListener('change', savePageReview);
  $('#export-session').addEventListener('click', async () => {
    const session = makeSessionExport();
    const filename = `.a11y/manual-review/${todayIso()}-${safeFilePart(state.tab?.url)}.json`;
    await downloadText(filename, JSON.stringify(session, null, 2) + '\n', 'application/json');
  });
  $('#export-issues').addEventListener('click', async () => {
    const doc = makeIssuesExport();
    const filename = `.a11y/manual-review/${todayIso()}-${safeFilePart(state.tab?.url)}-open-issues.yml`;
    await downloadText(filename, toYaml(doc) + '\n', 'text/yaml');
  });
  $('#copy-codex').addEventListener('click', async () => {
    await navigator.clipboard.writeText(makeCodexPrompt());
    $('#copy-codex').textContent = 'Copied';
    setTimeout(() => { $('#copy-codex').textContent = 'Copy Codex prompt'; }, 1200);
  });
  $('#reset-page').addEventListener('click', async () => {
    if (!state.pageKey) return;
    if (!confirm('Reset manual review data for this exact page URL?')) return;
    state.review = {};
    await chrome.storage.local.remove(state.pageKey);
    renderChecklist();
  });
}

async function main() {
  await loadCheckpoints();
  await initEvents();
  try {
    await connectPage();
  } catch (error) {
    $('#page-meta').textContent = error.message;
    renderChecklist();
  }
}

main();
