# 7. Semantic Forensics (SemaFor)

Continues `deepfake-detection` from [full guide](full-guide.md).

## 7. Semantic Forensics (SemaFor)

When pixel-level artifacts are masked, focus on semantic inconsistencies. This approach was pioneered by the DARPA SemaFor program (2020-2024), which has since transitioned technologies to operational government use [[12, 13, 14]](#references).

### Cross-Modal Consistency Checks

| Check | Description | Example |
|-------|-------------|---------|
| Shadow Physics | Verify shadow directions match single light source | Multiple shadow angles in composite |
| Reflection Consistency | Check reflections match scene geometry | Eyes reflecting different scenes |
| Perspective Geometry | Verify vanishing points are consistent | Impossible architectural angles |
| Audio-Visual Sync | Lip movements match phoneme timing [[7, 8]](#references) | Desync in voice clone overlays |
| Temporal Plausibility | Metadata matches claimed time/location | Weather, daylight inconsistent with timestamp |

### Example: Shadow Analysis

```python
def analyze_shadow_consistency(image: np.ndarray) -> dict:
    """
    Detect physically impossible shadow configurations.
    
    A single light source produces shadows in consistent directions.
    Composited images often have inconsistent shadow angles.
    """
    shadows = detect_shadows(image)
    objects = detect_objects(image)
    
    shadow_vectors = []
    for obj, shadow in zip(objects, shadows):
        vector = compute_shadow_vector(obj, shadow)
        shadow_vectors.append(vector)
    
    # All vectors should converge to consistent light source
    consistency_score = measure_vector_convergence(shadow_vectors)
    
    return {
        "shadow_vectors": shadow_vectors,
        "consistency_score": consistency_score,
        "physically_plausible": consistency_score > 0.85
    }
```

---
