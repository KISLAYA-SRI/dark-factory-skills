---
name: presentational-ui-generation
description: Use to generate the prop-driven React presentation layer — design-system atoms/molecules/organisms, feature display components, and views — with typed props, typed callbacks, visual state shells, responsive/RTL/accessibility implementation, and design-token mapping applied as one unified lens. Optimised for Presentational components (hero banner, hero carousel) that need NO API, mappers, services, or state stores. Triggers include UI generation, presentational component, display component, prop-driven UI, responsive implementation, Figma to code, design tokens, RTL, or generate the UI for a component.
disable-model-invocation: true
---

## Presentational UI Generation

### Purpose

Generate ONLY the presentation layer: stateless, prop-driven React components that render data passed in and raise typed callbacks. This is the primary build step for **Presentational** stories and the UI foundation for **Transactional** stories (logic is layered on later by other skills).

⚠️ **This skill embeds the complete project responsive, RTL, accessibility, token and Tailwind rules.** They are applied as a **single unified lens** simultaneously with every component — not as separate sequential passes. Skipping any step in the Unified Implementation Lens is a violation.

### Scope Boundary (Critical)

**Generate:**
- Design-system atoms, molecules, organisms.
- Feature display components and view/layout components.
- Typed Props interfaces and typed callback signatures.
- Visual state shells (loading skeleton, empty, error display) driven by props — NOT by data fetching.
- Accessibility contract (roles, labels, keyboard handlers, focus order).
- Responsive + RTL implementation with full token mapping.
- Barrel exports.

**Never generate here:**
- API calls, `fetch`, TanStack Query, hooks that fetch.
- Mappers, services, view-model transforms.
- Sitecore field extraction.
- Zustand stores / shared state.
- Business validation or persona/session logic.

> The moment a component needs data or business logic, it stops being this skill's job — the container/logic skills wire that in and pass results down as props.

### Presentational Path — Keep It Lean (Do Not Over-Engineer)

A Presentational component (e.g. hero banner, hero carousel) is plainly a UI component with interaction/effects only. For these:

- Build a **single component file** (plus sub-parts only if the hierarchy in the plan requires them).
- Local interaction state via `useState` / `useRef` is fine (carousel index, hover, expanded).
- **Do NOT** create a container, hook file, service, mapper, or store.
- **Do NOT** invoke `frontend-logic-integration`, `frontend-state-and-form-management`, or `sitecore-rendering-integration` unless the plan explicitly marks the component Transactional/Hybrid or CMS-mapped.
- Effects (autoplay, transitions, parallax) live inside the component using standard React + CSS/transition utilities.

```text
Hero carousel (Presentational) → ONE organism component:
  props: slides[], activeIndex?, autoPlayMs?, onSlideChange?
  local state: current index, paused-on-hover
  no API, no store, no mapper — done.
```

---

## SECTION A — UNIFIED IMPLEMENTATION LENS (MANDATORY)

This defines the **single, unified mandatory process** for reading Figma context and applying all responsive, RTL, accessibility, and design-system rules **simultaneously** during implementation. These are not separate sequential checks — they are one integrated lens applied to every component at the same time.

### Step 1 — Locate and Read All Context Sources

Before writing any component code, read ALL of the following completely (If these files were read earlier in contract loader phase then reuse the same content):

| Source | Use For |
| --- | --- |
| **Responsive Reconciliation JSON** (`responsive_design_intent.json`) | **Authoritative contract** for ALL responsive behaviour when present |
| **Desktop Figma context JSON** | Detail reference only — primitive names, variants, token names, labels, icon names, states |
| **Mobile Figma context JSON** | Detail reference only — same purposes as Desktop |

**Critical reading order when `responsive_design_intent.json` EXISTS:**
1. Read reconciliation JSON → extract the full responsive implementation contract
2. Read Desktop + Mobile Figma JSONs → extract implementation **details only**
3. Apply the rules in Sections B–H below

**Critical reading order when it does NOT exist:**
1. Read Desktop + Mobile Figma JSONs → reconcile layout differences yourself
2. Apply the rules in Sections B–H below

⚠️ **When `responsive_design_intent.json` exists:** Do NOT compare Mobile and Desktop Figma JSONs to derive responsive rules. Do NOT override `sharedComponents`, `breakpointSpecificComponents`, `layoutRules`, or `keyResponsiveDifferences`. The reconciliation has already been done — implement it directly.

Do not proceed until all applicable sources are loaded into working context.

### Step 2 — Build a Unified Component Implementation Map

For each component, build a **single unified map** capturing Figma values and their project-standard token equivalents together. **Do not implement any component without completing its map first.**

```text
Component: ClaimCard
  ── Figma ──────────────────────────────────────────────────────────────
  Desktop Figma Node: [node id / path in JSON]
  Mobile Figma Node:  [node id / path in JSON]
  Desktop Layout:     flex-row, gap-4, padding-6
  Mobile Layout:      flex-col, gap-3, padding-4
  Typography:         title → heading4, subtitle → body-medium-regular
  Colours:            background → bg-background-primary, border → border-base-default
  Visual States:      default, disabled, loading skeleton
  ── Project Rules Applied ──────────────────────────────────────────────
  Responsive:         Mobile-first base; lg: overrides for desktop; Grid for page layout
  RTL:                Logical CSS (ps-*, pe-*, ms-*, me-*); directional icon handling
  Accessibility:      Semantic HTML, ARIA roles/labels, keyboard navigability, focus states
  Tokens:             All spacing/typography/colour/radius/shadow mapped to tokens
  Tailwind:           cn() for class composition; classes derived from theme-block.css tokens
```

### Step 3 — Map ALL Figma Values to Design Tokens

**Do NOT hardcode any value from Figma.** Every value must map to a project design token:

| Figma Value Type | Mapping Rule |
| --- | --- |
| Colour (hex/rgba) | Semantic colour token (`--color-*`, `--text/base/*`, `--border/base/*`) |
| Spacing (px) | Spacing token class (`p-*`, `m-*`, `--spacing/*`) |
| Gap (px) | Gap token class (`gap-*`, `--gap/*`) |
| Typography (size, weight) | Typography token class (`heading*`, `body-*`, `--typography/*`) |
| Border radius (px) | Radius token (`rounded-primitive-radius-*`) |
| Shadow | Shadow token (`shadow-*`) |
| Border width/colour | Border token (`border-*`, `--border/base/*`) |

⚠️ **If no exact token exists:** use the closest token and **record the discrepancy as a gap**. Where the guideline requires it, create the primitive value and **call out all new tokens in the coding agent summary document**.

### Steps 4–8

Step 4 (responsive layout) → **Section B**. Step 5 (RTL) → **Section E**. Step 6 (accessibility) → **Section F**. Step 7 (Tailwind/design system) → **Sections C–D**. Step 8 (visual states) → **Section G**.

### Step 9 — Record Discrepancies

Record any discrepancy between Figma, the Analysis Plan, or project rules:

```text
Discrepancy Log:
- Component: ClaimCard
  Issue: Figma shows 3-column grid on desktop; ANALYSIS_PLAN describes 2-column
  Resolution: Implemented Figma (3-column) as visual source of truth
- Component: ClaimCard
  Issue: No exact spacing token for 18px gap found in theme-block.css
  Resolution: Used closest token (spacing-m = 16px); recorded as gap
```

---

## SECTION B — RESPONSIVE IMPLEMENTATION

### Design References

```text
Mobile:  390px
Desktop: 1700px
```

### One Responsive Implementation (Default)

When mobile and desktop represent the same logical experience, generate **one** responsive component — never separate mobile and desktop implementations unless the reconciliation explicitly requires breakpoint-specific subcomponents.

```text
Preferred pattern:
FeaturePage
  FeatureLayoutShell
    ResponsiveHeader (or breakpoint-specific Header variants)
    SharedFeatureContent
    SharedFooter
    DesktopOnlySupportingPanel, if applicable
```

Do not duplicate full page markup only to handle layout differences.

### Mobile-First Class Application

- **Base classes** (no prefix) apply to mobile (390px)
- **Breakpoint prefixes** (`lg:`) override base classes at larger screens

| Requirement | Implementation |
| --- | --- |
| Mobile fill/stretch | `w-full` |
| Desktop fixed width | `w-full lg:max-w-[1700px]` — prefer `max-w-*` over hard `w-*` |
| Desktop split layouts | `grid grid-cols-1 lg:grid-cols-2` or `flex flex-col lg:flex-row` |
| Layout direction change | Explicit: `flex-col lg:flex-row` |
| Absolute positioning | Avoid unless reconciliation requires it |

### Grid Component Usage

`Grid` / `GridItem` provide a responsive grid system based on Figma specs with automatic mobile-first behaviour.

**Figma specifications:**
- **Mobile (390px):** 4 columns, 8px gutter (`gap-2`), 16px margins (`px-4`)
- **Desktop (1700px):** 12 columns, 24px gutter (`gap-6`), 64px margins (`px-16`)

**Automatic behaviour:**
- `columns={4}` → mobile specs (4 cols, gap-2, px-4, max-w-[390px])
- `columns={12}` → responsive specs (mobile 4 cols → desktop 12 cols with Figma gutters/margins)

```tsx
import { Grid, GridItem } from "@dxp/design-system";

// Responsive grid (mobile: 4 cols → desktop: 12 cols)
<Grid>
  <GridItem span={4}>Column 1</GridItem>
  <GridItem span={4}>Column 2</GridItem>
  <GridItem span={4}>Column 3</GridItem>
</Grid>

// Mobile-only grid
<Grid columns={4}>
  <GridItem span={2}>Half width</GridItem>
  <GridItem span={2}>Half width</GridItem>
</Grid>
```

**Key props:** `columns` (1–12) · `gap` · `align` · `justify` · `container`

⚠️ **Important rules:**
- Use `columns={12}` for responsive layouts — automatically handles mobile → desktop
- Use `columns={4}` for mobile-only layouts
- **No manual responsive classes needed** — Grid handles `lg:grid-cols-12`, `lg:gap-6`, `lg:px-16` automatically
- Override `gap` only when needed — Figma specs applied by default
- `GridItem span` is responsive via Tailwind classes (e.g. `className="col-span-4 lg:col-span-6"`)

### Internal Responsiveness — Flex vs Local Grid

Components should be responsive within the space given by their parent. **Do not use the page-level grid inside every component.**

**Use `flex` for arranging content in one direction:**
Icon + text rows · title + action · button groups · file card rows · tags/chips · simple text + image alignment · internal content of a single card

**Use local `grid` for repeated or structured blocks:**
Video card lists · topic card lists · feature tiles · product cards · form field groups · data summary blocks

```text
✅ A single VideoCard uses flex/block internally for thumbnail, play icon, date, title
❌ A single VideoCard should NOT use grid just because it is part of a grid
✅ The parent VideoList uses local grid to arrange multiple VideoCard items
```

### Width and Sizing Rules

- Mobile full-width sections → `w-full`
- Desktop fixed form widths → become `max-width` with `w-full`
- Images/ad panels filling desktop space → responsive `object-fit`
- Use `min-h`, `max-h`, `min-w`, `max-w` only where needed
- Avoid hardcoded viewport-relative hacks

```text
Mobile form:   width = fill container (4-column grid, auto max-width)
Desktop form:  fixed 508px in Figma
Responsive:    w-full lg:max-w-[508px]
Container max: 1700px (automatically applied above 390px)
```

If the token system has a container size token, use that instead of a raw pixel value.

### Conditional Rendering and Responsive Visibility

When an element exists only in one breakpoint:
- Mark it as breakpoint-specific
- **Do not invent equivalents for missing breakpoints**
- Prefer **conditional rendering** for heavy content (desktop ad images, carousels)
- Prefer **responsive visibility classes** for lightweight layout differences

---

## SECTION C — TAILWIND UTILITY CLASSES FROM DESIGN TOKENS

All Tailwind utility classes are auto-generated from design tokens in `theme-block.css` via the Tailwind v4 `@theme` directive.

### ⚠️ Token → Utility Class Naming Convention

The agent **cannot guess these** — use the table exactly:

| Token Category | CSS Variable Pattern (to be used by Agent) | Utility Class Pattern (Not to be followed by Agent) | Example Usage by Agent |
| --- | --- | --- | --- |
| **Border Radius** | `--primitive-radius-{size}` | `rounded-primitive-radius-{size}` | `rounded-primitive-radius-m` |
| **Letter Spacing** | `--tracking-{variant}` | `tracking-{variant}` | `tracking-neutral`, `tracking-negative-1` |
| **Text Colour** | `--color-text-{category}-{variant}` | `text-text-{category}-{variant}` | `text-text-base-primary` |
| **Background Colour** | `--color-background-{category}-{variant}` | `bg-background-{category}-{variant}` | `bg-background-feedback-success` |
| **Spacing** | `--spacing-{size}` | `p-{size}`, `m-{size}` | `p-xl`, `mt-m` |
| **Gap** | `--gap-{size}` | `gap-gap-{size}` | `gap-l`, `gap-m` |
| **Font Size** | `--font-size-font-{size}` | `font-size-font-{size}` | `font-4xl`, `font-m` |
| **Line Height** | `--line-height-{size}` | `line-height-{size}` | `line-height-7xl` |
| **Font Weight** | `--font-weight-{variant}` | `font-weight-{variant}` | `font-weight-bold` |

### How to Choose the Right Class

```text
Need: Background colour for success state
  ↓
Check theme-block.css: --color-background-feedback-success
  ↓
Generate utility class: bg-background-feedback-success
  ↓
Use in component: className="bg-background-feedback-success"
```

1. Identify the design property needed
2. Check `theme-block.css` for available tokens in that category
3. Apply the naming convention
4. Use **semantic** tokens (`text-text-base-primary`), never primitive (`text-primitive-color-black`)
5. Always use Tailwind-wired utilities — never create custom classes

### Colour Rules

- Always use **semantic colour tokens**: `className="bg-background text-text-primary"`
- Do NOT generate `.bg-background` class definitions — Tailwind resolves semantic utilities to CSS variables
- `bg-background` → `var(--color-background)`; `text-text-primary` → `var(--color-text-primary)`
- `theme-block.css` maps every semantic CSS variable to a primitive value

### Spacing / Size Rules

`theme-block.css` maps every semantic CSS variable (spacing, size) to a primitive value. Always use the semantic CSS variable — never a hardcoded value or primitive token.

```text
Raw padding 80px → check @theme for --py/--px → use py-spacing-8xl
Raw gap 8px      → check @theme for --gap    → use gap-s
```

⚠️ **If a value is not found:** create the primitive value, then **call out all new tokens in the coding agent summary document**.

### Missing Token Escalation

If a semantic token must be added:
1. Add the semantic token to the SemanticColor catalog
2. Map it in Base to a primitive value
3. Note that `pnpm build:css` must be run to regenerate `theme-block.css`
4. **Record every new token in the summary's Deviations section**

⚠️ Never edit `base.css` or `theme-block.css` manually — they are build-generated.

---

## SECTION D — TAILWIND USAGE RULES

### When to Use Tailwind

Responsive layout (mobile-first breakpoints) · flex and grid composition · responsive visibility · logical spacing · width/max-width/container behaviour · alignment · gap and padding when tokens map to utilities

### When to Avoid Tailwind

- **Recreating design-system components** — button, input, typography, icon styles already exist
- **Hardcoding brand colours** — use `bg-background-primary`, not `bg-[#00FF00]`
- **Hardcoding typography** — use `font-size-font-4xl`, not `text-[24px]`
- **Duplicating token definitions** — check `theme-block.css` first

### Key Rules

- **Never hardcode values** like `bg-[#00FF00]` or `text-[16px]` when tokens exist
- **Always use semantic tokens** from `theme-block.css`
- **Prefer design-system components** over raw Tailwind for complex UI
- **Always use `cn()` from `@dxp/theme`** for class composition — never concatenate class strings

```tsx
// ✅ CORRECT — conditional classes via cn()
<span className={cn(
  'inline-flex rounded-full px-2 py-0.5 text-xs font-semibold',
  status === 'active' && 'bg-background-feedback-success',
  status === 'expired' && 'bg-background-secondary',
)} />

// ❌ WRONG — string concatenation
<span className={`badge ${status === 'active' ? 'badge-green' : 'badge-gray'}`} />
```

- **TailwindCSS only** — no inline styles, no CSS modules, no styled-components
- **Never** use `style={{ ... }}` on JSX elements
- Use **cva** for atoms with multiple visual variants

---

## SECTION E — TYPOGRAPHY

All text and labels **MUST** use the `Text` component from the design system. This ensures consistent typography, semantic HTML, and responsive token application.

### Text Component Props

| Prop | Required | Purpose |
| --- | --- | --- |
| `field` | ✅ | Text content — plain string, mock object, or Sitecore JSS Text field |
| `variant` | — | Predefined classes for headings, small body text, label text |
| `tag` | — | Semantic HTML element (`h1`–`h6`, `p`, `span`, `label`). Default: `span` |
| `className` | — | Additional Tailwind utilities for responsive styling |

```tsx
// Heading variants — no className needed, already mapped internally
<Text field="Main Title" tag="h1" variant="heading1" />
<Text field="Section Title" tag="h2" variant="heading2" />
<Text field="Subsection" tag="h3" variant="heading3" className="color-override" />

// Semantic element stays fixed; visual typography varies responsively
<Text field="Title" tag="h1" className="heading3 lg:heading1" />

// Body text variants
<Text field="Body copy" tag="p" variant="body-medium-regular" />
<Text field="Small print" tag="p" variant="body-small-regular" />

// Custom combinations
<Text
  field="Emphasized text"
  tag="span"
  className="text-body font-weight-bold text-text-brand-primary"
/>
```

**Rules:**
- Preserve semantic HTML hierarchy
- **Do not downgrade or upgrade semantic heading level based only on visual token name** — if mobile uses `heading3` visually and desktop uses `heading1`, keep the semantic element consistent and vary the visual token responsively
- Do not hardcode font size, line height, or weight when typography tokens exist

---

## SECTION F — RTL SUPPORT

All generated components must support RTL, especially Arabic. This project does **not** use i18n libraries — RTL is implemented via CSS logical properties, TailwindCSS RTL utilities, and the HTML `dir` attribute.

### Rules

| Rule | Correct Approach |
| --- | --- |
| Layout direction | `dir` at `<html>` root — single source of truth |
| Margins / padding | Logical properties: `ms-*`, `me-*`, `ps-*`, `pe-*` |
| Text alignment | `text-start` / `text-end` — never `text-left` / `text-right` |
| Alignment | `items-start` / `items-end` based on semantic alignment, not visual left/right |
| Mixed-language inputs | `dir="auto"` on text inputs |
| LTR content in RTL text | Wrap with `<bdi>` (IDs, codes, numbers) |
| Floats | Never `float: left` / `float: right` — use Flexbox or Grid |
| Absolute positioning | Never hardcoded left/right offsets in RTL-sensitive layouts |
| Physical directional classes | Never `ml-`, `mr-`, `pl-`, `pr-` in layout-critical styles |
| Transforms | Never `transform: translateX` with fixed positive value — negate or use logical transforms |

### ⚠️ Icon Mirroring — Three Categories

```text
✅ REVERSE — directional icons only:
     arrows, chevrons, back/next icons, progress indicators
     Use: rtl:rotate-180

❌ DO NOT REVERSE — neutral icons:
     eye, help, search, calendar
     (unless the design system explicitly specifies otherwise)

❌ DO NOT REVERSE — symmetric/decorative icons:
     close ✕, check ✓, warning ⚠

❌ DO NOT REVERSE — brand logos, ever
```

### Additional RTL Requirements

- Ensure Arabic text can grow without clipping — avoid fixed text widths where translations may be longer
- Ensure button content supports icon placement changing from leading to trailing where RTL requires it
- Preserve accessible name and keyboard behaviour in RTL
- Keep numerals, currency, and date formatting locale-aware

---

## SECTION G — ACCESSIBILITY

Apply accessibility **simultaneously** with implementation — never as a follow-up pass.

| Rule | Implementation |
| --- | --- |
| Semantic HTML | `<header>`, `<main>`, `<nav>`, `<section>`, `<table>`, `<button>` |
| Interactive elements | Every one has `aria-label` or a visible label |
| Scrollable containers | `role="region"` + `aria-label` |
| Dynamic content | `aria-live="polite"` on loaders and status updates |
| Loading tables/lists | `aria-busy={isLoading}` |
| Form inputs | `<label htmlFor>` — never omit labels |
| Keyboard navigation | All interactive elements reachable and operable via keyboard |
| Table headers | `scope="col"` on `<th>` |
| Focus states | Visible focus rings using design token classes |
| Non-semantic interactives | Never `div`/`span` for interactive elements — use `<button>` or `<a>` |
| Error messages | `role="alert"` |
| Test targeting | `data-testid` on all interactive and key structural elements |

- Expose `aria-label` as a prop for all interactive and landmark elements
- Preserve semantic heading order from the design
- Respect `prefers-reduced-motion` for autoplay/transition effects

---

## SECTION H — OVERFLOW AND SCROLL HANDLING

**Critical rule:** apply appropriate scroll behaviour wherever content may overflow its container.

| Axis | Implementation |
| --- | --- |
| **Vertical** | `overflow-y-auto` on any container whose content can exceed height; constrain with `max-h-[...]` |
| **Horizontal** | `overflow-x-auto` for wide content (tables, carousels); add `whitespace-nowrap` when content must not wrap; consider `scroll-snap-type: x mandatory` for carousels |
| **Both** | `overflow-auto` for data grids, spreadsheet-like views |

- ❌ **Never** allow content to overflow and become hidden without scroll
- ❌ **Never** use `overflow: hidden` on containers with dynamic/variable-length content
- ✅ **Always** ensure scrollable areas are keyboard-accessible (`tabIndex={0}` if needed)
- ✅ **Always** add `role="region"` and `aria-label` to scrollable containers

---

## SECTION I — ICON USAGE

- For direct SVG/icon use, wrap the SVG in `Icon.tsx` as a child, or pass the icon name to `Icon.tsx` from Atoms
- For icons inside buttons, use `IconButton` from Atoms; follow Figma specs for button and icon sizing
- Sitecore provides the icon name to `Button`'s `leadingIcon` / `trailingIcon` props, or to `IconButton`; the name becomes the SVG URL

```text
Icons are picked from public/icons/
  Default:        line.svg
  Selected state: fill.svg

Sitecore provides name 'eye' → public/icons/eye/line.svg
```

---

## SECTION J — FULL BLEED PATTERN

Extends components beyond container padding to reach viewport edges.

**✅ Use for:** headers, footers, navigation bars, full-width hero sections with background colours/images, marketing sections requiring visual emphasis

**❌ Don't use for:** standard content sections, nested components

```tsx
import { cn } from "@dxp/theme";
import { NEGATIVE_MARGIN_GUTTER } from "@/Packages/Common/Utils/Constants";

interface MyComponentFields {
  Title?: { value?: string };
  isFullBleed?: boolean;
}

export const MyComponent: React.FC<Props> = ({ fields }) => {
  const title = fields?.Title?.value ?? "";
  const isFullBleed = fields?.isFullBleed;

  return (
    <section
      className={cn(
        "bg-background-primary py-xl lg:py-2xl",
        isFullBleed && NEGATIVE_MARGIN_GUTTER, // "-mx-l lg:-mx-6xl"
      )}
    >
      {/* Inner padding prevents content touching edges */}
      <div className="px-l lg:px-6xl">
        <h2>{title}</h2>
      </div>
    </section>
  );
};
```

`NEGATIVE_MARGIN_GUTTER = "-mx-l lg:-mx-6xl"` — mobile counteracts `px-l`, desktop counteracts `lg:px-6xl`.

**Sitecore configuration:** checkbox field `isFullBleed`, default unchecked.

⚠️ **Common pitfalls:**
- Forgetting inner padding → content touches viewport edges
- Applying to nested components → only apply to top-level sections
- Hardcoding negative margin values → always use the constant

---

## SECTION K — COMPONENT AUTHORING STANDARDS

- ✅ Always use **named exports** — no default exports for components *(exception: CMS-mapped components use default export — handled by `sitecore-rendering-integration`)*
- ✅ Always define a **TypeScript interface** for props (not type aliases for objects)
- ✅ Always **destructure props** with defaults in the function signature
- ✅ Always declare the **return type** (`React.ReactElement` / `React.ReactNode`)
- ✅ Use **`cn()` from `@dxp/theme`** for all conditional class merging
- ✅ Use **cva** for atoms with multiple visual variants
- ❌ Never use class components
- ❌ Never use `React.FC` — it hides the return type
- ❌ Never use `any` for props

### Barrel Exports

Every feature folder MUST have an `index.ts` re-exporting the public API:

```ts
export { PolicyListClient } from "./Components/PolicyListClient";
export type { PolicyListClientProps } from "./Components/PolicyListClient";
```

⚠️ Never use `export *` — always named re-exports.

---

## SECTION L — REUSE-FIRST

Before creating any component, honour the `reuseDecisions[]` from the manifest:

| Decision | Action |
| --- | --- |
| **Reuse existing variant** | Import from the catalogue location; pass props. Do not recreate. |
| **Enhance existing** | Extend with the approved new prop/variant/slot. Preserve backward compatibility. No business logic. |
| **Compose from existing** | Create the approved wrapper using listed existing components. |
| **Extract reusable pattern** | Extract the business-neutral visual pattern into `@dxp/foundation`. |
| **Create new reusable** | Build in the Design System; mark as Storybook + catalogue target. |
| **Create feature-specific** | Build under the feature folder; reuse DS components internally. |

⚠️ The reuse list is already derived from `./src/component-catalogue.json` by the Analysis Agent — **do not search the catalogue again**. Apply decisions exactly as specified; do not override.

- **Always check `@dxp/foundation` FIRST** before creating any new UI element
- Never recreate a Design System element inside a feature or CMS folder

---

## SECTION M — PROP DESIGN RULES

### Complete Prop Interface

```ts
interface MyComponentProps {
  // Content props — all labels, copy, text, CTAs come from props
  title: string;
  description?: string;
  ctaLabel?: string;

  // Visual state props — all visual states controllable via props
  isLoading?: boolean;
  isEmpty?: boolean;
  hasError?: boolean;
  isDisabled?: boolean;

  // Interaction callback props — typed
  onCtaClick?: () => void;
  onChange?: (value: string) => void;

  // Style extension
  className?: string;

  // Accessibility
  "aria-label"?: string;

  // Test ID
  "data-testid"?: string;
}
```

### Prop Rules

- All labels, copy, CTA text, messages, display text → **string props**, never hardcoded
- All visual states (loading, empty, error, disabled) → **boolean props**
- All interaction handlers → **typed function props**
- All icon names, route paths, URLs, variant/config values → **props**
- Use optional props with `undefined` or empty-string defaults — **NEVER hardcoded fallback text**
- Expose `className` for style extension; expose `data-testid` for test targeting
- Use `React.ReactNode` for slot/children content where appropriate
- Booleans are predicates (`isDisabled`, `hasError`, `isLoading`)
- No `any`. Prefer discriminated unions for variant/state props

### No Hardcoded Content

Never hardcode: labels · copy/descriptions · CTA text · error messages · success messages · empty-state messages · icon names · route paths/URLs · business constants · visibility rules · variant values.

> The only place mock/hardcoded values are allowed is Storybook stories — written by the Storybook skill, not here.

---

## SECTION N — VISUAL STATE HANDLING

Every component with a loading, empty, error, or disabled state in Figma must expose those states as props.

```tsx
export function PolicyCard({
  isLoading,
  isEmpty,
  hasError,
  policyNumber,
  ...
}: PolicyCardProps) {
  if (isLoading) return <PolicyCardSkeleton />;
  if (isEmpty) return <PolicyCardEmpty />;
  if (hasError) return <PolicyCardError />;
  return <PolicyCardContent policyNumber={policyNumber} ... />;
}
```

```text
isLoading  → skeleton/placeholder shell
error      → error display slot (message from props)
empty      → empty state slot
disabled   → disabled styling + aria-disabled
default    → normal render
```

⚠️ The component does not decide *when* it is loading — the parent passes that in.

**Interaction and state rules:**
- Disabled button in Figma maps to form validation state
- Password fields support visibility toggle if indicated by design
- Links and buttons expose callback props or navigation handlers
- Inputs support value, validation, error, disabled and required states where relevant
- Do not hardcode static interaction states unless purely static display

---

## SECTION O — MEDIA (CONDITIONAL DELEGATION)

⚠️ **If — and only if — the component renders images, video, or documents**, invoke **`frontend-media-integration`** for DAM, CDN, `next/image` optimisation, responsive sizing, and lazy-loading rules.

Skip entirely for media-free components.

Never hardcode asset URLs. All `src`, `alt`, `width`, `height` come from props/CMS fields.

---

### Output Files (per component)

```text
<ComponentName>/
├── <ComponentName>.tsx          # the presentational component
├── <ComponentName>Types.ts      # Props + local view types (if non-trivial)
└── index.ts                     # barrel (named export)
```

Stories and tests are produced by their own skills — not here.

### Learnings Namespace

Load only the `# UI LEARNINGS` namespace. Do not read LOGIC/TEST/STORYBOOK namespaces.

---

### Gate: Complete When

```text
UNIFIED LENS
- [ ] Reconciliation JSON read first (if it exists); Figma JSONs used as detail only.
- [ ] Unified Implementation Map built for EVERY component before coding.
- [ ] Every Figma value mapped to a project token; discrepancies recorded.
- [ ] New tokens (if any) recorded for the summary.

RESPONSIVE
- [ ] Single responsive implementation (mobile-first base + lg: overrides).
- [ ] Grid used with columns={12} responsive / columns={4} mobile-only; no manual grid classes.
- [ ] Flex used for one-direction content; local grid only for repeated blocks.
- [ ] Width rules applied (w-full mobile; max-w desktop).

TOKENS & TAILWIND
- [ ] Token→utility naming convention applied exactly (gap-gap-*, rounded-primitive-radius-*, etc.).
- [ ] Semantic tokens only — no primitive tokens, no hardcoded values.
- [ ] cn() used for all class composition.

TYPOGRAPHY
- [ ] All text uses the Text component with field/variant/tag.
- [ ] Semantic heading level preserved; visual token varies responsively.

RTL
- [ ] Logical properties only (ms-, me-, ps-, pe-, text-start, text-end).
- [ ] Directional icons mirrored; neutral/symmetric icons and brand logos NOT mirrored.
- [ ] Arabic text growth accommodated.

ACCESSIBILITY
- [ ] Semantic HTML, ARIA roles/labels, keyboard operability, visible focus.
- [ ] data-testid on interactive and key structural elements.

COMPONENT QUALITY
- [ ] Every component fully prop-driven — no hardcoded labels/values/colours.
- [ ] Typed Props + typed callbacks; no `any`; named exports; return type declared.
- [ ] Visual states rendered from props.
- [ ] Reuse decisions honoured; @dxp/foundation checked first.
- [ ] Media delegated to frontend-media-integration only if assets present.
- [ ] Barrels updated with named re-exports.
- [ ] NO data fetching, mappers, services, or stores in any file.
- [ ] Presentational path: no container/hook/service/store created.
```

### Never Do

- Never place API calls, TanStack Query, or data fetching in a presentational component.
- Never wire Sitecore fields or rendering contracts here.
- Never implement business logic, validation logic, or transformation logic.
- Never create mappers, services, or query hooks.
- Never hardcode copy, values, colours, spacing, typography, radius, or shadow when tokens exist.
- Never hardcode image sources.
- Never create a container/hook/service/store for a plain Presentational component.
- Never introduce a raw API/Sitecore type into props — props use FE view models only.
- Never recreate existing design-system components from Figma visuals.
- Never import one feature component into another feature component.
- Never use `React.FC`, class components, or `any`.
- Never use `export *` in barrel files.
- Never edit `base.css` or `theme-block.css` manually.
- Never re-reconcile when `responsive_design_intent.json` already exists.
- Never produce separate desktop/mobile components unless reconciliation requires it.
- Never create Storybook `.stories` files or test files — separate skills own those.
- Never run lint, type-check, or test commands.
