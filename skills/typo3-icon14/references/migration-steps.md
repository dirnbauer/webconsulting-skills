# TYPO3 Icon Migration Steps

## Step 5: Migration Checklist

For each extension icon that needs updating:

- [ ] Read the current SVG content
- [ ] Identify the semantic meaning (what does the icon represent?)
- [ ] Remove solid background rectangle/path
- [ ] Replace `#FFFFFF` fills with `currentColor`
- [ ] Replace brand-color accent fills with `var(--icon-color-accent, #ff8700)`
- [ ] Replace `#333333` detail fills with `currentColor`
- [ ] Set depth fill opacity to **`.8`** for module/sidebar icons — validated against TYPO3 v14 Fresh theme dark sidebar; `.4` renders too faint
- [ ] Verify outline ring width is **≥ 6 units** in a 64-unit viewBox (outer gap minus inner cutout)
- [ ] Verify accent elements are **≥ 12 units** in smallest dimension for 64×64 module icons
- [ ] Set **viewBox** per icon type — `0 0 64 64` for backend **module** icons; `0 0 16 16` for many action/plugin/record icons (match a Core reference SVG)
- [ ] Remove all legacy attributes (`version`, `xmlns:xlink`, `enable-background`, `xml:space`, `id`)
- [ ] Remove generator comments
- [ ] Redesign shapes from filled-on-background to outlined/line-art
- [ ] Mental contrast check at half render size (32px for module, 8px for 16×16 icons)
- [ ] Verify `Configuration/Icons.php` exists and uses `SvgIconProvider`
- [ ] Verify `Configuration/Backend/Modules.php` references correct `iconIdentifier`
- [ ] Verify TCA `typeicon_classes` and `pluginIcon` references
- [ ] Clear TYPO3 caches and browser localStorage after deployment

## Step 6: Transforming Icon Shapes

### From Filled to Outlined

Old style icons are typically solid white shapes on a colored background. The v14 style
uses outlined shapes with an inner/outer path to create the outline effect.

**Old (solid shape on background):**
```xml
<path fill="#5BA34F" d="M0,0h64v64H0V0z"/>
<polygon fill="#FFFFFF" points="18,16 18,44 27,44 32,50 37,44 46,44 46,16"/>
```

**New (outlined shape, no background):**
```xml
<path fill="currentColor" d="M18 16v28h9l5 6 5-6h9V16H18zm26 26H38l-6 7.2L26 42H20V18h24v24z"/>
```

The outer path defines the full shape, the inner path (after `z` or as a cutout) creates
the outlined/hollow appearance.
