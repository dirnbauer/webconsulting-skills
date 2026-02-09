---
name: ab-testing
description: >-
  Design and implement statistically valid A/B tests and experiments. Covers hypothesis
  creation, sample size calculation, test design, metrics selection, and results analysis.
  Use when working with ab test, a/b test, split test, experiment, test this change,
  multivariate test, hypothesis, statistical significance.
license: MIT
metadata:
  version: "1.0.0"
---

# A/B Test Setup

> **Source:** This skill is adapted from **[AgentKits Marketing](https://github.com/aitytech/agentkits-marketing)** 
> by AITYTech. Enterprise-grade AI marketing automation (MIT License).

Design A/B tests that produce statistically valid, actionable results.

---

## Core Principles

### 1. Start with a Hypothesis
Not just "let's see what happens" — specific prediction based on reasoning or data.

### 2. Test One Thing
Single variable per test. Otherwise you don't know what worked.

### 3. Statistical Rigor
Pre-determine sample size. Don't peek and stop early.

### 4. Measure What Matters
Primary metric tied to business value. Guardrail metrics to prevent harm.

---

## Hypothesis Framework

### Structure

```
Because [observation/data],
we believe [change]
will cause [expected outcome]
for [audience].
We'll know this is true when [metrics].
```

### Example

**Weak**: "Changing the button color might increase clicks."

**Strong**: "Because users report difficulty finding the CTA (per heatmaps), we believe making the button larger and using contrasting color will increase CTA clicks by 15%+ for new visitors. We'll measure click-through rate from page view to signup start."

---

## Test Types

| Type | Description | When to Use |
|------|-------------|-------------|
| A/B (Split) | Two versions, single change | Most common, easiest |
| A/B/n | Multiple variants | Testing several options |
| Multivariate (MVT) | Multiple changes in combinations | Tests interactions, needs lots of traffic |
| Split URL | Different URLs | Major page changes |

---

## Sample Size Calculation

### Quick Reference

| Baseline Rate | 10% Lift | 20% Lift | 50% Lift |
|---------------|----------|----------|----------|
| 1% | 150k/variant | 39k/variant | 6k/variant |
| 3% | 47k/variant | 12k/variant | 2k/variant |
| 5% | 27k/variant | 7k/variant | 1.2k/variant |
| 10% | 12k/variant | 3k/variant | 550/variant |

### Inputs Needed

1. **Baseline conversion rate**: Your current rate
2. **Minimum detectable effect (MDE)**: Smallest change worth detecting
3. **Significance level**: Usually 95%
4. **Power**: Usually 80%

### Duration

```
Duration = Sample size × Number of variants
           ─────────────────────────────────
           Daily traffic × Conversion rate
```

Minimum: 1-2 business cycles (1-2 weeks)

---

## Metrics Selection

### Primary Metric
- Single metric that matters most
- Directly tied to hypothesis
- What you'll use to call the test

### Secondary Metrics
- Support primary interpretation
- Explain why/how the change worked

### Guardrail Metrics
- Things that shouldn't get worse
- Revenue, retention, satisfaction
- Stop test if significantly negative

### Examples

**Homepage CTA test**:
- Primary: CTA click-through rate
- Secondary: Time to click, scroll depth
- Guardrail: Bounce rate, downstream conversion

**Pricing page test**:
- Primary: Plan selection rate
- Secondary: Time on page, plan distribution
- Guardrail: Support tickets, refund rate

---

## Running the Test

### Pre-Launch Checklist

- [ ] Hypothesis documented
- [ ] Primary metric defined
- [ ] Sample size calculated
- [ ] Test duration estimated
- [ ] Variants implemented correctly
- [ ] Tracking verified
- [ ] QA completed on all variants

### During the Test

**DO**:
- Monitor for technical issues
- Document external factors

**DON'T**:
- Peek at results and stop early
- Make changes to variants
- Add traffic from new sources

### The Peeking Problem

Looking at results before sample size and stopping when you see significance leads to:
- False positives
- Inflated effect sizes
- Wrong decisions

**Solution**: Pre-commit to sample size and stick to it.

---

## Analyzing Results

### What to Check

1. **Did you reach sample size?** If not, result is preliminary
2. **Is it statistically significant?** Check confidence intervals, p-value
3. **Is the effect size meaningful?** Compare to MDE, project business impact
4. **Are secondary metrics consistent?** Do they support the primary?
5. **Any guardrail concerns?** Did anything get worse?
6. **Segment differences?** Mobile vs. desktop? New vs. returning?

### Interpreting Results

| Result | Action |
|--------|--------|
| Significant winner | Implement variant |
| Significant loser | Keep control, learn why |
| No significant difference | Need more traffic or bolder test |
| Mixed signals | Dig deeper, maybe segment |

---

## Documentation Template

```
Test Name: [Name]
Dates: [Start] - [End]

Hypothesis:
[Full hypothesis statement]

Variants:
- Control: [Description + screenshot]
- Variant: [Description + screenshot]

Results:
- Sample size: [achieved vs. target]
- Primary metric: [control] vs. [variant] ([% change], [confidence])
- Secondary metrics: [summary]

Decision: [Winner/Loser/Inconclusive]
Action: [What we're doing]

Learnings:
[What we learned, what to test next]
```

---

## Common Mistakes

### Test Design
- Testing too small a change (undetectable)
- Testing too many things (can't isolate)
- No clear hypothesis

### Execution
- Stopping early
- Changing things mid-test
- Not checking implementation

### Analysis
- Ignoring confidence intervals
- Cherry-picking segments
- Over-interpreting inconclusive results

---

## Credits & Attribution

This skill is adapted from **[AgentKits Marketing](https://github.com/aitytech/agentkits-marketing)** by AITYTech.

**Copyright (c) AITYTech** - MIT License  
Adapted by webconsulting.at for this skill collection
