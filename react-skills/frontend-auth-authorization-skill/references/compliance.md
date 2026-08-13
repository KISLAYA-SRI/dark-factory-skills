# Frontend Auth Compliance
- Do not store access tokens in localStorage/sessionStorage unless explicitly approved by the security model.
- Protected data must be checked server-side, not only hidden by client UI.
- Authorization policy must come from supplied identity docs, backend contract, or user requirements.

## Regulatory Context
Use supplied controls only. Apply WCAG, privacy, security, identity, and compliance boundaries only when required by the skill scope.