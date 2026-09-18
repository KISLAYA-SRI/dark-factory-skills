# Frontend Media Integration

Applies the project DAM and media-delivery rules whenever a component renders images, video, documents, or icons — Sitecore Media Library ownership, Layout Service asset references, CDN delivery, Next.js image optimization, responsive sizing, lazy loading, and prop-driven src/alt/dimensions.

## Use This For

- Handling images/video/documents/icons in a component (nested in Phase 4).
- Applying Next.js image optimization and responsive sizing.
- Preventing layout shift and ensuring accessible media.
- Keeping asset references prop-driven from the CMS/CDN.

## Expected Flow

```text
Detect media in component
  → Reference asset via CMS/CDN URL passed as prop
  → Render via next/image (or project wrapper) with explicit dimensions
  → Apply responsive sizing + lazy loading (hero/LCP eager only)
  → Handle video posters/captions + reduced-motion
  → Distinguish decorative vs meaningful for a11y
```

## Key Rules

- Never hardcode asset URLs — src/alt/dimensions come from props/CMS fields.
- Always provide explicit dimensions or a sized container to prevent layout shift.
- Lazy-load below-the-fold media; eager-load only the LCP/hero image.
- Respect prefers-reduced-motion; never autoplay video with sound.
- Skip this skill entirely for media-free components.

See [SKILL.md](./SKILL.md) for the full instructions.
