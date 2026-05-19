# 8. Authenticity Scoring System

Continues `deepfake-detection` from [full guide](full-guide.md).

## 8. Authenticity Scoring System

### Analysis Layer Weighting

Based on scientific reliability of each method (from webconsulting.at forensics research):

| Analysis Layer | Weight | Rationale |
|----------------|--------|-----------|
| **Signal Analysis** | 45% | Objective forensic signals: noise patterns, compression artifacts, frequency analysis. Hybrid approaches achieve F1 scores of 0.96 on benchmarks |
| **Metadata Analysis** | 35% | EXIF provenance chain. 62% of images have camera-specific signatures, 99% are manufacturer-identifiable |
| **Semantic Analysis** | 20% | AI-based artifact detection. Only 58% accuracy on standard benchmarks—OpenAI discontinued their detector in 2023 due to low accuracy |
| **C2PA (Bonus)** | +25-40 points | Cryptographic proof. Only unforgeable method. Combined with AI detection reduces false positives by 41% |

> **Important**: Without C2PA verification, maximum achievable grade is 2 ("No manipulation indicators"). Grade 1 ("Provenance cryptographically verified") requires a validated signature chain.

### Probability to Grade Mapping

| Authenticity % | Grade | Interpretation |
|----------------|-------|----------------|
| 90 - 100% | 1 (Excellent) | Evidence-based authenticity: Valid PRNU/PCE fingerprint; absence of DQ artifacts |
| 75 - 89% | 2 (Good) | Probably authentic: Consistent IGH profiles; minor deviations from standard compression |
| 50 - 74% | 3 (Satisfactory) | Hybrid content detected: Requires human-in-the-loop verification |
| 35 - 49% | 4 (Adequate) | Significant statistical anomalies: Noise profile inconsistencies indicate local editing |
| 20 - 34% | 5 (Poor) | High manipulation probability: Positive splicing detection via DQ maps |
| < 20% | 6 (Fail) | Confirmed forgery: Forensic evidence of synthetic generation (GAN fingerprints) or physical impossibilities |

### Composite Scoring Algorithm

```python
def calculate_authenticity_score(media_path: str) -> dict:
    """
    Calculate composite authenticity score from multiple forensic signals.
    """
    image = load_media(media_path)
    
    scores = {
        "prnu_pce": analyze_prnu(image),           # Weight: 0.25
        "igh_profile": analyze_igh_profile(image), # Weight: 0.20
        "dq_artifacts": detect_dq_artifacts(image), # Weight: 0.20
        "gan_fingerprints": detect_gan_fingerprints(image), # Weight: 0.15
        "semantic_consistency": check_semantic_consistency(image), # Weight: 0.20
    }
    
    weights = [0.25, 0.20, 0.20, 0.15, 0.20]
    composite = sum(s * w for s, w in zip(scores.values(), weights))
    
    return {
        "authenticity_probability": composite,
        "grade": map_to_grade(composite),
        "detailed_scores": scores,
        "confidence_interval": calculate_confidence(scores)
    }
```

---
