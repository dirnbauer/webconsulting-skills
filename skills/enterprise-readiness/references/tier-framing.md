# Tier framing — when does this skill apply, and to what depth?

This skill is the **high-stakes end** of the verification spectrum. Lower-stakes projects (internal scripts, prototypes, throwaway PoCs) have correspondingly lighter bars — they do not need SLSA Level 3, cosign attestation, or OpenSSF Silver. Production deploys, customer-facing releases, and supply-chain-critical artifacts do.

## Ask before applying

If the project being assessed does not yet ship to customers or production-grade infrastructure, ask the user **what target tier they want** before applying the full checklist. Applying enterprise-grade controls to a prototype is wasted work — and worse, it trains the team to ignore the report. That is the same failure mode the [`automated-assessment` skill](https://github.com/netresearch/automated-assessment-skill/blob/main/skills/automated-assessment/references/calibration.md) calls *calibration debt*: a noisy report nobody acts on costs CI time AND erodes trust in the next genuine signal.

## What "tier" means here

Roughly:

| Tier | What it ships to | What this skill applies |
|------|------------------|-------------------------|
| Prototype / internal script | A laptop, a one-off CI job | Almost nothing here. Skip. |
| Internal tool / shared utility | Internal teams, not customers | Subset: Critical Rules, basic dependabot, CI permissions hardening. |
| Customer-facing service | Production, paying customers | Full checklist applies. |
| Supply-chain-critical artifact | Other projects depend on releases | Full checklist + SLSA L3 + signed releases + Best Practices Silver+. |

These are heuristics, not strict gates. Surface the tier question; let the user decide.

## Why the checklist is the floor, not the ceiling

For projects in the customer-facing or supply-chain-critical tiers, the checklists in this skill define the **floor** of production readiness — not the ceiling. A project meeting every checklist item is the minimum bar to ship enterprise-grade; it does not exempt the project from project-specific risks (sector compliance, internal threat models, customer SLAs) that the checklist cannot encode.

The checklist is also not a default to apply to every repo in the org. Applying it indiscriminately confuses "this is a high-stakes project" with "this skill ran on it" and dilutes the signal.

## Inspiration

The tier framing comes from [Spotify Engineering — Better Experiments with LLM Evals: A Funnel, Not a Fork](https://engineering.atspotify.com/2026/5/better-experiments-with-llm-evals-a-funnel-not-a-fork): *"Not every change needs the same evidence: quick directional tests for iteration and data gathering, rigorous tests for ship decisions."* The same is true here — not every project needs SLSA L3.
