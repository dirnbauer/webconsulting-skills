export async function enrichAxeResult(page, result, config, stateName = 'default') {
  const componentAttr = config.typo3?.debugMarkers?.componentAttribute || 'data-a11y-component';
  const templateAttr = config.typo3?.debugMarkers?.templateAttribute || 'data-a11y-template';
  const clone = JSON.parse(JSON.stringify(result));
  clone.stateName = stateName;

  for (const violation of clone.violations || []) {
    for (const node of violation.nodes || []) {
      const selector = Array.isArray(node.target) ? node.target.join(', ') : String(node.target || '');
      node.typo3 = await mapSelector(page, selector, componentAttr, templateAttr);
    }
  }
  return clone;
}

async function mapSelector(page, selector, componentAttr, templateAttr) {
  if (!selector) return null;
  try {
    return await page.evaluate(({ selector, componentAttr, templateAttr }) => {
      const el = document.querySelector(selector);
      if (!el) return null;
      const marker = el.closest(`[${componentAttr}], [${templateAttr}]`);
      if (!marker) return null;
      return {
        component: marker.getAttribute(componentAttr) || '',
        template: marker.getAttribute(templateAttr) || '',
        markerTag: marker.tagName.toLowerCase()
      };
    }, { selector, componentAttr, templateAttr });
  } catch {
    return null;
  }
}
