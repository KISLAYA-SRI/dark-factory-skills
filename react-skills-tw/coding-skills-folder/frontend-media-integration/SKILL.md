---
name: frontend-media-integration
description: Use whenever a component renders images, video, documents, or icons — applies the project DAM and media-delivery rules (Sitecore Media Library ownership, Layout Service asset references, CDN delivery, Next.js image optimisation, responsive sizing, lazy loading, prop-driven src/alt/dimensions). Invoked conditionally from presentational-ui-generation only when assets are present. Triggers include image handling, media, DAM, video, asset URLs, or next/image.
disable-model-invocation: true
---

## Frontend Media Integration

### Purpose

Apply the project's Digital Asset Management (DAM) and media-delivery rules whenever a component renders media.

⚠️ **Invoked conditionally from `presentational-ui-generation`** — only when the component actually renders images, video, or documents (e.g. hero banner background, carousel slides). **Skip entirely for media-free components.**

---

## Media Delivery Architecture

```text
Sitecore Media Library  → owns the asset (single source of truth)
Layout Service          → provides the asset reference (URL, alt, dimensions)
CDN (Cloudflare)        → delivers the optimised asset
Component               → receives src/alt/dimensions as PROPS (never hardcoded)
```

### Source of Truth

- **Sitecore Media Library** is the single source of truth for all digital assets — images, documents, standard media
- Content authors manage assets within Sitecore; content items reference them through Sitecore content APIs
- The frontend consumes **Sitecore-generated media URLs** during page rendering
- Media references resolve through the **Layout Service**, so components render assets without additional transformation or custom media APIs

### CDN Delivery (Mandatory)

All media assets **MUST** be delivered through the CDN layer (Cloudflare) rather than directly from the Sitecore origin.

This provides: reduced latency via edge caching · improved global performance · lower load on Sitecore CD infrastructure · better scalability during peak traffic.

- ❌ **Never** bypass the CDN for media delivery — all asset URLs must point to the CDN endpoint
- ❌ **Never** hardcode media URLs — consume them from the Layout Service response
- ❌ **Never** create custom media transformation layers or custom media APIs

---

## Image Rules

- ✅ Use the **Next.js Image component** (or the project wrapper) for all raster images to leverage built-in optimisation
- ✅ Provide explicit `width`/`height` (or `fill` + a sized container) to prevent layout shift
- ✅ Always provide meaningful `alt` — empty `alt=""` only for decorative images
- ✅ Implement **responsive image sizing** via `sizes`/`srcset` per breakpoint; serve appropriately scaled assets from the CDN
- ✅ **Lazy-load** below-the-fold images; eager-load only the LCP/hero image when the design requires it
- ✅ Use modern image formats (WebP, AVIF) when supported
- ✅ Optimise images to improve Core Web Vitals (LCP, CLS)
- ✅ `src`, `alt`, `width`, `height`, and `priority` all come from props/CMS fields

- ❌ **Never** load full-resolution images for mobile viewports
- ❌ **Never** skip lazy loading for images below the fold
- ❌ **Never** use unoptimised image formats
- ❌ **Never** render raster images with a plain `<img>` when the project provides optimisation
- ❌ **Never** omit dimensions and cause layout shift

---

## Video Rules

- Reference video via the CMS/CDN URL passed as a prop
- Provide a **poster image**, captions/track where available, and sensible `preload`
- Respect `prefers-reduced-motion` for autoplaying/looping background video — provide a non-motion fallback
- ❌ **Never** autoplay with sound

---

## Document / File Assets

- Link documents via the CDN/Media Library URL from props
- Show file type and, if provided, size
- Open/download behaviour per the design
- Accessible link text — never "click here"

---

## Icons

- Use the **design-system icon set** — icons are prop-driven (name/variant), not inline hardcoded SVG copies
- Wrap direct SVGs in `Icon.tsx` as a child, or pass the icon name to `Icon.tsx` from Atoms
- For icons inside buttons, use `IconButton` from Atoms
- Sitecore provides the icon name to `Button`'s `leadingIcon` / `trailingIcon` props, or to `IconButton`

```text
Icons are picked from public/icons/
  Default:        line.svg
  Selected state: fill.svg

Sitecore provides name 'eye' → public/icons/eye/line.svg
```

- Decorative icons: `aria-hidden`
- Meaningful icons: accessible labels
- ❌ **Never** inline a one-off SVG when a design-system icon exists

---

## RTL & Localisation

- Mirror **directional** media controls under RTL (e.g. carousel next/prev arrows) — `rtl:rotate-180`
- ❌ Do **not** mirror neutral icons (eye, help, search, calendar)
- ❌ Do **not** mirror symmetric/decorative icons (close ✕, check ✓, warning ⚠)
- ❌ Do **not** mirror brand logos, ever
- Alt/caption text is localised and passed in — never hardcoded

---

### Gate: Complete When

```text
- [ ] All media rendered via optimised delivery (next/image or project wrapper)
- [ ] src/alt/dimensions supplied as props/CMS fields — no hardcoded URLs
- [ ] All asset URLs point to the CDN, not the Sitecore origin
- [ ] Explicit dimensions or sized container prevent layout shift
- [ ] Responsive sizing (sizes/srcset) applied per breakpoint
- [ ] Lazy loading applied; only hero/LCP image eager-loaded
- [ ] Video posters/captions + reduced-motion fallback where applicable
- [ ] Icons sourced from the design-system set with correct line/fill variant
- [ ] Decorative vs meaningful media distinguished for accessibility
- [ ] Directional media controls mirrored in RTL; neutral/symmetric icons not mirrored
```

### Never Do

- Never hardcode asset URLs in components.
- Never bypass the CDN for media delivery.
- Never create custom media transformation layers or media APIs.
- Never render raster images with a plain `<img>` when optimisation is available.
- Never omit dimensions and cause layout shift.
- Never load full-resolution images for mobile viewports.
- Never skip lazy loading for below-the-fold images.
- Never autoplay video with sound or ignore reduced-motion.
- Never inline one-off SVGs when a design-system icon exists.
- Never mirror neutral icons, symmetric icons, or brand logos in RTL.
- Never hardcode alt or caption text.
