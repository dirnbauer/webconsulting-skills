import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import { loadConfig, resolveUrl, safeFileName } from './helpers/config.js';
import { loadUrlInventory } from './helpers/inventory.js';
import { dismissCookieBanner, runDynamicStateScans, keyboardSmoke, reflowCheck, targetSizeCheck, focusStyleSmoke } from './helpers/browser-checks.js';
import { enrichAxeResult } from './helpers/typo3-map.js';

const config = await loadConfig('.a11y/a11y.config.yml');
const inventory = await loadUrlInventory(config);
const reportOnly = process.env.A11Y_REPORT_ONLY === '1' || process.env.A11Y_REPORT_ONLY === 'true';
const axeTags = config.axe?.tags?.length ? config.axe.tags : ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
const failImpacts = new Set(config.axe?.failImpacts || ['critical', 'serious']);
const rawDir = path.resolve('.a11y/raw');
await fs.mkdir(rawDir, { recursive: true });

function blockingViolations(result) {
  return (result.violations || []).filter(v => failImpacts.has(v.impact || ''));
}

async function scanPage(page, url, stateName, testInfo) {
  let builder = new AxeBuilder({ page }).withTags(axeTags);

  for (const selector of config.axe?.excludedSelectors || []) {
    builder = builder.exclude(selector);
  }
  if (config.axe?.disabledRules?.length) {
    builder = builder.disableRules(config.axe.disabledRules);
  }

  const result = await builder.analyze();
  const enriched = await enrichAxeResult(page, result, config, stateName);
  const file = path.join(rawDir, `${safeFileName(url)}--${safeFileName(stateName)}.json`);
  await fs.writeFile(file, JSON.stringify({ url, stateName, result: enriched }, null, 2));
  await testInfo.attach(`axe-${stateName}`, { path: file, contentType: 'application/json' });
  return enriched;
}

for (const item of inventory) {
  const url = typeof item === 'string' ? item : item.url;
  test(`WCAG 2.2 AA automated scan: ${url}`, async ({ page }, testInfo) => {
    const fullUrl = resolveUrl(config.site.baseUrl, url);
    await page.goto(fullUrl, { waitUntil: config.browser?.waitUntil || 'networkidle' });

    if (config.browser?.waitForSelector) {
      await page.locator(config.browser.waitForSelector).first().waitFor({ timeout: 15_000 }).catch(() => {});
    }

    await dismissCookieBanner(page, config);

    const defaultResult = await scanPage(page, url, 'default', testInfo);
    const dynamicResults = await runDynamicStateScans(page, config, async (stateName) => scanPage(page, url, stateName, testInfo));
    const keyboard = await keyboardSmoke(page, config);
    const reflow = await reflowCheck(page, config);
    const targetSize = await targetSizeCheck(page, config);
    const focusStyle = await focusStyleSmoke(page, config);

    const customFile = path.join(rawDir, `${safeFileName(url)}--custom-checks.json`);
    await fs.writeFile(customFile, JSON.stringify({ url, keyboard, reflow, targetSize, focusStyle }, null, 2));
    await testInfo.attach('custom-checks', { path: customFile, contentType: 'application/json' });

    const allBlocking = [defaultResult, ...dynamicResults].flatMap(blockingViolations);
    const customBlocking = [];
    if (reflow?.hasHorizontalOverflow) customBlocking.push({ id: 'custom-reflow-horizontal-overflow', impact: 'serious', message: reflow.message });

    if (!reportOnly) {
      expect([...allBlocking, ...customBlocking], 'blocking accessibility findings').toEqual([]);
    }
  });
}
