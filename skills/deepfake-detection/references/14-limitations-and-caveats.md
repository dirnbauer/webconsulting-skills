# 14. Limitations & Caveats

Continues `deepfake-detection` from [full guide](full-guide.md).

## 14. Limitations & Caveats

### Known Detection Challenges

| Challenge | Impact | Mitigation |
|-----------|--------|------------|
| Computational imaging (HDR+, Night Sight) | Destroys PRNU | Rely on semantic analysis |
| Social media compression | Removes fine artifacts | Focus on coarse-grained signals |
| Adversarial attacks on detectors | Evades specific models | Multi-model ensemble |
| Rapid GAN evolution | Outdated fingerprints | Continuous model updates |
| **Metadata stripping** | Screenshots, re-uploads remove C2PA | Invisible watermarks coupled with C2PA |

> **C2PA Challenge**: Screenshots and social media uploads can strip metadata ("stripping attack"). The industry is developing invisible watermarks that survive re-encoding and link back to C2PA manifests.

### Ethical Considerations

1. **False Positives**: Incorrectly flagging authentic media can cause harm
2. **Dual Use**: Detection research enables better synthesis
3. **Automation Bias**: Over-reliance on automated verdicts
4. **Privacy**: PRNU databases can identify individuals

### The Liar's Dividend

> The mere existence of deepfakes allows bad actors to dismiss authentic evidence as fake. Detection tools must be communicated carefully to avoid amplifying this effect.

---
