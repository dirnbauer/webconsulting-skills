(() => {
  if (window.__typo3WcagManualHelperLoaded) return;
  window.__typo3WcagManualHelperLoaded = true;

  const state = {
    focusRecording: false,
    focusOrder: [],
  };

  const FOCUSABLE_SELECTOR = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled]):not([type="hidden"])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])',
    '[contenteditable="true"]',
    'summary',
    'audio[controls]',
    'video[controls]',
  ].join(',');

  function text(value, max = 120) {
    return String(value || '').replace(/\s+/g, ' ').trim().slice(0, max);
  }

  function cssPath(el) {
    if (!el || el.nodeType !== 1) return '';
    if (el.id) return `#${CSS.escape(el.id)}`;
    const parts = [];
    let node = el;
    while (node && node.nodeType === 1 && node !== document.body && parts.length < 6) {
      let part = node.localName.toLowerCase();
      if (node.classList.length) part += '.' + [...node.classList].slice(0, 2).map((c) => CSS.escape(c)).join('.');
      const parent = node.parentElement;
      if (parent) {
        const sameTag = [...parent.children].filter((child) => child.localName === node.localName);
        if (sameTag.length > 1) part += `:nth-of-type(${sameTag.indexOf(node) + 1})`;
      }
      parts.unshift(part);
      node = parent;
    }
    return parts.join(' > ');
  }

  function accessibleName(el) {
    if (!el) return '';
    const labelledby = el.getAttribute('aria-labelledby');
    if (labelledby) {
      const label = labelledby.split(/\s+/).map((id) => document.getElementById(id)?.textContent || '').join(' ');
      if (text(label)) return text(label);
    }
    for (const attr of ['aria-label', 'alt', 'title', 'value']) {
      const value = el.getAttribute?.(attr);
      if (text(value)) return text(value);
    }
    if (el.id) {
      const label = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
      if (label && text(label.textContent)) return text(label.textContent);
    }
    const closestLabel = el.closest?.('label');
    if (closestLabel && text(closestLabel.textContent)) return text(closestLabel.textContent);
    return text(el.textContent || '');
  }

  function visible(el) {
    const style = getComputedStyle(el);
    if (style.visibility === 'hidden' || style.display === 'none') return false;
    const rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  }

  function scanPage() {
    const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map((el) => ({
      level: Number(el.tagName.slice(1)),
      text: text(el.textContent),
      selector: cssPath(el),
    }));

    const landmarkSelectors = ['header', 'nav', 'main', 'footer', 'aside', 'form', '[role="banner"]', '[role="navigation"]', '[role="main"]', '[role="contentinfo"]', '[role="complementary"]', '[role="search"]', '[role="region"]'];
    const landmarks = [...new Set(landmarkSelectors.flatMap((sel) => [...document.querySelectorAll(sel)]))].map((el) => ({
      tag: el.localName,
      role: el.getAttribute('role') || null,
      name: accessibleName(el),
      selector: cssPath(el),
    }));

    const imageElements = [...document.images];
    const missingAlt = imageElements.filter((img) => !img.hasAttribute('alt')).map(imageInfo);
    const emptyAlt = imageElements.filter((img) => img.hasAttribute('alt') && img.getAttribute('alt') === '').map(imageInfo);

    const controls = [...document.querySelectorAll('input,select,textarea,button')].filter((el) => el.type !== 'hidden' && visible(el));
    const unlabeled = controls.filter((el) => {
      if (el.localName === 'button') return !accessibleName(el);
      return !accessibleName(el);
    }).map(controlInfo);

    const links = [...document.querySelectorAll('a[href]')].filter(visible);
    const generic = /^(click here|here|more|read more|learn more|mehr|weiter|hier|zum artikel|details|link)$/i;
    const suspectLinks = links.filter((a) => !accessibleName(a) || generic.test(accessibleName(a))).map(linkInfo);

    const focusable = [...document.querySelectorAll(FOCUSABLE_SELECTOR)].filter(visible);
    const smallTargets = focusable.filter((el) => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0 && (r.width < 24 || r.height < 24);
    }).map(targetInfo);

    const ids = [...document.querySelectorAll('[id]')].map((el) => el.id).filter(Boolean);
    const duplicateIds = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];

    const iframes = [...document.querySelectorAll('iframe')];
    const videos = [...document.querySelectorAll('video')];

    return {
      url: location.href,
      title: document.title,
      htmlLang: document.documentElement.getAttribute('lang') || '',
      headings,
      landmarks,
      images: {
        total: imageElements.length,
        missingAlt,
        emptyAlt,
        samples: imageElements.slice(0, 50).map(imageInfo),
      },
      forms: {
        controls: controls.length,
        unlabeled,
      },
      links: {
        total: links.length,
        suspect: suspectLinks,
      },
      focusable: {
        total: focusable.length,
        smallTargets,
      },
      duplicateIds,
      iframes: {
        total: iframes.length,
        missingTitle: iframes.filter((el) => !accessibleName(el)).map((el) => ({ selector: cssPath(el), src: el.src || '' })),
      },
      media: {
        videos: videos.length,
        videosWithoutCaptionTrack: videos.filter((video) => ![...video.querySelectorAll('track')].some((track) => /captions|subtitles/i.test(track.kind))).length,
      },
    };
  }

  function imageInfo(img) {
    return { selector: cssPath(img), alt: img.getAttribute('alt'), src: img.currentSrc || img.src || '', name: accessibleName(img) };
  }

  function controlInfo(el) {
    return { selector: cssPath(el), tag: el.localName, type: el.type || null, name: accessibleName(el) };
  }

  function linkInfo(el) {
    return { selector: cssPath(el), href: el.href, text: text(el.textContent), name: accessibleName(el) };
  }

  function targetInfo(el) {
    const r = el.getBoundingClientRect();
    return { selector: cssPath(el), tag: el.localName, name: accessibleName(el), width: Math.round(r.width), height: Math.round(r.height) };
  }

  function ensureStyle() {
    if (document.getElementById('wcag-manual-helper-style')) return;
    const style = document.createElement('style');
    style.id = 'wcag-manual-helper-style';
    style.textContent = `
      .wcag-manual-helper-highlight { outline: 3px solid #ff3b30 !important; outline-offset: 3px !important; }
      .wcag-manual-helper-highlight-secondary { outline: 3px solid #007aff !important; outline-offset: 3px !important; }
      .wcag-manual-helper-label {
        position: absolute !important;
        z-index: 2147483647 !important;
        max-width: 360px !important;
        padding: 2px 5px !important;
        border-radius: 3px !important;
        background: #111 !important;
        color: #fff !important;
        font: 12px/1.3 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        pointer-events: none !important;
        box-shadow: 0 1px 3px rgba(0,0,0,.35) !important;
      }
      .wcag-manual-helper-focus-ring { outline: 5px solid #ffcc00 !important; outline-offset: 4px !important; }
    `;
    document.documentElement.append(style);
  }

  function clearHighlights() {
    document.querySelectorAll('.wcag-manual-helper-highlight,.wcag-manual-helper-highlight-secondary,.wcag-manual-helper-focus-ring').forEach((el) => {
      el.classList.remove('wcag-manual-helper-highlight', 'wcag-manual-helper-highlight-secondary', 'wcag-manual-helper-focus-ring');
    });
    document.querySelectorAll('.wcag-manual-helper-label').forEach((el) => el.remove());
  }

  function labelElement(el, label, secondary = false) {
    ensureStyle();
    if (!visible(el)) return;
    el.classList.add(secondary ? 'wcag-manual-helper-highlight-secondary' : 'wcag-manual-helper-highlight');
    const rect = el.getBoundingClientRect();
    const tag = document.createElement('div');
    tag.className = 'wcag-manual-helper-label';
    tag.textContent = label;
    tag.style.left = `${Math.max(0, rect.left + scrollX)}px`;
    tag.style.top = `${Math.max(0, rect.top + scrollY - 22)}px`;
    document.body.append(tag);
  }

  function highlight(kind) {
    clearHighlights();
    const scan = scanPage();
    if (kind === 'headings') {
      document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach((el) => labelElement(el, `${el.tagName}: ${text(el.textContent, 60)}`));
    } else if (kind === 'landmarks') {
      const selector = 'header,nav,main,footer,aside,form,[role="banner"],[role="navigation"],[role="main"],[role="contentinfo"],[role="complementary"],[role="search"],[role="region"]';
      document.querySelectorAll(selector).forEach((el) => labelElement(el, `${el.localName}${el.getAttribute('role') ? ' role=' + el.getAttribute('role') : ''} ${accessibleName(el)}`));
    } else if (kind === 'images') {
      document.querySelectorAll('img').forEach((el) => labelElement(el, `img alt=${JSON.stringify(el.getAttribute('alt'))}`));
    } else if (kind === 'forms') {
      document.querySelectorAll('input,select,textarea,button,label,fieldset,legend').forEach((el) => labelElement(el, `${el.localName} ${accessibleName(el)}`, ['label', 'legend'].includes(el.localName)));
    } else if (kind === 'links') {
      document.querySelectorAll('a[href]').forEach((el) => labelElement(el, `link: ${accessibleName(el) || '(no name)'}`));
    } else if (kind === 'focusables') {
      document.querySelectorAll(FOCUSABLE_SELECTOR).forEach((el, index) => labelElement(el, `${index + 1}. ${el.localName}: ${accessibleName(el) || '(no name)'}`));
    } else if (kind === 'small-targets') {
      const selectors = new Set(scan.focusable.smallTargets.map((item) => item.selector));
      document.querySelectorAll(FOCUSABLE_SELECTOR).forEach((el) => {
        if (selectors.has(cssPath(el))) {
          const r = el.getBoundingClientRect();
          labelElement(el, `${Math.round(r.width)}×${Math.round(r.height)} px: ${accessibleName(el) || el.localName}`);
        }
      });
    }
    return { ok: true, kind };
  }

  function onFocusIn(event) {
    if (!state.focusRecording) return;
    const el = event.target;
    document.querySelectorAll('.wcag-manual-helper-focus-ring').forEach((item) => item.classList.remove('wcag-manual-helper-focus-ring'));
    el.classList.add('wcag-manual-helper-focus-ring');
    const record = {
      index: state.focusOrder.length + 1,
      selector: cssPath(el),
      tag: el.localName,
      role: el.getAttribute('role') || null,
      name: accessibleName(el),
      text: text(el.textContent, 80),
      timestamp: new Date().toISOString(),
    };
    state.focusOrder.push(record);
    labelElement(el, `focus ${record.index}: ${record.name || record.tag}`);
  }

  document.addEventListener('focusin', onFocusIn, true);

  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    try {
      if (message.type === 'wcag-helper-scan') sendResponse(scanPage());
      else if (message.type === 'wcag-helper-highlight') sendResponse(highlight(message.kind));
      else if (message.type === 'wcag-helper-clear') { clearHighlights(); sendResponse({ ok: true }); }
      else if (message.type === 'wcag-helper-focus-start') {
        state.focusRecording = true;
        state.focusOrder = [];
        ensureStyle();
        sendResponse({ ok: true });
      } else if (message.type === 'wcag-helper-focus-stop') {
        state.focusRecording = false;
        document.querySelectorAll('.wcag-manual-helper-focus-ring').forEach((item) => item.classList.remove('wcag-manual-helper-focus-ring'));
        sendResponse({ ok: true, focusOrder: state.focusOrder });
      } else if (message.type === 'wcag-helper-focus-get') {
        sendResponse({ ok: true, focusOrder: state.focusOrder });
      }
    } catch (error) {
      sendResponse({ ok: false, error: error.message });
    }
    return true;
  });
})();
