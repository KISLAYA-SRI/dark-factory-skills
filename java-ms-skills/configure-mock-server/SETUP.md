# Setup

This skill is portable across tools that support Agent Skills-style folders. Keep the directory intact and make sure `SKILL.md` remains at the root of the skill folder.

## Slingshot

Slingshot discovers skills from workspace or user-level skill folders. The internal reference supports both the original `.slingshot/skills` path and the newer `.agent/skills` path.

Workspace-level examples:

```text
<repo>/.slingshot/skills/configure-mock-server/SKILL.md
<repo>/.agent/skills/configure-mock-server/SKILL.md
```

User-level examples:

```text
~/.slingshot/skills/configure-mock-server/SKILL.md
~/.agent/skills/configure-mock-server/SKILL.md
```

After adding a user-level skill, refresh and enable agent skills from Slingshot using the refresh control next to the `@` button, or run `Refresh Agent Skills and Local Prompts for Agent Mode` from the VS Code command palette. You can also manage installed skills with `Slingshot: Manage Skills`.

Example prompt:

```text
Use the configure-mock-server skill in Agent mode to wire mock/real downstream toggling for this Spring Boot BFF service.
```


## Codex

Install the skill in the Codex skills location used by your environment, or keep it in a workspace skills folder if your Codex setup loads project-local skills.

Example prompt:

```text
Use the configure-mock-server skill to configure the mock service toggle for the payments downstream call using the JIRA ticket details.
```

If the skill is loaded by name, use the frontmatter skill name from `SKILL.md`:

```text
Use configure-mock-server for this mock/real toggle change.
```

## Claude Code

Install as either a personal or project skill:

```text
~/.claude/skills/configure-mock-server/SKILL.md
.claude/skills/configure-mock-server/SKILL.md
```

Claude Code can invoke the skill automatically from its description, or you can call it directly:

```text
/configure-mock-server configure profile-based mock/real downstream switching using the provided mock service URL.
```

## GitHub Copilot

For Copilot agent skills, install the folder in a supported skills directory.

Project-level examples:

```text
.github/skills/configure-mock-server/SKILL.md
.claude/skills/configure-mock-server/SKILL.md
.agents/skills/configure-mock-server/SKILL.md
```

Personal examples:

```text
~/.copilot/skills/configure-mock-server/SKILL.md
~/.agents/skills/configure-mock-server/SKILL.md
```

Example prompt:

```text
Use the configure-mock-server skill to add MockServiceProperties and DownstreamConfig for the order lookup downstream call, using the mock server URL from the JIRA ticket.
```


## Usage Context Checklist

Before invoking the skill, provide or attach:

- JIRA ticket ID with mock server details, **or** the mock server base URL and downstream API base URL as code-context.
- OpenAPI spec or endpoint details (paths, methods, request/response schemas) for the downstream API.
- Target Spring Boot BFF repository or module.
- Confirmation of whether the project uses `WebClient` (WebFlux) or `RestClient` (Spring 6 MVC).
- Any CI/CD environment variable override requirements.

Expected result: `MockServiceProperties`/`DownstreamConfig` classes and profile-specific YAML changes that let downstream calls switch between the shared mock service and real downstream systems, plus a verification report of the mock server URL used, toggle state per profile, and connectivity check result.
