# OpenSSF OSPS Baseline Levels (1/2/3)

> The OSPS Baseline is a **separate** framework from the original Best Practices Badge (Passing/Silver/Gold).
> Both frameworks are managed on the same bestpractices.dev platform but produce **different badges**.

## Overview

| Framework | Levels | Badge URL Pattern | Focus |
|-----------|--------|-------------------|-------|
| Best Practices | Passing, Silver, Gold | `/projects/{ID}/badge` | Project maturity & practices |
| OSPS Baseline | 1, 2, 3 | `/projects/{ID}/baseline` | Security posture (OSPS standard) |

**Both badges should be displayed** in your README. A project can achieve both simultaneously.

## Badge Display

```markdown
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/PROJECT_ID/badge)](https://www.bestpractices.dev/projects/PROJECT_ID)
[![OpenSSF Baseline](https://www.bestpractices.dev/projects/PROJECT_ID/baseline)](https://www.bestpractices.dev/projects/PROJECT_ID)
```

## Baseline Level 1 (Foundation)

Core security practices every project should meet.

### Access Control (OSPS-AC)

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-AC-01.01 | `osps_ac_01_01` | Multi-factor authentication for maintainers |
| OSPS-AC-02.01 | `osps_ac_02_01` | Defined roles with access control |
| OSPS-AC-03.01 | `osps_ac_03_01` | Enforce access control on repositories |

### Build & Release (OSPS-BR)

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-BR-01.01 | `osps_br_01_01` | Automated build process |
| OSPS-BR-02.01 | `osps_br_02_01` | Dependency management |
| OSPS-BR-03.01 | `osps_br_03_01` | Integrity verification for dependencies |

### Documentation (OSPS-DO)

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-DO-01.01 | `osps_do_01_01` | Security policy documented |
| OSPS-DO-02.01 | `osps_do_02_01` | Contribution guidelines |

### Governance (OSPS-GV)

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-GV-01.01 | `osps_gv_01_01` | Project governance documented |

### Legal (OSPS-LE)

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-LE-01.01 | `osps_le_01_01` | License clearly identified |

### Quality Assurance (OSPS-QA)

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-QA-01.01 | `osps_qa_01_01` | Automated testing exists |
| OSPS-QA-02.01 | `osps_qa_02_01` | Tests run in CI |
| OSPS-QA-03.01 | `osps_qa_03_01` | Static analysis in CI |

### Vulnerability Management (OSPS-VM)

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-VM-01.01 | `osps_vm_01_01` | Process for reporting vulnerabilities |
| OSPS-VM-02.01 | `osps_vm_02_01` | Dependency vulnerability monitoring |
| OSPS-VM-03.01 | `osps_vm_03_01` | Timely vulnerability response |

---

## Baseline Level 2 (Intermediate)

Builds on Level 1 with stronger controls.

### Additional Criteria

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-AC-01.02 | `osps_ac_01_02` | Phishing-resistant MFA (FIDO2/WebAuthn) |
| OSPS-AC-02.02 | `osps_ac_02_02` | Least privilege access |
| OSPS-BR-01.02 | `osps_br_01_02` | Reproducible builds or build provenance |
| OSPS-BR-02.02 | `osps_br_02_02` | Pinned dependencies |
| OSPS-DO-01.02 | `osps_do_01_02` | Security design documentation |
| OSPS-GV-01.02 | `osps_gv_01_02` | Succession planning |
| OSPS-QA-02.02 | `osps_qa_02_02` | Code coverage tracking |
| OSPS-QA-04.01 | `osps_qa_04_01` | Dynamic analysis / fuzz testing |
| OSPS-VM-02.02 | `osps_vm_02_02` | Automated vulnerability scanning |
| OSPS-VM-04.01 | `osps_vm_04_01` | Security advisories published |

---

## Baseline Level 3 (Advanced)

Highest security posture. Some criteria are challenging for solo maintainers.

### Additional Criteria

| Criterion | Field Name | Requirement |
|-----------|-----------|-------------|
| OSPS-BR-01.03 | `osps_br_01_03` | SLSA Level 3 provenance |
| OSPS-BR-03.02 | `osps_br_03_02` | Signed releases |
| OSPS-QA-05.01 | `osps_qa_05_01` | Architecture documentation |
| OSPS-QA-06.01 | `osps_qa_06_01` | Threat model documented |
| OSPS-QA-07.01 | `osps_qa_07_01` | Two-person review for changes |
| OSPS-VM-01.02 | `osps_vm_01_02` | Private vulnerability reporting |

### Solo Maintainer Blockers at Level 3

| Criterion | Issue | Mitigation |
|-----------|-------|------------|
| `OSPS-QA-07.01` | Requires two-person review | Same challenge as Gold `two_person_review`. Use automated review tools (Copilot, CodeQL) as compensating controls. Mark Unmet with justification. |

---

## Field Naming Convention

**CRITICAL**: The bestpractices.dev HTML forms use a different naming convention than the display names:

| Display Name | Form Field Name |
|-------------|----------------|
| `OSPS-AC-01.01` | `osps_ac_01_01_status` / `osps_ac_01_01_justification` |
| `OSPS-BR-03.02` | `osps_br_03_02_status` / `osps_br_03_02_justification` |

**Pattern**: Replace hyphens with underscores, dots with underscores, all lowercase.

When submitting programmatically, use the form field name format (e.g., `project[osps_ac_01_01_status]`).

---

## Relationship to Best Practices Badge

The two frameworks overlap significantly:

| OSPS Baseline | Overlaps With Best Practices |
|---------------|------------------------------|
| OSPS-AC-01.01 (MFA) | Gold: `require_2FA` |
| OSPS-QA-07.01 (Two-person review) | Gold: `two_person_review` |
| OSPS-VM-01.01 (Vuln reporting) | Passing: `vulnerability_report_process` |
| OSPS-BR-03.02 (Signed releases) | Silver: `signed_releases` |
| OSPS-QA-01.01 (Automated tests) | Passing: `test` |

**Tip**: If you've achieved Silver or Gold, most Baseline criteria are already Met. Focus on the non-overlapping OSPS-specific criteria.

---

## Checking Baseline Status

```bash
# Check current baseline level via API
curl -s "https://www.bestpractices.dev/projects/PROJECT_ID.json" | \
  jq '{badge_level, osps_baseline_level: .tiered_percentage}'

# Or with cache-busting
curl -s "https://www.bestpractices.dev/projects/PROJECT_ID.json?_=$(date +%s)" | \
  jq '{badge_level, osps_baseline_level: .tiered_percentage}'
```

---

## Resources

- [OSPS Baseline Standard](https://baseline.openssf.org/)
- [bestpractices.dev Baseline Criteria](https://www.bestpractices.dev/en/criteria)
- [OpenSSF Security Baseline](https://openssf.org/projects/security-baseline/)
