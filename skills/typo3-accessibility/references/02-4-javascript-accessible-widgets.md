# 4. JavaScript: Accessible Widgets

Continues `typo3-accessibility` from [full guide](full-guide.md).

## 4. JavaScript: Accessible Widgets

### 4.1 Accordion

```javascript
// EXT:site_package/Resources/Public/JavaScript/accordion.js
class AccessibleAccordion {
    constructor(container) {
        this.container = container;
        this.triggers = container.querySelectorAll('[data-accordion-trigger]');
        this.init();
    }

    init() {
        this.triggers.forEach((trigger) => {
            trigger.addEventListener('click', () => this.toggle(trigger));
            trigger.addEventListener('keydown', (e) => this.handleKeydown(e));
        });
    }

    toggle(trigger) {
        const expanded = trigger.getAttribute('aria-expanded') === 'true';
        const panelId = trigger.getAttribute('aria-controls');
        const panel = document.getElementById(panelId);

        trigger.setAttribute('aria-expanded', String(!expanded));
        panel.hidden = expanded;
    }

    handleKeydown(e) {
        const triggers = [...this.triggers];
        const index = triggers.indexOf(e.currentTarget);

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                triggers[(index + 1) % triggers.length].focus();
                break;
            case 'ArrowUp':
                e.preventDefault();
                triggers[(index - 1 + triggers.length) % triggers.length].focus();
                break;
            case 'Home':
                e.preventDefault();
                triggers[0].focus();
                break;
            case 'End':
                e.preventDefault();
                triggers[triggers.length - 1].focus();
                break;
        }
    }
}

document.querySelectorAll('[data-accordion]').forEach((el) => new AccessibleAccordion(el));
```

### 4.2 Tabs

```javascript
// EXT:site_package/Resources/Public/JavaScript/tabs.js
class AccessibleTabs {
    constructor(container) {
        this.tablist = container.querySelector('[role="tablist"]');
        this.tabs = [...this.tablist.querySelectorAll('[role="tab"]')];
        this.panels = this.tabs.map(
            (tab) => document.getElementById(tab.getAttribute('aria-controls'))
        );
        this.init();
    }

    init() {
        this.tabs.forEach((tab) => {
            tab.addEventListener('click', () => this.selectTab(tab));
            tab.addEventListener('keydown', (e) => this.handleKeydown(e));
        });
    }

    selectTab(selectedTab) {
        this.tabs.forEach((tab, i) => {
            const selected = tab === selectedTab;
            tab.setAttribute('aria-selected', String(selected));
            tab.tabIndex = selected ? 0 : -1;
            this.panels[i].hidden = !selected;
        });
        selectedTab.focus();
    }

    handleKeydown(e) {
        const index = this.tabs.indexOf(e.currentTarget);
        let next;

        switch (e.key) {
            case 'ArrowRight':
                next = (index + 1) % this.tabs.length;
                break;
            case 'ArrowLeft':
                next = (index - 1 + this.tabs.length) % this.tabs.length;
                break;
            case 'Home':
                next = 0;
                break;
            case 'End':
                next = this.tabs.length - 1;
                break;
            default:
                return;
        }
        e.preventDefault();
        this.selectTab(this.tabs[next]);
    }
}

document.querySelectorAll('[data-tabs]').forEach((el) => new AccessibleTabs(el));
```

### 4.3 Modal / Dialog

```javascript
// EXT:site_package/Resources/Public/JavaScript/dialog.js
class AccessibleDialog {
    constructor(dialog) {
        this.dialog = dialog;
        this.previousFocus = null;
        this.init();
    }

    init() {
        // showModal() closes on Escape natively; listen to 'close' for focus restore only.
        this.dialog.addEventListener('close', () => {
            this.previousFocus?.focus();
        });

        this.dialog.addEventListener('click', (e) => {
            if (e.target === this.dialog) this.dialog.close();
        });
    }

    open() {
        this.previousFocus = document.activeElement;
        // showModal() provides built-in focus trapping in supporting browsers; skip custom Tab loops unless you must target legacy engines.
        this.dialog.showModal();
    }

    close() {
        this.dialog.close();
    }
}
```

Use the native `<dialog>` element in Fluid:

```html
<dialog id="my-dialog" aria-labelledby="dialog-title">
    <h2 id="dialog-title">{dialogTitle}</h2>
    <div>{dialogContent}</div>
    <button type="button" data-close-dialog>
        <f:translate key="button.close" />
    </button>
</dialog>
```

### 4.4 Reduced Motion Check

```javascript
// EXT:site_package/Resources/Public/JavaScript/motion.js
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function getTransitionDuration() {
    return prefersReducedMotion.matches ? 0 : 300;
}

prefersReducedMotion.addEventListener('change', () => {
    document.documentElement.classList.toggle('reduce-motion', prefersReducedMotion.matches);
});

if (prefersReducedMotion.matches) {
    document.documentElement.classList.add('reduce-motion');
}
```

```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

### 4.5 Live Region Announcer

```javascript
// EXT:site_package/Resources/Public/JavaScript/announcer.js
class LiveAnnouncer {
    constructor() {
        this.region = document.createElement('div');
        this.region.setAttribute('aria-live', 'polite');
        this.region.setAttribute('aria-atomic', 'true');
        this.region.classList.add('sr-only');
        document.body.appendChild(this.region);
    }

    announce(message, priority = 'polite') {
        this.region.setAttribute('aria-live', priority);
        this.region.textContent = '';
        requestAnimationFrame(() => {
            this.region.textContent = message;
        });
    }
}

window.liveAnnouncer = new LiveAnnouncer();
```

Usage: `window.liveAnnouncer.announce('3 results found');`
