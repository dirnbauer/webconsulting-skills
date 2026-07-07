#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

function usage() {
  console.error(`Usage:
  node scripts/wcag22_audit.cjs --url <url> [--url <url> ...] [--out audit.json] [--markdown audit.md]

Options:
  --url       URL to audit. Repeat for multiple pages.
  --out       JSON report path. Default: wcag22-audit.json
  --markdown  Markdown report path. Optional.
  --viewport  Viewport as WIDTHxHEIGHT. Default: 1280x900
  --no-keyboard  Skip the basic Tab-order probe.

Dependencies:
  npm install --no-save playwright axe-core
`);
}

function parseArgs(argv) {
  const args = { urls: [], out: 'wcag22-audit.json', markdown: '', viewport: { width: 1280, height: 900 }, keyboard: true };
  for (let i = 2; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--url') {
      args.urls.push(argv[++i]);
    } else if (arg === '--out') {
      args.out = argv[++i];
    } else if (arg === '--markdown') {
      args.markdown = argv[++i];
    } else if (arg === '--viewport') {
      const [width, height] = String(argv[++i]).split('x').map(Number);
      if (!width || !height) {
        throw new Error('Viewport must use WIDTHxHEIGHT, e.g. 1280x900');
      }
      args.viewport = { width, height };
    } else if (arg === '--no-keyboard') {
      args.keyboard = false;
    } else if (arg === '--help' || arg === '-h') {
      usage();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  if (args.urls.length === 0) {
    throw new Error('At least one --url is required.');
  }
  return args;
}

function loadDependency(name) {
  try {
    return require(name);
  } catch (error) {
    throw new Error(`Missing dependency "${name}". Install it in the current project with: npm install --no-save playwright axe-core`);
  }
}

function axeTags() {
  return ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22a', 'wcag22aa'];
}

function summarizeAxeResult(result) {
  return {
    axeVersion: result.testEngine.version,
    violations: result.violations.map(summarizeRule),
    incomplete: result.incomplete.map(summarizeRule),
    passes: result.passes.length,
    inapplicable: result.inapplicable.length,
  };
}

function summarizeRule(rule) {
  return {
    id: rule.id,
    impact: rule.impact || '',
    help: rule.help,
    tags: rule.tags.filter((tag) => tag.startsWith('wcag')),
    nodes: rule.nodes.length,
    targets: rule.nodes.slice(0, 10).map((node) => node.target),
  };
}

async function reviewIncompleteItems(page, axeResult) {
  const incomplete = axeResult.incomplete.map((rule) => ({
    id: rule.id,
    impact: rule.impact || '',
    help: rule.help,
    targets: rule.nodes.slice(0, 10).map((node) => node.target),
  }));

  return await page.evaluate((items) => {
    const white = { r: 255, g: 255, b: 255, a: 1 };

    function clamp(value, min, max) {
      return Math.min(max, Math.max(min, value));
    }

    function parseRgb(value) {
      const match = String(value).match(/rgba?\(([^)]+)\)/i);
      if (!match) {
        return null;
      }
      const parts = match[1].split(/[\s,\/]+/).filter(Boolean);
      if (parts.length < 3) {
        return null;
      }
      const channel = (part) => {
        if (part.endsWith('%')) {
          return clamp((Number.parseFloat(part) / 100) * 255, 0, 255);
        }
        return clamp(Number.parseFloat(part), 0, 255);
      };
      return {
        r: channel(parts[0]),
        g: channel(parts[1]),
        b: channel(parts[2]),
        a: parts[3] === undefined ? 1 : clamp(Number.parseFloat(parts[3]), 0, 1),
      };
    }

    function parseOklch(value) {
      const match = String(value).match(/oklch\(([^)]+)\)/i);
      if (!match) {
        return null;
      }
      const parts = match[1].split(/[\s,\/]+/).filter(Boolean);
      if (parts.length < 3) {
        return null;
      }
      const l = parts[0].endsWith('%') ? Number.parseFloat(parts[0]) / 100 : Number.parseFloat(parts[0]);
      const c = Number.parseFloat(parts[1]);
      const h = Number.parseFloat(parts[2]) * (Math.PI / 180);
      const a = c * Math.cos(h);
      const b = c * Math.sin(h);
      const lPrime = l + 0.3963377774 * a + 0.2158037573 * b;
      const mPrime = l - 0.1055613458 * a - 0.0638541728 * b;
      const sPrime = l - 0.0894841775 * a - 1.2914855480 * b;
      const l3 = lPrime ** 3;
      const m3 = mPrime ** 3;
      const s3 = sPrime ** 3;
      const linearRgb = {
        r: 4.0767416621 * l3 - 3.3077115913 * m3 + 0.2309699292 * s3,
        g: -1.2684380046 * l3 + 2.6097574011 * m3 - 0.3413193965 * s3,
        b: -0.0041960863 * l3 - 0.7034186147 * m3 + 1.7076147010 * s3,
      };
      const gamma = (channel) => {
        const clamped = clamp(channel, 0, 1);
        if (clamped <= 0.0031308) {
          return clamped * 12.92 * 255;
        }
        return (1.055 * (clamped ** (1 / 2.4)) - 0.055) * 255;
      };
      return {
        r: gamma(linearRgb.r),
        g: gamma(linearRgb.g),
        b: gamma(linearRgb.b),
        a: parts[3] === undefined ? 1 : clamp(Number.parseFloat(parts[3]), 0, 1),
      };
    }

    function parseColor(value) {
      if (!value || value === 'transparent') {
        return { r: 0, g: 0, b: 0, a: 0 };
      }
      return parseRgb(value) || parseOklch(value);
    }

    function composite(foreground, background) {
      const alpha = foreground.a + background.a * (1 - foreground.a);
      if (alpha === 0) {
        return { r: 0, g: 0, b: 0, a: 0 };
      }
      return {
        r: (foreground.r * foreground.a + background.r * background.a * (1 - foreground.a)) / alpha,
        g: (foreground.g * foreground.a + background.g * background.a * (1 - foreground.a)) / alpha,
        b: (foreground.b * foreground.a + background.b * background.a * (1 - foreground.a)) / alpha,
        a: alpha,
      };
    }

    function relativeLuminance(color) {
      const channel = (value) => {
        const normalized = value / 255;
        return normalized <= 0.03928 ? normalized / 12.92 : ((normalized + 0.055) / 1.055) ** 2.4;
      };
      return 0.2126 * channel(color.r) + 0.7152 * channel(color.g) + 0.0722 * channel(color.b);
    }

    function contrastRatio(foreground, background) {
      const l1 = relativeLuminance(foreground);
      const l2 = relativeLuminance(background);
      const lighter = Math.max(l1, l2);
      const darker = Math.min(l1, l2);
      return (lighter + 0.05) / (darker + 0.05);
    }

    function elementLabel(element) {
      return [
        element.tagName.toLowerCase(),
        element.id ? `#${element.id}` : '',
        element.className && typeof element.className === 'string' ? `.${element.className.trim().split(/\s+/).slice(0, 3).join('.')}` : '',
      ].filter(Boolean).join('');
    }

    function effectiveBackground(element) {
      const layers = [];
      let hasBackgroundImage = false;
      let current = element;
      while (current && current.nodeType === Node.ELEMENT_NODE) {
        const styles = getComputedStyle(current);
        const background = parseColor(styles.backgroundColor);
        if (styles.backgroundImage && styles.backgroundImage !== 'none') {
          hasBackgroundImage = true;
        }
        if (background && background.a > 0) {
          layers.push({ color: background, source: elementLabel(current) });
        }
        current = current.parentElement;
      }
      let composed = white;
      let source = 'viewport fallback';
      for (let i = layers.length - 1; i >= 0; i--) {
        composed = composite(layers[i].color, composed);
        source = layers[i].source;
      }
      return { color: composed, source, hasBackgroundImage };
    }

    function isLargeText(styles) {
      const fontSize = Number.parseFloat(styles.fontSize || '0');
      const weight = Number.parseInt(styles.fontWeight || '400', 10);
      return fontSize >= 24 || (fontSize >= 18.66 && weight >= 700);
    }

    const checks = [];
    for (const item of items.filter((entry) => entry.id === 'color-contrast')) {
      for (const target of item.targets) {
        const selector = Array.isArray(target) ? target[0] : target;
        const element = selector ? document.querySelector(selector) : null;
        if (!element) {
          checks.push({
            rule: item.id,
            target,
            status: 'needs-review',
            reason: 'Target selector was not found in the rendered document.',
          });
          continue;
        }
        const styles = getComputedStyle(element);
        const foreground = parseColor(styles.color);
        const background = effectiveBackground(element);
        if (!foreground || !background.color) {
          checks.push({
            rule: item.id,
            target,
            status: 'needs-review',
            reason: 'Could not parse computed foreground or background color.',
          });
          continue;
        }
        const ratio = contrastRatio(foreground, background.color);
        const threshold = isLargeText(styles) ? 3 : 4.5;
        checks.push({
          rule: item.id,
          target,
          status: ratio >= threshold && !background.hasBackgroundImage ? 'pass' : 'needs-review',
          ratio: Number(ratio.toFixed(2)),
          threshold,
          foreground: styles.color,
          background: styles.backgroundColor,
          effectiveBackgroundSource: background.source,
          hasBackgroundImage: background.hasBackgroundImage,
          text: (element.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 100),
        });
      }
    }
    return checks;
  }, incomplete);
}

async function structuralChecks(page, expectedUrl) {
  return await page.evaluate((url) => {
    const headingLevel = (heading) => Number(heading.tagName.slice(1));
    const headings = Array.from(document.querySelectorAll('main h1, main h2, main h3, main h4, main h5, main h6'))
      .map((heading) => ({ level: headingLevel(heading), tag: heading.tagName.toLowerCase(), text: heading.textContent.trim() }));
    const jumps = [];
    for (let i = 1; i < headings.length; i++) {
      if (headings[i].level > headings[i - 1].level + 1) {
        jumps.push({ from: headings[i - 1], to: headings[i] });
      }
    }
    const images = Array.from(document.images).map((image) => ({
      src: image.currentSrc || image.src,
      alt: image.getAttribute('alt'),
      width: image.getAttribute('width') || String(image.width || ''),
      height: image.getAttribute('height') || String(image.height || ''),
    }));
    const skipLinks = Array.from(document.querySelectorAll('a[href^="#"]'))
      .filter((link) => /skip|content|inhalt|hauptinhalt/i.test(link.textContent || link.getAttribute('aria-label') || ''))
      .map((link) => ({ text: link.textContent.trim(), href: link.getAttribute('href') }));
    const viewport = document.querySelector('meta[name="viewport"]')?.content || '';
    const footerLinks = Array.from(document.querySelectorAll('footer a')).map((link) => ({
      text: link.textContent.trim(),
      href: link.getAttribute('href') || '',
    }));
    const documentLinks = Array.from(document.querySelectorAll('a[href]'))
      .filter((link) => /\.(pdf|docx?|xlsx?|pptx?)(?:[?#].*)?$/i.test(link.getAttribute('href') || ''))
      .map((link) => ({ text: link.textContent.trim().slice(0, 120), href: link.getAttribute('href') || '' }));
    const embeds = Array.from(document.querySelectorAll('iframe, embed, object'))
      .map((element) => ({ tag: element.tagName.toLowerCase(), title: element.getAttribute('title') || '', src: element.getAttribute('src') || element.getAttribute('data') || '' }));
    const media = Array.from(document.querySelectorAll('video, audio'))
      .map((element) => ({ tag: element.tagName.toLowerCase(), controls: element.hasAttribute('controls'), src: element.currentSrc || element.getAttribute('src') || '' }));
    const focusable = Array.from(document.querySelectorAll('a[href], button, input, select, textarea, summary, [tabindex]:not([tabindex="-1"])'))
      .filter((element) => !element.disabled && element.offsetParent !== null)
      .map((element) => {
        const styles = getComputedStyle(element);
        const tag = element.tagName.toLowerCase();
        const isInlineTextLink = tag === 'a'
          && styles.display === 'inline'
          && !!element.closest('p, li, dd, dt, figcaption, blockquote');
        return {
          tag,
          text: (element.textContent || element.getAttribute('aria-label') || element.getAttribute('title') || '').trim().slice(0, 120),
          href: element.getAttribute('href') || '',
          width: Math.round(element.getBoundingClientRect().width),
          height: Math.round(element.getBoundingClientRect().height),
          isInlineTextLink,
        };
      });
    const smallTargets = focusable.filter((element) => element.width < 24 || element.height < 24);
    return {
      url,
      actualUrl: location.href,
      lang: document.documentElement.getAttribute('lang') || '',
      title: document.title,
      hasMain: !!document.querySelector('main'),
      hasHeader: !!document.querySelector('header'),
      hasFooter: !!document.querySelector('footer'),
      h1Count: document.querySelectorAll('main h1').length,
      headings,
      headingJumps: jumps,
      imagesMissingAlt: images.filter((image) => image.alt === null).length,
      imagesMissingDimensions: images.filter((image) => !image.width || !image.height).length,
      skipLinks,
      viewportUserScalableNo: /user-scalable\s*=\s*no/i.test(viewport),
      footerLinks,
      focusableCount: focusable.length,
      smallTargets: smallTargets.filter((element) => !element.isInlineTextLink).slice(0, 20),
      smallTargetInlineTextExceptions: smallTargets.filter((element) => element.isInlineTextLink).slice(0, 20),
      documentsAndEmbeds: {
        documentLinks,
        embeds,
        media,
      },
    };
  }, expectedUrl);
}

async function keyboardProbe(page, maxTabs = 40) {
  const seen = [];
  await page.evaluate(() => {
    if (document.activeElement && document.activeElement instanceof HTMLElement) {
      document.activeElement.blur();
    }
    document.body.focus();
  });
  for (let i = 0; i < maxTabs; i++) {
    await page.keyboard.press('Tab');
    const entry = await page.evaluate(() => {
      const element = document.activeElement;
      if (!element || element === document.body) {
        return { key: 'body', outline: '', boxShadow: '' };
      }
      const styles = getComputedStyle(element);
      return {
        key: [
          element.tagName.toLowerCase(),
          element.id ? `#${element.id}` : '',
          element.getAttribute('href') ? `[href="${element.getAttribute('href')}"]` : '',
          element.getAttribute('aria-label') ? `[aria-label="${element.getAttribute('aria-label')}"]` : '',
          (element.textContent || '').trim().slice(0, 60),
        ].filter(Boolean).join(''),
        outline: styles.outlineStyle === 'none' ? '' : `${styles.outlineWidth} ${styles.outlineStyle} ${styles.outlineColor}`,
        boxShadow: styles.boxShadow === 'none' ? '' : styles.boxShadow,
      };
    });
    if (entry.key === 'body') {
      break;
    }
    seen.push(entry);
    if (seen.length > 1 && seen[seen.length - 1].key === seen[0].key) {
      break;
    }
  }
  return {
    visited: seen.length,
    order: seen,
    elementsWithoutVisibleIndicator: seen.filter((entry) => !entry.outline && !entry.boxShadow).slice(0, 20),
  };
}

function markdownReport(results) {
  const lines = ['# WCAG 2.2 Audit Starter Report', ''];
  lines.push('This report combines automated axe-core checks with deterministic DOM checks. It is not a complete human conformance claim.');
  lines.push('');
  for (const result of results) {
    const unresolvedIncomplete = result.axe.incomplete.filter((item) => {
      const reviews = result.reviewedIncomplete.filter((review) => review.rule === item.id);
      return reviews.length === 0 || reviews.some((review) => review.status !== 'pass');
    });
    lines.push(`## ${result.name || result.url}`);
    lines.push('');
    lines.push(`- URL: ${result.url}`);
    lines.push(`- HTTP status: ${result.status}`);
    lines.push(`- Viewport: ${result.viewport.width}x${result.viewport.height}`);
    lines.push(`- axe-core: ${result.axe.axeVersion}`);
    lines.push(`- Violations: ${result.axe.violations.length}`);
    lines.push(`- Incomplete: ${result.axe.incomplete.length}`);
    lines.push(`- Incomplete unresolved after agent review: ${unresolvedIncomplete.length}`);
    lines.push(`- Passed rule groups: ${result.axe.passes}`);
    lines.push(`- H1 count: ${result.structural.h1Count}`);
    lines.push(`- Lang: ${result.structural.lang}`);
    lines.push(`- Skip links: ${result.structural.skipLinks.length}`);
    lines.push(`- Images missing alt: ${result.structural.imagesMissingAlt}`);
    lines.push(`- Images missing dimensions: ${result.structural.imagesMissingDimensions}`);
    lines.push(`- Small target candidates: ${result.structural.smallTargets.length}`);
    lines.push(`- Small target inline-text exceptions: ${result.structural.smallTargetInlineTextExceptions.length}`);
    lines.push(`- Document links: ${result.structural.documentsAndEmbeds.documentLinks.length}`);
    lines.push(`- Embeds: ${result.structural.documentsAndEmbeds.embeds.length}`);
    lines.push(`- Audio/video elements: ${result.structural.documentsAndEmbeds.media.length}`);
    lines.push('');
    if (result.axe.violations.length > 0) {
      lines.push('### Automated Violations');
      for (const violation of result.axe.violations) {
        lines.push(`- ${violation.id} (${violation.impact}): ${violation.help}; nodes: ${violation.nodes}; targets: ${JSON.stringify(violation.targets)}`);
      }
      lines.push('');
    }
    if (unresolvedIncomplete.length > 0) {
      lines.push('### Needs Agent Review');
      for (const item of unresolvedIncomplete) {
        lines.push(`- ${item.id} (${item.impact}): ${item.help}; nodes: ${item.nodes}; targets: ${JSON.stringify(item.targets)}`);
      }
      lines.push('');
    }
    if (result.reviewedIncomplete.length > 0) {
      lines.push('### Agent-Reviewed Incomplete Items');
      for (const item of result.reviewedIncomplete) {
        if (item.status === 'pass') {
          lines.push(`- ${item.rule}: computed contrast ${item.ratio}:1 passes ${item.threshold}:1 for ${JSON.stringify(item.target)}; text: "${item.text}"`);
        } else if (item.ratio) {
          lines.push(`- ${item.rule}: computed contrast ${item.ratio}:1 needs review for ${JSON.stringify(item.target)}; threshold ${item.threshold}:1; text: "${item.text}"`);
        } else {
          lines.push(`- ${item.rule}: needs review for ${JSON.stringify(item.target)}; ${item.reason}`);
        }
      }
      lines.push('');
    }
    if (result.keyboard) {
      lines.push('### Keyboard Probe');
      lines.push(`- Tab stops visited: ${result.keyboard.visited}`);
      lines.push(`- Possible missing visible indicators: ${result.keyboard.elementsWithoutVisibleIndicator.length}`);
      for (const item of result.keyboard.elementsWithoutVisibleIndicator.slice(0, 10)) {
        lines.push(`  - ${item.key}`);
      }
      lines.push('');
    }
  }
  const unresolvedSmallTargets = results.reduce((sum, result) => sum + result.structural.smallTargets.length, 0);
  const documentLinks = results.reduce((sum, result) => sum + result.structural.documentsAndEmbeds.documentLinks.length, 0);
  const embeds = results.reduce((sum, result) => sum + result.structural.documentsAndEmbeds.embeds.length, 0);
  const media = results.reduce((sum, result) => sum + result.structural.documentsAndEmbeds.media.length, 0);
  lines.push('## Human/User Follow-up Only');
  lines.push('');
  lines.push('- Run screen reader review with the actual target assistive technology and browser combination.');
  lines.push('- Confirm focus order and focus not obscured on the user-supported devices and breakpoints.');
  if (unresolvedSmallTargets > 0) {
    lines.push('- Confirm pointer/touch target exceptions where unresolved targets are below 24x24 CSS px.');
  }
  if (documentLinks > 0 || embeds > 0 || media > 0) {
    lines.push('- Review detected video captions, audio transcripts, PDFs, office documents, and third-party embeds.');
  }
  lines.push('- Confirm legal scope, enforcement contact, organization identity, and publication date before making a conformance statement.');
  lines.push('');
  return lines.join('\n');
}

async function main() {
  const args = parseArgs(process.argv);
  const { chromium } = loadDependency('playwright');
  const axePath = require.resolve('axe-core/axe.min.js');
  const axeSource = fs.readFileSync(axePath, 'utf8');
  const browser = await chromium.launch({
    channel: 'chrome',
    headless: true,
    args: ['--ignore-certificate-errors', '--disable-background-networking', '--disable-component-update', '--disable-sync', '--no-first-run'],
  });
  const results = [];
  try {
    for (const url of args.urls) {
      const page = await browser.newPage({ ignoreHTTPSErrors: true, viewport: args.viewport });
      const response = await page.goto(url, { waitUntil: 'load', timeout: 30000 });
      await page.addScriptTag({ content: axeSource });
      const axeResult = await page.evaluate(async (tags) => {
        return await window.axe.run(document, {
          runOnly: { type: 'tag', values: tags },
          resultTypes: ['violations', 'incomplete', 'inapplicable', 'passes'],
        });
      }, axeTags());
      const reviewedIncomplete = await reviewIncompleteItems(page, axeResult);
      const structural = await structuralChecks(page, url);
      const keyboard = args.keyboard ? await keyboardProbe(page) : null;
      results.push({
        url,
        status: response ? response.status() : 0,
        viewport: args.viewport,
        axe: summarizeAxeResult(axeResult),
        reviewedIncomplete,
        structural,
        keyboard,
      });
      await page.close();
    }
  } finally {
    await browser.close();
  }

  fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
  fs.writeFileSync(args.out, JSON.stringify(results, null, 2));
  if (args.markdown) {
    fs.mkdirSync(path.dirname(path.resolve(args.markdown)), { recursive: true });
    fs.writeFileSync(args.markdown, markdownReport(results));
  }
  console.log(JSON.stringify({
    urls: results.length,
    violations: results.reduce((sum, result) => sum + result.axe.violations.length, 0),
    incomplete: results.reduce((sum, result) => sum + result.axe.incomplete.length, 0),
    reviewedIncomplete: results.reduce((sum, result) => sum + result.reviewedIncomplete.length, 0),
    reviewedIncompleteNeedingReview: results.reduce((sum, result) => sum + result.reviewedIncomplete.filter((item) => item.status !== 'pass').length, 0),
    out: args.out,
    markdown: args.markdown || null,
  }, null, 2));
  if (results.some((result) => result.axe.violations.length > 0 || result.reviewedIncomplete.some((item) => item.status !== 'pass' && item.ratio && item.ratio < item.threshold))) {
    process.exitCode = 2;
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
