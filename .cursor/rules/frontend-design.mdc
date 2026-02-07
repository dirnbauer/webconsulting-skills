---
name: frontend-design
description: Guide for creating distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices. Use when building UI components, pages, applications, or when the user wants visually striking, memorable interfaces.
version: 1.0.0
license: MIT
triggers:
  - frontend
  - design
  - ui
  - interface
  - beautiful
  - creative
  - distinctive
  - aesthetics
  - visual
  - memorable
  - striking
  - polished
  - production
---

# Frontend Design

> **Source:** This skill is adapted from **[Anthropic's Skills](https://github.com/anthropics/skills)** 
> frontend-design skill for Claude Code and AI agents.

Create distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. 
Implement real working code with exceptional attention to aesthetic details and creative choices.

---

## When to Apply

Reference these guidelines when:

- Building new UI components, pages, or applications
- User asks for "beautiful", "stunning", "creative", or "distinctive" interfaces
- Creating landing pages, dashboards, or marketing sites
- Refactoring existing UI for visual impact
- User complains about generic or boring design

---

## Design Thinking Process

Before coding, understand the context and commit to a **BOLD** aesthetic direction:

### 1. Purpose Analysis

| Question | Why It Matters |
|----------|----------------|
| What problem does this interface solve? | Drives functional requirements |
| Who uses it? | Determines complexity level |
| What emotion should it evoke? | Guides color and tone choices |

### 2. Tone Selection

Pick an **extreme** aesthetic direction—not a blend:

| Direction | Characteristics | Best For |
|-----------|-----------------|----------|
| Brutally Minimal | Lots of whitespace, stark contrasts, limited elements | Premium products, portfolios |
| Maximalist Chaos | Dense information, overlapping elements, bold patterns | Creative agencies, entertainment |
| Retro-Futuristic | Neon accents, geometric shapes, gradient meshes | Tech startups, gaming |
| Organic/Natural | Soft curves, earthy tones, flowing animations | Wellness, sustainability |
| Luxury/Refined | Subtle gradients, serif fonts, gold accents | High-end products, fashion |
| Playful/Toy-like | Bright colors, rounded corners, bouncy animations | Consumer apps, children's products |
| Editorial/Magazine | Strong typography, grid-based, high contrast | News, content platforms |
| Brutalist/Raw | Exposed structure, monospace fonts, raw HTML feel | Developer tools, experimental |
| Art Deco/Geometric | Bold shapes, symmetry, metallic accents | Architecture, luxury |
| Soft/Pastel | Low contrast, rounded shapes, gentle colors | Healthcare, wellness |
| Industrial/Utilitarian | Metal textures, sharp edges, monochrome | Manufacturing, enterprise |

### 3. Differentiation Question

**Ask yourself:** What's the ONE thing someone will remember about this interface?

---

## Aesthetic Guidelines

### Typography

**CRITICAL:** Choose fonts that are beautiful, unique, and interesting.

#### Fonts to AVOID (Generic AI Slop)

```css
/* ❌ NEVER use these - they scream "AI generated" */
font-family: Inter, sans-serif;
font-family: Roboto, sans-serif;
font-family: Arial, sans-serif;
font-family: system-ui, sans-serif;
font-family: -apple-system, sans-serif;
```

#### Distinctive Font Pairings

| Aesthetic | Display Font | Body Font | Example Use |
|-----------|--------------|-----------|-------------|
| **Modern Editorial** | Playfair Display | Source Sans Pro | Magazines, blogs |
| **Tech Premium** | Space Grotesk | DM Sans | SaaS dashboards |
| **Luxury Refined** | Cormorant Garamond | Lato | High-end e-commerce |
| **Bold Creative** | Clash Display | Satoshi | Agency portfolios |
| **Warm Friendly** | Fraunces | Nunito | Consumer apps |
| **Neo-Brutalist** | JetBrains Mono | IBM Plex Mono | Developer tools |
| **Retro Modern** | Cabinet Grotesk | Outfit | Startup landing pages |
| **Elegant Minimal** | Tenor Sans | Karla | Photography portfolios |
| **Playful Fun** | Fredoka | Quicksand | Kids products |
| **Corporate Trust** | Libre Franklin | Merriweather | Financial services |

```css
/* ✅ GOOD: Distinctive pairing */
:root {
  --font-display: 'Clash Display', sans-serif;
  --font-body: 'Satoshi', sans-serif;
}

h1, h2, h3 {
  font-family: var(--font-display);
  letter-spacing: -0.02em;
}

body {
  font-family: var(--font-body);
  font-weight: 450;
}
```

### Color & Theme

#### Commit to a Cohesive Aesthetic

**Dominant colors with sharp accents outperform timid, evenly-distributed palettes.**

```css
/* ❌ BAD: Timid, evenly distributed */
:root {
  --color-1: #6366f1;
  --color-2: #8b5cf6;
  --color-3: #a855f7;
  --color-4: #d946ef;
}

/* ✅ GOOD: Dominant with sharp accent */
:root {
  --bg-primary: #0a0a0b;      /* 70% - Dominant */
  --bg-secondary: #1a1a1d;    /* 20% - Supporting */
  --accent: #ff3366;          /* 10% - Sharp accent */
  --text-primary: #fafafa;
}
```

#### Color Palette Examples

| Palette Name | Colors | Use Case |
|--------------|--------|----------|
| **Midnight Neon** | `#0a0a0b`, `#1a1a1d`, `#ff3366`, `#00ff88` | Tech, gaming |
| **Warm Cream** | `#faf7f2`, `#e8e2d9`, `#1a1a1a`, `#d4a574` | Luxury, editorial |
| **Ocean Depths** | `#0c1222`, `#1e293b`, `#38bdf8`, `#818cf8` | SaaS, dashboards |
| **Forest Sage** | `#1a2e1a`, `#2d472d`, `#86efac`, `#fef3c7` | Sustainability |
| **Coral Sunset** | `#fff7ed`, `#fed7aa`, `#f97316`, `#1c1917` | Warm, inviting |
| **Electric Purple** | `#0f0f1a`, `#1a1a2e`, `#a855f7`, `#f0abfc` | Creative, bold |
| **Monochrome Pro** | `#ffffff`, `#f5f5f5`, `#171717`, `#404040` | Professional |
| **Retro Cream** | `#f5f5dc`, `#daa520`, `#8b4513`, `#2f4f4f` | Vintage |

### Motion & Animation

#### High-Impact Moments

Focus on key moments rather than scattered micro-interactions:

```css
/* ✅ GOOD: Orchestrated page load with staggered reveals */
@keyframes fadeSlideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-title {
  animation: fadeSlideUp 0.6s ease-out forwards;
  animation-delay: 0.1s;
  opacity: 0;
}

.hero-subtitle {
  animation: fadeSlideUp 0.6s ease-out forwards;
  animation-delay: 0.2s;
  opacity: 0;
}

.hero-cta {
  animation: fadeSlideUp 0.6s ease-out forwards;
  animation-delay: 0.3s;
  opacity: 0;
}
```

#### Scroll-Triggered Animations

```css
/* Intersection Observer reveals */
.reveal {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

#### Hover States That Surprise

```css
/* ✅ Creative hover effect */
.card {
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
}

.card:hover::before {
  opacity: 1;
}
```

### Spatial Composition

#### Break the Grid

```css
/* ✅ Asymmetric layout */
.hero {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 4rem;
  align-items: center;
}

/* ✅ Overlapping elements */
.feature-card {
  position: relative;
  margin-left: -2rem;
  z-index: 1;
}

.feature-card:nth-child(2) {
  margin-left: 0;
  margin-top: -3rem;
  z-index: 2;
}
```

#### Diagonal Flow

```css
/* Diagonal section divider */
.section-divider {
  clip-path: polygon(0 0, 100% 10%, 100% 100%, 0 90%);
  padding: 8rem 0;
}
```

### Backgrounds & Visual Details

#### Create Atmosphere

```css
/* ✅ Gradient mesh background */
.hero {
  background: 
    radial-gradient(ellipse at 20% 30%, rgba(168, 85, 247, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(56, 189, 248, 0.1) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(15, 23, 42, 1) 0%, rgba(15, 23, 42, 1) 100%);
}

/* ✅ Noise texture overlay */
.textured {
  position: relative;
}

.textured::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
}

/* ✅ Geometric patterns */
.pattern-dots {
  background-image: radial-gradient(circle, #374151 1px, transparent 1px);
  background-size: 24px 24px;
}
```

---

## Component Examples

### Hero Section (Dark Tech)

```html
<section class="hero">
  <div class="hero-content">
    <span class="hero-eyebrow">Introducing v2.0</span>
    <h1 class="hero-title">
      Ship faster.<br />
      <span class="gradient-text">Break nothing.</span>
    </h1>
    <p class="hero-subtitle">
      The deployment platform that lets your team move fast 
      without breaking production.
    </p>
    <div class="hero-actions">
      <button class="btn-primary">Start Building</button>
      <button class="btn-secondary">Watch Demo</button>
    </div>
  </div>
  <div class="hero-visual">
    <div class="glow-orb"></div>
    <div class="code-preview">
      <!-- Animated code snippet -->
    </div>
  </div>
</section>

<style>
.hero {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding: 8rem 4rem;
  background: #0a0a0b;
  color: #fafafa;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -25%;
  width: 80%;
  height: 150%;
  background: radial-gradient(ellipse, rgba(168, 85, 247, 0.15) 0%, transparent 70%);
  pointer-events: none;
}

.hero-eyebrow {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: rgba(168, 85, 247, 0.1);
  border: 1px solid rgba(168, 85, 247, 0.3);
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #a855f7;
  margin-bottom: 1.5rem;
}

.hero-title {
  font-family: 'Clash Display', sans-serif;
  font-size: clamp(3rem, 6vw, 5rem);
  font-weight: 600;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: 1.5rem;
}

.gradient-text {
  background: linear-gradient(135deg, #a855f7, #38bdf8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #a1a1aa;
  max-width: 480px;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn-primary {
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #a855f7, #7c3aed);
  color: white;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 40px rgba(168, 85, 247, 0.3);
}

.btn-secondary {
  padding: 1rem 2rem;
  background: transparent;
  color: #fafafa;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
}

.glow-orb {
  position: absolute;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  filter: blur(60px);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
</style>
```

### Feature Card (Glass Morphism)

```html
<div class="feature-card">
  <div class="feature-icon">
    <svg><!-- Icon SVG --></svg>
  </div>
  <h3 class="feature-title">Lightning Fast</h3>
  <p class="feature-description">
    Deploy in seconds, not minutes. Our edge network ensures 
    your users get the fastest experience possible.
  </p>
  <a href="#" class="feature-link">Learn more →</a>
</div>

<style>
.feature-card {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  transition: transform 0.3s, border-color 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: rgba(168, 85, 247, 0.5);
}

.feature-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #a855f7, #7c3aed);
  border-radius: 12px;
  margin-bottom: 1.5rem;
}

.feature-icon svg {
  width: 24px;
  height: 24px;
  color: white;
}

.feature-title {
  font-family: 'Clash Display', sans-serif;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.feature-description {
  color: #a1a1aa;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.feature-link {
  color: #a855f7;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s;
}

.feature-link:hover {
  color: #c084fc;
}
</style>
```

### Pricing Card (Premium)

```html
<div class="pricing-card featured">
  <div class="pricing-badge">Most Popular</div>
  <div class="pricing-header">
    <h3 class="pricing-name">Pro</h3>
    <div class="pricing-price">
      <span class="price-currency">$</span>
      <span class="price-amount">49</span>
      <span class="price-period">/month</span>
    </div>
    <p class="pricing-description">Perfect for growing teams</p>
  </div>
  <ul class="pricing-features">
    <li><span class="check">✓</span> Unlimited deployments</li>
    <li><span class="check">✓</span> Custom domains</li>
    <li><span class="check">✓</span> Analytics dashboard</li>
    <li><span class="check">✓</span> Priority support</li>
    <li><span class="check">✓</span> Team collaboration</li>
  </ul>
  <button class="pricing-cta">Get Started</button>
</div>

<style>
.pricing-card {
  padding: 2.5rem;
  background: #1a1a1d;
  border: 1px solid #2a2a2d;
  border-radius: 20px;
  position: relative;
  overflow: hidden;
}

.pricing-card.featured {
  background: linear-gradient(180deg, rgba(168, 85, 247, 0.1) 0%, #1a1a1d 50%);
  border-color: rgba(168, 85, 247, 0.3);
  transform: scale(1.05);
}

.pricing-badge {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  padding: 0.25rem 0.75rem;
  background: linear-gradient(135deg, #a855f7, #7c3aed);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
}

.pricing-name {
  font-family: 'Clash Display', sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.pricing-price {
  display: flex;
  align-items: baseline;
  margin-bottom: 0.5rem;
}

.price-currency {
  font-size: 1.5rem;
  font-weight: 600;
  color: #a1a1aa;
}

.price-amount {
  font-family: 'Clash Display', sans-serif;
  font-size: 4rem;
  font-weight: 700;
  line-height: 1;
}

.price-period {
  font-size: 1rem;
  color: #a1a1aa;
  margin-left: 0.25rem;
}

.pricing-description {
  color: #71717a;
  margin-bottom: 2rem;
}

.pricing-features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem;
}

.pricing-features li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: #d4d4d8;
}

.check {
  color: #22c55e;
  font-weight: 600;
}

.pricing-cta {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #a855f7, #7c3aed);
  color: white;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.pricing-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 40px rgba(168, 85, 247, 0.3);
}
</style>
```

### Testimonial Card (Editorial)

```html
<div class="testimonial-card">
  <blockquote class="testimonial-quote">
    "This completely transformed how our team ships code. 
    We went from weekly deploys to multiple times per day, 
    and our confidence in production has never been higher."
  </blockquote>
  <div class="testimonial-author">
    <img src="avatar.jpg" alt="Sarah Chen" class="author-avatar" />
    <div class="author-info">
      <div class="author-name">Sarah Chen</div>
      <div class="author-title">CTO at Acme Inc</div>
    </div>
  </div>
</div>

<style>
.testimonial-card {
  padding: 3rem;
  background: linear-gradient(135deg, #faf7f2 0%, #f5f0e8 100%);
  border-radius: 24px;
  position: relative;
}

.testimonial-card::before {
  content: '"';
  position: absolute;
  top: 1.5rem;
  left: 2rem;
  font-family: 'Playfair Display', serif;
  font-size: 8rem;
  line-height: 1;
  color: rgba(0, 0, 0, 0.05);
}

.testimonial-quote {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-style: italic;
  line-height: 1.6;
  color: #1a1a1a;
  margin: 0 0 2rem;
  position: relative;
  z-index: 1;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.author-name {
  font-weight: 600;
  color: #1a1a1a;
}

.author-title {
  color: #71717a;
  font-size: 0.875rem;
}
</style>
```

---

## Anti-Patterns to Avoid

### The "AI Slop" Checklist

| Anti-Pattern | Why It's Bad | Better Alternative |
|--------------|--------------|-------------------|
| Purple gradient on white | Overused, generic | Commit to dark or light theme |
| Inter/Roboto fonts | Seen everywhere | Distinctive display + body pairing |
| 12-column grid everywhere | Predictable | Asymmetric layouts, overlap |
| Generic gradient buttons | No personality | Solid colors with subtle effects |
| Card soup layout | No visual hierarchy | Vary sizes, create focal points |
| Stock photo heroes | Feels corporate | Illustrations, 3D, or real photos |
| Rounded corners on everything | Too safe | Mix sharp and rounded strategically |
| Evenly spaced sections | Monotonous | Vary density and rhythm |

---

## Quick Reference: CSS Variables System

```css
:root {
  /* Colors */
  --bg-primary: #0a0a0b;
  --bg-secondary: #1a1a1d;
  --bg-tertiary: #2a2a2d;
  --text-primary: #fafafa;
  --text-secondary: #a1a1aa;
  --text-tertiary: #71717a;
  --accent: #a855f7;
  --accent-light: #c084fc;
  --accent-dark: #7c3aed;
  
  /* Typography */
  --font-display: 'Clash Display', sans-serif;
  --font-body: 'Satoshi', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-24: 6rem;
  
  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-2xl: 24px;
  --radius-full: 9999px;
  
  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 40px rgba(0, 0, 0, 0.5);
  --shadow-glow: 0 0 40px rgba(168, 85, 247, 0.3);
  
  /* Transitions */
  --transition-fast: 0.15s ease;
  --transition-normal: 0.3s ease;
  --transition-slow: 0.5s ease;
}
```

---

## Credits & Attribution

This skill is adapted from **[Anthropic's Skills](https://github.com/anthropics/skills)**.

Original repository: https://github.com/anthropics/skills

**Copyright (c) Anthropic** - MIT License  
Adapted by webconsulting.at for this skill collection
