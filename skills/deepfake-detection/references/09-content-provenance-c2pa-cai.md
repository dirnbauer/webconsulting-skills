# 9. Content Provenance (C2PA / CAI)

Continues `deepfake-detection` from [full guide](full-guide.md).

## 9. Content Provenance (C2PA / CAI)

### C2PA Steering Committee (2026)

The Coalition for Content Provenance and Authenticity is governed by major technology and media companies:

| Member | Role |
|--------|------|
| **Adobe** | Founding member, CAI lead |
| **Amazon** | Cloud and AI integration (AWS, Titan) |
| **BBC** | Media organization representative |
| **Google** | Platform integration |
| **Meta** | Social platform adoption |
| **Microsoft** | Enterprise integration (365) |
| **OpenAI** | AI generator signing (DALL-E, ChatGPT) |
| **Publicis Groupe** | Advertising industry adoption |
| **Sony** | Hardware integration (cameras) |
| **Truepic** | Mobile authentication pioneer |

### Content Credentials: The CR Icon

**C2PA** is the technical standard. **Content Credentials** is the user-facing implementation with the visible "CR" icon.

| What the CR Icon Shows | Description |
|------------------------|-------------|
| **Creator** | Who created the media (camera, person, AI) |
| **Software** | What software was used for editing |
| **AI Disclosure** | Whether AI was used for generation |
| **Edit History** | What editing steps occurred |

> **Key Feature**: All assertions are cryptographically signed. Changing even **one pixel** invalidates the signature—manipulation is immediately detectable.

### Industry Adoption (2025-2026)

C2PA is rapidly becoming the industry standard. Current adoption landscape:

| Category | Adopters | Status |
|----------|----------|--------|
| **AI Generators** | DALL-E 3, Adobe Firefly, Google Gemini | Auto-sign all outputs |
| **Software** | Adobe Photoshop, Lightroom | Cryptographic edit history |
| **Professional Cameras** | Leica M11-P, Sony (select models) | Sign at capture |
| **Camera Manufacturers** | Nikon, Canon | Following (announced) |
| **Smartphones** | Google Pixel 10 (2025/26) | Native C2PA support |
| **Mobile OEMs** | Samsung Galaxy | Following (announced) |
| **Enterprise** | Microsoft 365 | Mandatory AI watermarks (2026) |

> **Prognosis (3-5 years)**: For media organizations and government agencies: Without cryptographic provenance, no file will be considered trustworthy.

### Content Authenticity Initiative (CAI) Integration

```json
{
  "claim": {
    "recorder": "Canon EOS R5",
    "signature": {
      "alg": "ES256",
      "cert": "-----BEGIN CERTIFICATE-----...",
      "sig": "base64_signature"
    },
    "assertions": [
      {
        "label": "c2pa.actions",
        "data": {
          "actions": [
            {
              "action": "c2pa.created",
              "when": "2026-01-20T14:32:00Z",
              "softwareAgent": "Canon DPP 4.17"
            }
          ]
        }
      }
    ]
  }
}
```

### Provenance Verification Workflow

```python
def verify_c2pa_provenance(media_path: str) -> dict:
    """
    Verify Content Authenticity Initiative (C2PA) manifests.
    
    C2PA provides cryptographic proof of media origin and edit history.
    """
    manifest = extract_c2pa_manifest(media_path)
    
    if not manifest:
        return {
            "has_provenance": False,
            "recommendation": "No cryptographic provenance available. Proceed with forensic analysis."
        }
    
    # Verify certificate chain
    cert_valid = verify_certificate_chain(manifest["signature"]["cert"])
    
    # Verify signature
    sig_valid = verify_signature(
        manifest["claim"],
        manifest["signature"]["sig"],
        manifest["signature"]["alg"]
    )
    
    # Check assertion integrity
    assertions_valid = verify_assertions(manifest["assertions"])
    
    return {
        "has_provenance": True,
        "certificate_valid": cert_valid,
        "signature_valid": sig_valid,
        "assertions_valid": assertions_valid,
        "edit_history": extract_edit_history(manifest),
        "original_device": manifest["claim"].get("recorder"),
        "overall_valid": all([cert_valid, sig_valid, assertions_valid])
    }
```

---
