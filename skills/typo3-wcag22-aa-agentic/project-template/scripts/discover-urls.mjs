#!/usr/bin/env node
import fs from 'node:fs/promises';
import { XMLParser } from 'fast-xml-parser';
import { loadConfig, resolveUrl } from '../tests/helpers/config.js';

const args = parseArgs(process.argv.slice(2));
const config = await loadConfig(args.config || '.a11y/a11y.config.yml');
const maxPages = Number(config.crawler?.maxPages || 80);
const excludes = (config.crawler?.exclude || []).map(pattern => new RegExp(pattern));
const urls = new Set();

for (const item of config.crawler?.include || []) {
  const normalized = normalizeUrl(item, config.site.baseUrl);
  if (normalized && !isExcluded(normalized)) urls.add(normalized);
}

if (config.site?.sitemapUrl) {
  await collectFromSitemap(config.site.sitemapUrl);
}

if (!urls.size) urls.add('/');

const sorted = [...urls]
  .filter(Boolean)
  .sort((a, b) => score(a, config) - score(b, config) || a.localeCompare(b))
  .slice(0, maxPages);

await fs.mkdir('.a11y', { recursive: true });
await fs.writeFile('.a11y/url-inventory.json', JSON.stringify({ generatedAt: new Date().toISOString(), baseUrl: config.site.baseUrl, urls: sorted }, null, 2));
console.log(`Discovered ${sorted.length} URLs -> .a11y/url-inventory.json`);

async function collectFromSitemap(sitemapUrl, depth = 0) {
  if (depth > 3 || urls.size >= maxPages * 3) return;
  try {
    const response = await fetch(sitemapUrl, { redirect: 'follow' });
    if (!response.ok) throw new Error(`${response.status} ${response.statusText}`);
    const xml = await response.text();
    const parsed = new XMLParser({ ignoreAttributes: false }).parse(xml);

    const sitemapEntries = arrayify(parsed?.sitemapindex?.sitemap);
    for (const entry of sitemapEntries) {
      if (entry?.loc) await collectFromSitemap(entry.loc, depth + 1);
    }

    const urlEntries = arrayify(parsed?.urlset?.url);
    for (const entry of urlEntries) {
      const normalized = normalizeUrl(entry?.loc, config.site.baseUrl);
      if (normalized && !isExcluded(normalized)) urls.add(normalized);
      if (urls.size >= maxPages * 3) break;
    }
  } catch (error) {
    console.warn(`Could not read sitemap ${sitemapUrl}: ${error.message}`);
  }
}

function arrayify(value) {
  if (!value) return [];
  return Array.isArray(value) ? value : [value];
}

function normalizeUrl(input, baseUrl) {
  if (!input) return null;
  try {
    const u = new URL(input, baseUrl);
    const base = new URL(baseUrl);
    if (u.host !== base.host) return null;
    let pathname = u.pathname || '/';
    if (!pathname.endsWith('/') && !/\.[a-z0-9]{2,5}$/i.test(pathname)) pathname += '/';
    return `${pathname}${u.search || ''}`;
  } catch {
    return null;
  }
}

function isExcluded(url) {
  return excludes.some(re => re.test(url));
}

function score(url, config) {
  if (url === '/') return 0;
  const patterns = config.crawler?.samplePatterns || {};
  let i = 1;
  for (const group of Object.values(patterns)) {
    for (const pattern of group || []) {
      try {
        if (new RegExp(pattern).test(url)) return i;
      } catch {}
    }
    i++;
  }
  return 50 + url.length / 1000;
}

function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--config') result.config = argv[++i];
  }
  return result;
}
