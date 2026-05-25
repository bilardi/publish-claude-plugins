# publish-claude-plugins

Personal plugins for Claude Code.

## Install

In the terminal digit `claude` and then digit the commands below.

### 1. Add the marketplace

```
/plugin marketplace add bilardi/publish-claude-plugins
```

```
Successfully added marketplace: publish-claude-plugins
```

### 2. Install the plugin

```
/plugin install bilardi@publish-claude-plugins
```

```
✓ Installed bilardi. Run /reload-plugins to activate.
```

### 3. Reload plugin from local cache

```
/reload-plugins
```

### 4. Update plugin after a push

Option A: from the Claude Code TUI

```
/plugin update bilardi@publish-claude-plugins
```

Navigate to the **Installed** tab, select the plugin, and update it.

Option B: from the shell (outside Claude Code)

```sh
claude plugin update bilardi@publish-claude-plugins
```

Then inside Claude Code run `/reload-plugins` to activate the updated version.

## Skills

- **drawio-architecture** - generate a draw.io architecture diagram by analyzing the project code, infrastructure files, and existing diagrams
- **mermaid-png** - replace mermaid code blocks in markdown files with PNG images via mermaid.live
- **md-to-slides** - build a `.pptx` workshop deck from a Markdown source via a Python script that clones template slides and substitutes text, lists, code, tables, and images
