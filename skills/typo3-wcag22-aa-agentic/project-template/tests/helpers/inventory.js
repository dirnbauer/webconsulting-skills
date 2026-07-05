import fs from 'node:fs/promises';

export async function loadUrlInventory(config) {
  const fromFile = await fs.readFile('.a11y/url-inventory.json', 'utf8')
    .then(JSON.parse)
    .catch(() => null);

  const urls = [];
  if (Array.isArray(fromFile?.urls)) urls.push(...fromFile.urls.map(x => typeof x === 'string' ? x : x.url));
  if (Array.isArray(config.crawler?.include)) urls.push(...config.crawler.include);

  const normalized = [...new Set(urls.map(normalizePath).filter(Boolean))];
  if (!normalized.length) normalized.push('/');
  return normalized.slice(0, config.crawler?.maxPages || 80);
}

function normalizePath(url) {
  if (!url) return null;
  try {
    if (/^https?:\/\//.test(url)) return new URL(url).pathname || '/';
  } catch {}
  return url.startsWith('/') ? url : `/${url}`;
}
