# 5. Forensic Detection Criteria

Continues `deepfake-detection` from [full guide](full-guide.md).

## 5. Forensic Detection Criteria

### Criterion A: Sensor Fingerprints (PRNU/PCE)

Photo-Response Non-Uniformity (PRNU) is a sensor-specific noise pattern that acts as a biometric fingerprint for cameras.

#### Metric: Peak to Correlation Energy (PCE)

```python
# Conceptual PRNU/PCE calculation
def calculate_pce(image: np.ndarray, reference_prnu: np.ndarray) -> float:
    """
    Calculate Peak-to-Correlation-Energy for PRNU matching.
    
    Returns:
        PCE value > 60 indicates high confidence match
        PCE value 40-60 indicates moderate confidence
        PCE value < 40 indicates low confidence or mismatch
    """
    noise_residual = extract_noise_residual(image)
    correlation = correlate_2d(noise_residual, reference_prnu)
    peak = np.max(correlation)
    energy = np.mean(correlation**2)
    return peak**2 / energy
```

#### PRNU Limitations (Wronski Effect)

Modern computational photography (multi-frame capture, super-resolution) breaks the direct sensor-to-pixel mapping [[22, 23]](#references):

| Device Era | PRNU Reliability | Notes |
|------------|------------------|-------|
| Pre-2018 DSLRs | High | Direct sensor output |
| 2018-2022 Smartphones | Medium | Some computational processing |
| 2023+ Smartphones | Low | Heavy multi-frame HDR, AI enhancement |
| Synthetic (GAN/Diffusion) | None | No physical sensor involved |

### Criterion B: Noise-Intensity Relationship & IGH

The Intensity Gradient Histogram (IGH) classifies the relationship between local intensity and noise, exploiting Camera Response Function (CRF) physics.

```python
def analyze_igh_profile(image: np.ndarray) -> dict:
    """
    Analyze Intensity Gradient Histogram for CRF consistency.
    
    Synthetic blur (portrait mode) destroys the statistical harmony
    of the CRF model, detectable via IGH asymmetry analysis.
    """
    gradients = compute_intensity_gradients(image)
    
    # Authentic optical blur: asymmetric gradient distribution
    # Synthetic blur: symmetric Gaussian distribution
    symmetry_score = measure_gradient_symmetry(gradients)
    
    return {
        "gradient_histogram": gradients,
        "symmetry_score": symmetry_score,
        "classification": "authentic" if symmetry_score < 0.7 else "synthetic"
    }
```

### Criterion C: Geometric & Optical Blur Analysis

Physical law: Due to CRF non-linearity, optically blurred edges are asymmetric. Software Gaussian filters produce symmetric profiles.

| Blur Type | Gradient Profile | Detection Method |
|-----------|------------------|------------------|
| Optical (lens) | Asymmetric | IGH analysis |
| Digital (software) | Symmetric | IGH analysis |
| Depth-of-field (real) | Varies with distance | 3D consistency check |
| Portrait mode (fake) | Uniform application | Edge discontinuity detection |

### Criterion D: Compression Artifacts (Double JPEG / DQ)

Double Quantization (DQ) effects serve as primary evidence for multiple save operations, enabling splicing localization.

```python
def generate_dq_probability_map(image: np.ndarray) -> np.ndarray:
    """
    Generate Double Quantization probability map.
    
    Spliced regions show different quantization histories,
    creating detectable statistical anomalies.
    """
    dct_blocks = compute_dct_blocks(image)
    q_estimates = estimate_quantization_tables(dct_blocks)
    
    # Probability map highlights regions with different
    # compression histories (splicing indicators)
    prob_map = detect_quantization_inconsistencies(q_estimates)
    
    return prob_map  # Heatmap: red = likely manipulation
```

---
