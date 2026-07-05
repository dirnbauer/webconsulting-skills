import fs from 'node:fs/promises';
import path from 'node:path';
import YAML from 'yaml';

export async function loadConfig(configPath = '.a11y/a11y.config.yml') {
  let source;
  try {
    source = await fs.readFile(configPath, 'utf8');
  } catch (error) {
    if (error.code === 'ENOENT') {
      source = await fs.readFile('.a11y/a11y.config.example.yml', 'utf8');
    } else {
      throw error;
    }
  }
  const config = YAML.parse(source) || {};
  if (process.env.A11Y_BASE_URL) {
    config.site = config.site || {};
    config.site.baseUrl = process.env.A11Y_BASE_URL;
  }
  if (!config.site?.baseUrl) {
    throw new Error('Missing site.baseUrl in .a11y/a11y.config.yml or A11Y_BASE_URL env var.');
  }
  return config;
}

export function resolveUrl(baseUrl, maybeRelative) {
  return new URL(maybeRelative, baseUrl).toString();
}

export function safeFileName(input) {
  return String(input || 'root')
    .replace(/^https?:\/\//, '')
    .replace(/[^a-zA-Z0-9._-]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 160) || 'root';
}

export async function pathExists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

export async function readJson(p, fallback = null) {
  try {
    return JSON.parse(await fs.readFile(p, 'utf8'));
  } catch (error) {
    if (error.code === 'ENOENT') return fallback;
    throw error;
  }
}
