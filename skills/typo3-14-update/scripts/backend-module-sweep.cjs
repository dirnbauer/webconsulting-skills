#!/usr/bin/env node
/**
 * TYPO3 backend module sweep
 *
 * Logs into the TYPO3 backend, discovers every module from the rendered
 * module menu, opens each one, and fails when a module renders an error.
 * Used after a TYPO3 update to prove the backend runs all modules without
 * problems.
 *
 * Usage:
 *   node backend-module-sweep.cjs --base-url=https://site.ddev.site \
 *     [--output=backend-module-sweep.json] [--settle=1500] [--timeout=30000]
 *
 * Credentials come from BE_USER / BE_PASSWORD. Process environment wins over
 * the .env / .env.local files loaded from the directory above this script.
 * Use a dedicated local admin account for the sweep; never commit credentials.
 *
 * Selector assumptions (verify against the installed TYPO3 version if the
 * sweep cannot log in or finds zero modules):
 *   - Login form:   input[name="username"], input[type="password"], button[type="submit"]
 *   - Module menu:  [data-modulemenu-identifier] items inside the scaffold
 *   - Content area: iframe named "list_frame"
 */

const { chromium } = require('@playwright/test');
const path = require('path');
const fs = require('fs-extra');
const dotenv = require('dotenv');
const { program } = require('commander');

const ERROR_TEXT_MARKERS = [
    'Oops, an error occurred',
    'Uncaught TYPO3 Exception',
    'Fatal error:',
    'Call to undefined',
    'An exception occurred',
];

function loadEnvironment() {
    const root = path.resolve(__dirname, '..');
    const merged = {};
    for (const filename of ['.env', '.env.local']) {
        const envPath = path.join(root, filename);
        if (fs.existsSync(envPath)) {
            Object.assign(merged, dotenv.parse(fs.readFileSync(envPath)));
        }
    }
    for (const [key, value] of Object.entries(merged)) {
        if (process.env[key] === undefined) {
            process.env[key] = value;
        }
    }
}

/**
 * Playwright's chromium-headless-shell can crash on newer macOS. Mirror the
 * launch strategy of run-tests.cjs: full Chromium with --headless=new on
 * Darwin, plain headless elsewhere. PLAYWRIGHT_CHANNEL overrides.
 */
function getLaunchOptions() {
    const args = ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'];
    const channel = process.env.PLAYWRIGHT_CHANNEL;
    if (channel) {
        return { args, channel, headless: true };
    }
    if (process.platform === 'darwin') {
        return { args: [...args, '--headless=new'], headless: false };
    }
    return { args, headless: true };
}

function contentFrame(page) {
    return page.frames().find((f) => f.name() === 'list_frame') || null;
}

async function login(page, baseUrl, timeout) {
    const user = process.env.BE_USER;
    const password = process.env.BE_PASSWORD;
    if (!user || !password) {
        throw new Error('BE_USER and BE_PASSWORD must be set (environment or .env one level above this script).');
    }
    await page.goto(`${baseUrl.replace(/\/+$/, '')}/typo3/`, { waitUntil: 'domcontentloaded', timeout });
    await page.fill('input[name="username"]', user, { timeout });
    await page.fill('input[type="password"]', password, { timeout });
    await page.click('button[type="submit"]', { timeout });
    try {
        await page.waitForSelector('[data-modulemenu-identifier]', { timeout });
    } catch {
        throw new Error('Login failed or module menu not found — check BE_USER/BE_PASSWORD and the selector assumptions in this script header.');
    }
}

async function sweepModule(page, identifier, settle) {
    const selector = `[data-modulemenu-identifier="${identifier}"]`;
    const before = contentFrame(page)?.url() ?? '';
    const consoleErrors = [];
    const serverErrors = [];

    const onConsole = (msg) => {
        if (msg.type() === 'error') {
            consoleErrors.push(msg.text().slice(0, 300));
        }
    };
    const onResponse = (response) => {
        if (response.status() >= 500) {
            serverErrors.push(`${response.status()} ${response.url().slice(0, 200)}`);
        }
    };
    page.on('console', onConsole);
    page.on('response', onResponse);

    const result = { identifier, status: 'ok', reasons: [] };
    try {
        try {
            await page.locator(selector).first().click({ timeout: 5000 });
        } catch {
            result.status = 'skipped';
            result.reasons.push('menu item not clickable (hidden or collapsed group)');
            return result;
        }
        await page.waitForTimeout(settle);

        const frame = contentFrame(page);
        const after = frame?.url() ?? '';
        if (!frame || after === before) {
            result.status = 'skipped';
            result.reasons.push('no content-frame navigation (module group, not a module)');
            return result;
        }

        const title = await frame.title().catch(() => '');
        const bodyText = await frame
            .evaluate(() => (document.body ? document.body.innerText.slice(0, 5000) : ''))
            .catch(() => '');

        if (/exception/i.test(title)) {
            result.reasons.push(`exception page title: ${title.slice(0, 120)}`);
        }
        for (const marker of ERROR_TEXT_MARKERS) {
            if (bodyText.includes(marker)) {
                result.reasons.push(`error marker in module output: "${marker}"`);
            }
        }
        if (serverErrors.length > 0) {
            result.reasons.push(...serverErrors.map((e) => `server error: ${e}`));
        }
        if (consoleErrors.length > 0) {
            result.reasons.push(...consoleErrors.map((e) => `console error: ${e}`));
        }
        if (result.reasons.length > 0) {
            result.status = 'fail';
        }
        result.url = after.slice(0, 250);
        return result;
    } finally {
        page.off('console', onConsole);
        page.off('response', onResponse);
    }
}

async function main() {
    loadEnvironment();
    program
        .requiredOption('--base-url <baseUrl>', 'DDEV base URL, e.g. https://site.ddev.site')
        .option('--output <output>', 'JSON report path', 'backend-module-sweep.json')
        .option('--settle <ms>', 'wait after opening a module', '1500')
        .option('--timeout <ms>', 'navigation/login timeout', '30000')
        .parse(process.argv);
    const options = program.opts();
    const settle = Number.parseInt(options.settle, 10);
    const timeout = Number.parseInt(options.timeout, 10);

    const browser = await chromium.launch(getLaunchOptions());
    const page = await browser.newPage({ ignoreHTTPSErrors: true, viewport: { width: 1920, height: 1080 } });

    const report = {
        baseUrl: options.baseUrl,
        generatedAt: new Date().toISOString(),
        modules: [],
    };

    try {
        await login(page, options.baseUrl, timeout);

        const identifiers = [...new Set(
            await page.$$eval('[data-modulemenu-identifier]', (els) =>
                els.map((el) => el.getAttribute('data-modulemenu-identifier')).filter(Boolean)
            )
        )];
        if (identifiers.length === 0) {
            throw new Error('No backend modules found in the module menu — verify the selector assumptions in this script header.');
        }

        for (const identifier of identifiers) {
            const result = await sweepModule(page, identifier, settle);
            report.modules.push(result);
            const flag = result.status === 'ok' ? 'OK  ' : result.status === 'fail' ? 'FAIL' : 'SKIP';
            console.log(`[${flag}] ${identifier}${result.reasons.length ? ' — ' + result.reasons[0] : ''}`);
        }
    } finally {
        await browser.close();
    }

    report.total = report.modules.length;
    report.ok = report.modules.filter((m) => m.status === 'ok').length;
    report.failed = report.modules.filter((m) => m.status === 'fail').length;
    report.skipped = report.modules.filter((m) => m.status === 'skipped').length;

    await fs.outputJson(options.output, report, { spaces: 2 });
    console.log(`\n${report.ok}/${report.total} modules OK, ${report.failed} failed, ${report.skipped} skipped — report: ${options.output}`);

    if (report.failed > 0) {
        process.exitCode = 1;
    }
}

main().catch((error) => {
    console.error(`Backend module sweep aborted: ${error.message}`);
    process.exitCode = 2;
});
