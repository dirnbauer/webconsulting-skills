# 8. Multimedia Optimization

Continues `ai-search-optimization` from [full guide](full-guide.md).

## 8. Multimedia Optimization

### Image Requirements

Perplexity and other AI engines prefer visual content:

```html
<figure>
    <img 
        src="/images/ai-search-diagram.webp" 
        alt="Diagram showing how AI search engines process and cite content"
        width="800"
        height="450"
        loading="lazy"
    />
    <figcaption>
        How AI search engines extract and cite content sources
    </figcaption>
</figure>
```

**Best practices:**
- Minimum 2 unique, relevant images per article
- Descriptive alt text (not keyword stuffing)
- WebP format for performance
- Include diagrams, infographics, process flows
- Add captions with context

### Video Integration

```html
<figure class="video-embed">
    <iframe 
        src="https://www.youtube.com/embed/VIDEO_ID"
        title="Detailed explanation of AI Search Optimization"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media"
        allowfullscreen
    ></iframe>
    <figcaption>
        Video: Complete guide to optimizing for AI search engines
    </figcaption>
</figure>
```

### Video Schema

```json
{
    "@context": "https://schema.org",
    "@type": "VideoObject",
    "name": "AI Search Optimization Tutorial",
    "description": "Learn how to optimize content for ChatGPT, Perplexity, and Google AI",
    "thumbnailUrl": "https://example.com/video-thumbnail.jpg",
    "uploadDate": "2025-01-15",
    "duration": "PT10M30S",
    "contentUrl": "https://example.com/videos/ai-search-tutorial.mp4"
}
```
