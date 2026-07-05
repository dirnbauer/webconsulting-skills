# TYPO3 accessibility fix patterns

## Skip link and main landmark

```html
<a class="skip-link" href="#main-content">Zum Inhalt springen</a>
<main id="main-content" tabindex="-1">
  <f:render section="Main" />
</main>
```

Use `tabindex="-1"` only if JavaScript focuses the main area after skip-link activation.

## Main navigation

```html
<nav aria-label="Hauptnavigation" data-a11y-component="navigation.main">
  <ul>
    <li>
      <a href="/foo/" aria-current="page">Foo</a>
    </li>
  </ul>
</nav>
```

## Mobile navigation button

```html
<button
  class="navbar-toggler"
  type="button"
  aria-controls="main-navigation"
  aria-expanded="false"
  aria-label="Hauptnavigation öffnen"
>
  <span aria-hidden="true"></span>
</button>
```

Update `aria-expanded` when the menu opens/closes.

## Accordion

```html
<h2>
  <button type="button" aria-expanded="false" aria-controls="faq-1" id="faq-1-button">
    Frage
  </button>
</h2>
<div id="faq-1" role="region" aria-labelledby="faq-1-button" hidden>
  Antwort
</div>
```

## TYPO3 Fluid image

Do not output images without alt. For decorative images:

```html
<f:image image="{image}" alt="" />
```

For informative images, bind to a maintained metadata field:

```html
<f:image image="{image}" alt="{image.alternative}" />
```

Add editorial guidance so editors do not enter filenames or generic text.

## Form errors

```html
<label for="email">E-Mail-Adresse</label>
<input id="email" name="email" type="email" autocomplete="email" aria-describedby="email-error" aria-invalid="true">
<p id="email-error">Bitte geben Sie eine gültige E-Mail-Adresse ein.</p>
```

## Avoid

- `tabindex="1"` or higher.
- `<div onclick="...">` as control.
- Placeholder-only labels.
- Removing outline without replacement.
- `aria-label` that disagrees with visible text.
- Hidden focusable elements.
