function isLocatorError(error) {
  return error && /strict mode|Timeout|not visible|not attached|Target closed/i.test(String(error.message || error));
}

export async function dismissCookieBanner(page, config) {
  for (const selector of config.browser?.cookieBannerDismissSelectors || []) {
    try {
      const locator = page.locator(selector).first();
      if (await locator.isVisible({ timeout: 1000 })) {
        await locator.click({ timeout: 2000 });
        await page.waitForTimeout(300);
        return { dismissedWith: selector };
      }
    } catch (error) {
      if (!isLocatorError(error)) throw error;
    }
  }
  return { dismissedWith: null };
}

export async function runDynamicStateScans(page, config, scanCallback) {
  const max = Number(config.browser?.maxDynamicActionsPerPage || 10);
  const results = [];
  const candidates = [
    'button[aria-expanded="false"]',
    '[role="button"][aria-expanded="false"]',
    'summary',
    '[data-bs-toggle="collapse"]',
    '[data-bs-toggle="dropdown"]',
    '[data-bs-toggle="modal"]',
    '.accordion-button.collapsed',
    '.navbar-toggler'
  ];

  let actionIndex = 0;
  for (const selector of candidates) {
    const count = await page.locator(selector).count().catch(() => 0);
    for (let i = 0; i < Math.min(count, max - actionIndex); i++) {
      try {
        const locator = page.locator(selector).nth(i);
        if (!(await locator.isVisible({ timeout: 1000 }))) continue;
        await locator.scrollIntoViewIfNeeded({ timeout: 1000 }).catch(() => {});
        await locator.click({ timeout: 3000 });
        await page.waitForTimeout(350);
        results.push(await scanCallback(`state-${actionIndex + 1}-${slug(selector)}`));
        actionIndex++;
        if (actionIndex >= max) return results;
      } catch (error) {
        if (!isLocatorError(error)) {
          results.push({ violations: [], customError: String(error.message || error), stateName: `state-error-${actionIndex + 1}` });
        }
      }
    }
  }
  return results;
}

export async function keyboardSmoke(page, config) {
  const steps = [];
  const seen = new Set();
  for (let i = 0; i < 35; i++) {
    await page.keyboard.press('Tab');
    const active = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el) return null;
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);
      return {
        tag: el.tagName.toLowerCase(),
        id: el.id || '',
        className: typeof el.className === 'string' ? el.className : '',
        text: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim().slice(0, 80),
        href: el.getAttribute('href') || '',
        role: el.getAttribute('role') || '',
        visible: rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none',
        rect: { x: Math.round(rect.x), y: Math.round(rect.y), width: Math.round(rect.width), height: Math.round(rect.height) }
      };
    });
    if (!active) continue;
    const key = `${active.tag}#${active.id}.${active.className}.${active.text}.${active.href}`;
    if (seen.has(key) && i > 3) break;
    seen.add(key);
    steps.push(active);
  }
  const invisibleFocus = steps.filter(s => !s.visible);
  return { steps, invisibleFocus, needsHumanReview: true };
}

export async function reflowCheck(page, config) {
  const original = page.viewportSize();
  await page.setViewportSize({ width: 320, height: 900 });
  await page.waitForTimeout(250);
  const data = await page.evaluate(() => {
    const doc = document.documentElement;
    return {
      clientWidth: doc.clientWidth,
      scrollWidth: doc.scrollWidth,
      bodyScrollWidth: document.body ? document.body.scrollWidth : null,
      hasHorizontalOverflow: doc.scrollWidth > doc.clientWidth + 2
    };
  });
  if (original) await page.setViewportSize(original);
  return {
    ...data,
    message: data.hasHorizontalOverflow ? `Horizontal overflow at 320px: scrollWidth ${data.scrollWidth}, clientWidth ${data.clientWidth}` : 'No horizontal overflow at 320px.'
  };
}

export async function targetSizeCheck(page, config) {
  const smallTargets = await page.evaluate(() => {
    const selectors = 'a[href], button, input:not([type="hidden"]), select, textarea, [role="button"], [role="link"], [tabindex]:not([tabindex="-1"])';
    return [...document.querySelectorAll(selectors)]
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        const visible = rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none';
        return {
          selector: cssPath(el),
          text: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').trim().slice(0, 80),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          visible
        };
      })
      .filter(item => item.visible && (item.width < 24 || item.height < 24))
      .slice(0, 100);

    function cssPath(el) {
      if (el.id) return `#${CSS.escape(el.id)}`;
      const parts = [];
      while (el && el.nodeType === Node.ELEMENT_NODE && parts.length < 5) {
        let part = el.nodeName.toLowerCase();
        if (el.classList && el.classList.length) part += '.' + [...el.classList].slice(0, 2).map(c => CSS.escape(c)).join('.');
        parts.unshift(part);
        el = el.parentElement;
      }
      return parts.join(' > ');
    }
  });
  return { smallTargets, needsHumanReview: smallTargets.length > 0 };
}

export async function focusStyleSmoke(page, config) {
  const issues = [];
  await page.keyboard.press('Home').catch(() => {});
  for (let i = 0; i < 20; i++) {
    await page.keyboard.press('Tab');
    const item = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body) return null;
      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      const hasOutline = style.outlineStyle !== 'none' && parseFloat(style.outlineWidth || '0') > 0;
      const hasBoxShadow = style.boxShadow && style.boxShadow !== 'none';
      const visible = rect.width > 0 && rect.height > 0;
      return {
        tag: el.tagName.toLowerCase(),
        id: el.id || '',
        className: typeof el.className === 'string' ? el.className : '',
        text: (el.innerText || el.getAttribute('aria-label') || '').trim().slice(0, 80),
        hasOutline,
        hasBoxShadow,
        visible
      };
    });
    if (item && item.visible && !item.hasOutline && !item.hasBoxShadow) issues.push(item);
  }
  return { possibleMissingFocusStyle: issues, needsHumanReview: true };
}

function slug(input) {
  return String(input).replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').slice(0, 60).toLowerCase();
}
