# 12. Tool & Dataset References

Continues `deepfake-detection` from [full guide](full-guide.md).

## 12. Tool & Dataset References

### Detection Tools

| Tool | Type | Description |
|------|------|-------------|
| [FaceForensics++](https://github.com/ondyari/FaceForensics) | Dataset & Benchmark | Standard deepfake detection benchmark |
| [Sensity](https://sensity.ai/) | Commercial | Enterprise deepfake detection API |
| Microsoft Video Authenticator | Tool | Frame-by-frame manipulation scoring (announced 2020; never generally released, discontinued) |
| [C2PA Tool](https://github.com/contentauth/c2pa-rs/tree/main/cli) | CLI | Content provenance verification |
| [Content Credentials Verify](https://contentcredentials.org/verify) | Web | Online C2PA verification (CAI) |
| [webconsulting Forensik-Tool](https://www.webconsulting.at/blog/deepfakes-erkennen-verstehen) | Web | Multi-layer analysis (EXIF, C2PA, Signal, AI) |

### Reference Datasets

| Dataset | Content | Use Case |
|---------|---------|----------|
| DARPA MediFor | Multi-modal manipulation | Comprehensive forensic training |
| DARPA SemaFor | Semantic manipulation | Semantic consistency models |
| Google/Jigsaw DeepFake | Face-swap videos | Video deepfake detection |
| Facebook DFDC | Diverse deepfakes | Large-scale detection training |
| StyleGAN2 FFHQ | Synthetic faces | GAN fingerprint analysis |

### Industry Standards

- **C2PA (Coalition for Content Provenance and Authenticity)**: Cryptographic media provenance
- **CAI (Content Authenticity Initiative)**: Adobe-led provenance standard
- **IPTC Photo Metadata**: Standard metadata for photographic content

---
