# TYPO3 v14 Web Components Checklists

Use this reference for reviews, migrations, and implementation planning.

## Dos

- Use TYPO3 v14 documentation as the source of truth before writing code.
- Prefer existing TYPO3 APIs and components over custom UI primitives.
- Register backend ES modules in `Configuration/JavaScriptModules.php`.
- Load JavaScript with `PageRenderer->loadJavaScriptModule()` or `<f:asset.module identifier="..."/>`.
- Keep custom elements named with a vendor/project prefix and a hyphen, for example `vendor-status-card`.
- Use Lit reactive properties for public attributes and internal state.
- Initialize defaults in the constructor when using no-build JavaScript.
- Keep `render()` deterministic and cheap.
- Replace arrays and objects instead of mutating them in place when a rerender should happen.
- Call `super.connectedCallback()` and `super.disconnectedCallback()` when overriding Lit lifecycle methods.
- Remove global event listeners, timers, observers, and subscriptions in `disconnectedCallback()`.
- Use `DataHandler` for TCA-managed record writes triggered by a component.
- Add `inheritAccessFromModule` or explicit backend permission checks on AJAX routes.
- Use XLIFF labels for backend-visible strings.
- Test with a non-admin backend user and keyboard navigation.

## Donts

- Do not target TYPO3 12/13 APIs in this skill's examples.
- Do not rely on relative imports in TYPO3-loaded backend modules.
- Do not add inline `<script>` blocks for component setup.
- Do not put sensitive or large JSON payloads into HTML attributes.
- Do not expose all import maps to anonymous frontend visitors.
- Do not use TYPO3 backend Web Components in frontend output.
- Do not call backend routes from frontend JavaScript.
- Do not write raw SQL for records that are managed by TCA.
- Do not fetch data or perform heavy transformations inside `render()`.
- Do not mutate Lit reactive arrays/objects in place and expect an update.
- Do not assume every Core Web Component is stable or reusable just because it exists.
- Do not use modals for routine information; prefer notifications or inline UI.

## Speed Checklist

- Load the module only where the backend screen needs it.
- Keep first render useful without waiting for network data when possible.
- Use skeleton, spinner, empty, and error states for async components.
- Use `firstUpdated()` for one-shot setup that needs rendered DOM.
- Use `updated(changedProperties)` only for follow-up work that truly depends on changed properties.
- Use debounced or throttled handlers for search, resize, drag, and typing.
- Abort stale requests with `AbortController` or TYPO3's AJAX helper behavior.
- Cache repeated endpoint results server-side or client-side when data is stable.
- Avoid full-page reloads for local UI updates, but do not turn a simple backend action into a large SPA.
- For frontend components, use Vite or another production asset pipeline because TYPO3 v14 Core no longer handles frontend concatenation/compression.

## Security And Accessibility Checklist

- Escape all Fluid output used in attributes or text.
- Keep privileged values on the server and fetch them through permission-checked backend routes.
- Use backend route `inheritAccessFromModule` for module-owned AJAX endpoints.
- Add CSRF/session-token protections through TYPO3 backend routing instead of custom tokens where possible.
- Respect backend CSP. Configure `ContentSecurityPolicies.php` when the component must fetch an external domain.
- Do not use `unsafeHTML` unless the input is already sanitized and the reason is documented.
- Provide real buttons for actions, not clickable divs.
- Preserve focus after modal, panel, and async updates.
- Support Enter, Space, Escape, Tab, and arrow-key behavior where the widget pattern expects it.
- Keep ARIA attributes synchronized with visible state.
- Respect reduced motion for animations and transitions.

## Cool Examples

- A backend status card that fetches system or extension metrics through an authenticated AJAX route.
- A record health dashboard with filters, pagination, and row actions wired to DataHandler-backed PHP endpoints.
- A Form Editor custom element that uses the built-in v14.2 `<typo3-form-form-element-stage-item>` instead of legacy Fluid stage partials.
- A page-tree backed backend module using `@typo3/backend/tree/page-tree-element` as `navigationComponent`.
- A content quality preview, similar in spirit to Yoast SEO for TYPO3's custom elements for snippet previews, social previews, analysis results, and status indicators.
- A copy-to-clipboard or QR-code utility wrapper around TYPO3 backend helper components.
- A progress tracker for long-running backend tasks, with polling or server status refresh and clear cancellation behavior.

## Lit Or Vanilla JavaScript

Use vanilla JavaScript when:

- The behavior is one short event listener.
- The DOM is mostly static.
- There is no reusable public API.
- No reactive rendering is needed.

Use Lit when:

- The element has several states and rerenders.
- Attribute/property conversion matters.
- The component needs slots, scoped styles, or lifecycle cleanup.
- Multiple instances appear on one backend screen.
- The UI should be portable across backend modules or extensions.
- You want to align with TYPO3 backend's Lit-heavy direction.

## Source Notes

- MDN defines Web Components as browser APIs around custom elements, Shadow DOM, and templates/slots.
- TYPO3 Explained documents ES module import maps, `Configuration/JavaScriptModules.php`, backend module configuration, backend routes, AJAX requests, AssetCollector, and `f:asset.module`.
- TYPO3 v14 module configuration exposes `component` and `navigationComponent`; v14 uses `@typo3/backend/tree/page-tree-element` for the page tree navigation component.
- TYPO3 v14.2 Form Framework introduced Web Component-based simplification for custom form elements and modernized the Form Editor tree with Lit.
- Camino: Camp Vienna "Lit it Up!" by ochorocho is a practical TYPO3 backend Lit presentation and demo source.
- Lit positions itself as a small Web Components helper with reactive properties, declarative templates, scoped styles through Shadow DOM, and efficient dynamic updates.

## Similar Local Skill Comparison

- `typo3-datahandler` is the closest backend programming neighbor for server-side record mutations. Use it when a component changes TCA-managed data.
- `typo3-visual-editor` is the closest UI/backend/frontend bridge. Use it when the component participates in editing content in context.
- `typo3-workspaces` is the closest state model neighbor. Use it when the component displays live/draft overlays or publish actions.
- `typo3-vite` is the closest frontend asset neighbor. Use it when the user asks whether the Web Component approach should run in the frontend.
