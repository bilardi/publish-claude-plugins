---
name: mermaid-png
description: >
  Replace mermaid code blocks in markdown files with PNG images.
  Extracts blocks to .mermaid files, generates mermaid.live links for the user
  to create PNGs from browser, then substitutes the blocks with image references.
  Use when the user asks to replace mermaid diagrams with images.
---

# Mermaid to PNG

Replace mermaid code blocks in markdown files with PNG images.

## When to use

When the user says "sostituisci i mermaid con delle immagini", "replace mermaid with images", "convert mermaid to png", or similar.

## Process

1. **Find mermaid blocks** - scan the target markdown file for ` ```mermaid ` code blocks
2. **Extract to files** - save each block to `img/{type}.{n}.mermaid` where `{type}` is the diagram type (first word: flowchart, sequenceDiagram, classDiagram, etc.) and `{n}` is a sequential number starting from 1 (2, 3, .. if there are multiple of the same type)
3. **Generate mermaid.live links** - for each `.mermaid` file, encode the content and generate a mermaid.live/edit URL using pako compression:

   ```python
   import json, base64, zlib
   state = json.dumps({
       'code': mermaid_code,
       'mermaid': {'theme': 'default'},
       'autoSync': True,
       'updateDiagram': True
   })
   compressed = zlib.compress(state.encode('utf-8'), 9)
   encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
   url = f'https://mermaid.live/edit#pako:{encoded}'
   ```

4. **Present links to the user** - show each link with instructions:
   - Open the link in the browser
   - Verify the diagram renders correctly
   - Save as PNG: Actions menu (top right) > PNG
   - Save the file as `img/{type}.{n}.png`
5. **Wait for confirmation** - the user will confirm when PNGs are in place
6. **Replace blocks** - substitute each ` ```mermaid ... ``` ` block in the markdown with `![{alt text}](img/{type}.{n}.png)` where `{alt text}` is a descriptive caption derived from the diagram type and context

## Output location

- `.mermaid` source files: `img/` directory of the project
- `.png` files: same `img/` directory (created by the user from browser)

## Notes

- The `img/` directory must exist; create it if missing
- If a `.mermaid` file already exists with the same name, ask before overwriting
- The `.mermaid` files are kept as source of truth for future edits
