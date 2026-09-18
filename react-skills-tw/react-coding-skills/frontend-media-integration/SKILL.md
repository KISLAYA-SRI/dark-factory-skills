---
name: frontend-media-integration
description: Use whenever a component renders images, video, documents, or icons — applies the project DAM and media-delivery rules (Sitecore Media Library ownership, Layout Service asset references, CDN delivery, Next.js image optimization, responsive sizing, lazy loading, prop-driven src/alt/dimensions). Triggers include image handling, media, DAM, video, asset URLs, or next/image.
disable-model-invocation: true
---

## Frontend Media Integration

### Purpose

Apply the project's Digital Asset Management (DAM) and media-delivery rules whenever a component renders media. Invoked nested from `presentational-ui-generation` only when assets are present (e.g. hero banner background, carousel slides). Skip entirely for media-free components.

### Source of Truth

```text
Sitecore Media Library → owns the asset
Layout Service         → provides the asset reference (URL, alt, dimensions)
CDN                    → delivers the optimized asset
Component              → receives src/alt/dimensions as PROPS (never hardcoded)
```

### Image Rules

- Use the project's Next.js image optimization (`next/image` or the project wrapper) for raster images.
- Provide explicit `width`/`height` (or fill + sized container) to prevent layout shift.
- Always provide meaningful `alt` (empty `alt=""` only for decorative images).
- Responsive sizing via `sizes`/`srcset` per breakpoint; serve appropriately scaled assets from the CDN.
- Lazy-load below-the-fold images; eager-load only the LCP/hero image when the design requires it.
- `src`, `alt`, `width`, `height`, and `priority` all come from props/CMS fields — no hardcoded asset URLs.

### Video Rules

- Reference video via the CMS/CDN URL passed as a prop.
- Provide poster image, captions/track where available, and `preload` sensibly.
- Respect `prefers-reduced-motion` for autoplaying/looping background video; provide a non-motion fallback.
- Never autoplay with sound.

### Document / File Assets

- Link documents via the CDN/Media Library URL from props; show type and (if provided) size.
- Open/download behaviour per the design; accessible link text (not "click here").

### Icons

- Use the design-system icon set; icons are prop-driven (name/variant), not inline hardcoded SVG copies.
- Decorative icons `aria-hidden`; meaningful icons have accessible labels.

### RTL & Localisation

- Mirror directional media/controls under RTL (e.g. carousel arrows).
- Alt/caption text is localised and passed in — never hardcoded.

### Gate: Complete When

```text
- [ ] All media rendered via optimized delivery (next/image or project wrapper).
- [ ] src/alt/dimensions supplied as props/CMS fields — no hardcoded URLs.
- [ ] Explicit dimensions or sized container prevent layout shift.
- [ ] Responsive sizing + lazy loading applied (hero/LCP eager only).
- [ ] Video posters/captions + reduced-motion fallback where applicable.
- [ ] Decorative vs meaningful media distinguished for accessibility.
```

### Never Do

- Never hardcode asset URLs in components.
- Never render raster images with a plain `<img>` when the project provides optimization.
- Never omit dimensions and cause layout shift.
- Never autoplay video with sound or ignore reduced-motion.
- Never inline one-off SVGs when a design-system icon exists.
