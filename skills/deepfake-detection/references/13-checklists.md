# 13. Checklists

Continues `deepfake-detection` from [full guide](full-guide.md).

## 13. Checklists

### Pre-Analysis Checklist

- [ ] Obtain original file (avoid screenshots, re-uploads)
- [ ] Preserve file hash (SHA-256) for chain of custody
- [ ] Document source and context of media
- [ ] Check for C2PA/CAI provenance data
- [ ] Identify claimed device/source for PRNU matching

### Analysis Checklist

- [ ] Run PRNU/PCE analysis (if reference available)
- [ ] Generate IGH profile and classify blur types
- [ ] Create DQ probability map for splicing detection
- [ ] Analyze for GAN fingerprints (FFT spectrum)
- [ ] Check semantic consistency (shadows, reflections, physics)
- [ ] For video: temporal consistency, audio-visual sync
- [ ] Calculate composite authenticity score

### Reporting Checklist

- [ ] Document all findings with confidence levels
- [ ] Include visualizations (DQ maps, FFT spectra)
- [ ] Provide grade interpretation with caveats
- [ ] List limitations of analysis
- [ ] Recommend human review for borderline cases

---
