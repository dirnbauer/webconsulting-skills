# 10. Forensic Report Template

Continues `deepfake-detection` from [full guide](full-guide.md).

## 10. Forensic Report Template

### Module A: Media Metadata & Summary

```markdown
# Media Authentication Report

## Metadata
| Field | Value |
|-------|-------|
| Report ID | MAR-2026-001 |
| Classification | Confidential |
| Analysis Date | 2026-01-23 15:00 UTC |
| Media Type | Video (MP4) |
| Duration | 00:02:34 |
| Resolution | 1920x1080 |
| File Hash (SHA-256) | a1b2c3d4... |
| Lead Analyst | Forensic AI Agent |

## Executive Summary (max 200 words)

Analysis of [MEDIA_FILE] reveals [AUTHENTICITY_ASSESSMENT].
Key findings include [PRIMARY_INDICATORS]. The composite authenticity
score is [SCORE]% (Grade: [GRADE]). [RECOMMENDATION].

## Authenticity Assessment
| Criterion | Score | Status |
|-----------|-------|--------|
| PRNU/PCE Match | 45/100 | ⚠️ Inconclusive |
| IGH Profile | 82/100 | ✅ Consistent |
| DQ Artifacts | 23/100 | ❌ Detected |
| GAN Fingerprints | 15/100 | ❌ Detected |
| Semantic Consistency | 67/100 | ⚠️ Minor issues |
| **Composite Score** | **34%** | **Grade: 5** |
```

### Module B: Technical Evidence

```markdown
## Technical Analysis

### PRNU/PCE Analysis
- Reference device: Not identified
- PCE Value: 23.4 (below threshold of 40)
- Interpretation: Cannot establish camera origin

### Double Quantization Map
![DQ Probability Map](dq_map.png)
- Red regions indicate areas with different compression histories
- Face region shows 89% probability of splicing

### GAN Fingerprint Analysis
- Checkerboard artifacts: Detected (FFT analysis)
- Suspected generator: StyleGAN2-derived architecture
- Confidence: 78%

### Semantic Inconsistencies
1. Shadow direction: Inconsistent (2 apparent light sources)
2. Eye reflections: Different scene reflected in each eye
3. Audio-visual sync: 120ms average desync detected
```

---
