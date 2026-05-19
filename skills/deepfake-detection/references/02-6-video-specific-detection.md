# 6. Video-Specific Detection

Continues `deepfake-detection` from [full guide](full-guide.md).

## 6. Video-Specific Detection

Video deepfake detection requires analysis of temporal consistency, which current research shows remains challenging for generalization across different manipulation methods [[1, 4]](#references).

### Visual Detection Indicators (Human Review)

Before algorithmic analysis, trained reviewers check for these telltale signs:

| Indicator | What to Look For | Why It Happens |
|-----------|------------------|----------------|
| **Face Boundaries** | Flickering edges, face "floating" over body | Imperfect blending between swapped face and original |
| **Blinking** | No blinking, asymmetric blinking, stiff eyes | Early models lacked blink training; still imperfect |
| **Lip Sync** | Delays on plosives (p, b, m sounds) | Audio-visual alignment is computationally hard |
| **Shadows & Light** | Multiple shadow directions, inconsistent lighting | Composited elements from different light sources |
| **Eye Reflections** | Different scenes reflected in each eye | Synthesized eyes don't share real-world reflection |
| **Hair Details** | Smooth contours, "melting" strands, clipping | Fine details are hardest for generators |

> **Best Practice**: Slow down video to 25% speed and examine frame-by-frame. Artifacts become more visible when temporal smoothing is removed.

### Temporal Consistency Analysis

```python
def analyze_temporal_artifacts(video_path: str) -> dict:
    """
    Detect temporal inconsistencies in video deepfakes.
    
    Face-swap deepfakes often show:
    - Flickering at face boundaries
    - Inconsistent lighting between frames
    - Unnatural head pose transitions
    """
    frames = extract_frames(video_path)
    
    results = {
        "face_boundary_flickering": detect_boundary_flickering(frames),
        "lighting_consistency": analyze_lighting_consistency(frames),
        "pose_smoothness": measure_pose_transitions(frames),
        "blink_analysis": detect_blink_patterns(frames),  # Early deepfakes lacked blinking
        "audio_visual_sync": check_lip_sync_accuracy(video_path)
    }
    
    return results
```

### GAN & Diffusion Model Fingerprint Detection

Modern detection must address both GAN-based and diffusion model-generated images. Recent research demonstrates that diffusion models leave distinct artifacts detectable via uncertainty estimation [[5]](#references) and characteristic photorealism patterns [[6]](#references).

```python
def detect_gan_fingerprints(image: np.ndarray) -> dict:
    """
    Detect characteristic patterns left by generative architectures.
    
    Different families (StyleGAN, Stable Diffusion, DALL-E, Midjourney)
    leave distinct frequency-domain artifacts.
    """
    fft = compute_fft_spectrum(image)
    
    # GANs often produce checkerboard patterns in FFT
    checkerboard_score = detect_checkerboard_artifacts(fft)
    
    # Spectral analysis for GAN-specific signatures
    gan_signatures = match_known_gan_spectra(fft)
    
    return {
        "checkerboard_score": checkerboard_score,
        "suspected_generator": gan_signatures.get("best_match"),
        "confidence": gan_signatures.get("confidence")
    }
```

---
