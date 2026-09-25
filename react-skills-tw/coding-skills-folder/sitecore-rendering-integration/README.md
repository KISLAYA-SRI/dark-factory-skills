# Sitecore Rendering Integration

Owns the Sitecore-to-React boundary for CMS-mapped components — typed Sitecore field contracts, Layout Service field mapping, rendering entry components, placeholder handling, and component-registry integration. Keeps CMS labels separate from API values.

## Use This For

- Wiring CMS-mapped components to the Sitecore Layout Service (Phase 5).
- Defining typed field contracts and mapping fields to presentational props.
- Registering default-exported rendering entry components in the component registry.
- Handling child placeholders and Experience Editor/preview safety.

## Expected Flow

```text
1. Typed Sitecore field contract
2. Map Layout Service fields → props (via helpers)
3. Rendering entry component (default export)
4. Register in component registry
5. Wire child placeholders
6. Keep CMS labels separate from API values
```

## Key Rules

- Layout JSON is the Sitecore-to-frontend contract; frontend renders registered components.
- Rendering entry components use default exports (registry requirement).
- Never hardcode CMS copy — read from Sitecore fields.
- No BFF data fetching in the rendering entry — that belongs to the logic layer.
- Never source a business value from a CMS field.

See [SKILL.md](./SKILL.md) for the full instructions.
