# 11. Defense Strategies

Continues `deepfake-detection` from [full guide](full-guide.md).

## 11. Defense Strategies

### Technical Controls

| Control | Implementation | Effectiveness |
|---------|----------------|---------------|
| C2PA/CAI Validation | Require provenance for high-stakes media | High (when available) |
| Automated Screening | Deploy detection pipeline for inbound media | Medium (arms race) |
| Multi-Signal Fusion | Combine PRNU, IGH, DQ, semantic signals | High |
| Human-in-the-Loop | Expert review for Grade 3-4 cases | High |

### Organizational Inoculation

1. **Pre-bunking**: Educate stakeholders about deepfake capabilities before exposure
2. **Source Triangulation**: Verify claims through multiple independent sources
3. **Temporal Delay**: Wait for verification before amplifying uncertain content
4. **Provenance Requirement**: Mandate C2PA for critical communications

### Response When Targeted (Personal Deepfakes)

If you or your client are depicted in a deepfake:

| Step | Action | Details |
|------|--------|---------|
| 1 | **Preserve Evidence** | Screenshot with timestamp, save URL, download file |
| 2 | **Platform Takedown** | Report to platform using manipulation/deepfake reporting tools |
| 3 | **Legal Assessment** | Consult attorney for jurisdiction-specific remedies |
| 4 | **Support Resources** | Contact victim support organizations |

#### Legal Framework (Austria)

| Statute | Protection | Application |
|---------|------------|-------------|
| **§ 78 UrhG** | Recht am eigenen Bild (Right to own image) | Unauthorized use of likeness |
| **§ 107c StGB** | Cybermobbing | Persistent harassment via digital means |
| **§ 120a StGB** | Unbefugte Bildaufnahmen | Intimate imagery without consent |

**Austrian Resources**:
- [Saferinternet.at Helpline](https://www.saferinternet.at/helpline) - Expert counseling
- [Saferinternet.at Unterrichtsmaterialien](https://www.saferinternet.at/zielgruppen/lehrende) - Teaching materials ("Wahr oder falsch im Internet")
- Rat auf Draht: **147** (24/7 hotline for young people)
- Internet Ombudsstelle: [ombudsstelle.at](https://www.ombudsstelle.at)

> **Note**: Similar protections exist across EU member states under the Digital Services Act (DSA) and GDPR. Consult local counsel for jurisdiction-specific advice.

### Detection Pipeline Example

```python
class MediaAuthenticationPipeline:
    """
    Production pipeline for automated media authentication.
    """
    
    def __init__(self, config: PipelineConfig):
        self.prnu_analyzer = PRNUAnalyzer(config.prnu_db)
        self.igh_classifier = IGHClassifier(config.igh_model)
        self.dq_detector = DQDetector()
        self.gan_detector = GANFingerprintDetector(config.gan_signatures)
        self.semantic_analyzer = SemanticAnalyzer(config.llm_endpoint)
        self.c2pa_validator = C2PAValidator(config.trusted_roots)
    
    async def authenticate(self, media_path: str) -> AuthenticationResult:
        # Check provenance first (fast path)
        provenance = await self.c2pa_validator.verify(media_path)
        if provenance.valid:
            return AuthenticationResult(
                authentic=True,
                confidence=0.99,
                method="cryptographic_provenance"
            )
        
        # Run forensic analysis in parallel
        results = await asyncio.gather(
            self.prnu_analyzer.analyze(media_path),
            self.igh_classifier.classify(media_path),
            self.dq_detector.detect(media_path),
            self.gan_detector.detect(media_path),
            self.semantic_analyzer.analyze(media_path)
        )
        
        # Fuse signals
        composite = self.fuse_signals(results)
        
        return AuthenticationResult(
            authentic=composite.score > 0.75,
            confidence=composite.confidence,
            grade=composite.grade,
            details=results,
            method="forensic_analysis"
        )
```

---
