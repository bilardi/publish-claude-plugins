# CLAUDE.md

## Working directory

Source of truth: `~/github/bilardi/claude/publish-claude-plugins`.

## Versioning

When modifying skills, update the version in both:
- `.claude-plugin/marketplace.json` (plugin version)
- `plugins/bilardi/.claude-plugin/plugin.json`

Use semver: patch for fixes, minor for new/removed skills, major for breaking changes.
