---
name: md-to-slides
description: >
  Use when adding/modifying slide types, extending build_slides.py / extract_slides.py / config.py,
  swapping or adapting a .pptx template, scaffolding a new workshop project from existing
  templates, or debugging mismatches between template and script. Also use when the user mentions
  "md-to-slides", "build_slides", "type:N slide", or "slides_it.md".
---

# Workshop slides

Build workshop `.pptx` decks from a Markdown source via a custom Python script that clones template slides and replaces text / lists / code / tables / images based on the MD content.

## What this skill provides

- `scripts/` : current snapshot of `build_slides.py`, `extract_slides.py`, `config.py`, `README.md`. Copy into a workshop folder when scaffolding a new project.
- `templates/python_workshop_template.pptx` : reference template (8 template slides + 2 BLANK markers + 4 footer slides). Copy and rename to `python_workshop.pptx` in the workshop folder.

## File layout in a workshop project

```
<workshop_dir>/
  build_slides.py            # main: MD -> .pptx
  extract_slides.py          # one-shot: .pptx -> MD bootstrap
  config.py                  # type-to-template map, fonts, colors, keywords
  README.md                  # user-facing docs
  python_workshop.pptx       # actual deck
  slides_it.md               # source content (per language)
  images/                    # assets used by type:7 slides
```

## Template "contracts"

The `.pptx` must guarantee, otherwise the script fails or produces wrong output:

1. **Template slide positions** (1-indexed, must match `config.TYPE_TO_TEMPLATE`):
   - 1 : Cover (`BLANK` + BG, manual content)
   - 2 : Agenda (`BIG_NUMBER` + BG; updated in-place from MD `type:2`)
   - 3 : Section stacco (`TITLE` + BG)
   - 4 : List + code (`TITLE_AND_BODY`; left bullet list, right Solarized code box)
   - 5 : Practice stacco (`TITLE`, no BG)
   - 6 : Code + terminal (`TITLE_AND_BODY`; both Solarized code boxes)
   - 7 : Title + decorative picture (`TITLE_ONLY_1`)
   - 8 : Title + minimal table 2 rows x 2 columns (`TITLE_ONLY_1` with table shape)
2. **Markers** : 2 empty `BLANK` slides, one right after the templates, one right before the footer. The script clears and rebuilds everything strictly between them.
3. **Shape detection contracts** :
   - Title placeholder must have `placeholder_format.idx == 0`
   - Code box detected by fill color `#002B36` (Solarized base03)
   - Marker slides have `layout.name == "BLANK"` and no text in any shape

## Quick reference

| Task | What to edit |
|------|---|
| New slide type N | template at slide N + `config.TYPE_TO_TEMPLATE` + `apply_content` case (if custom) + `README.md` |
| New MD section name (e.g. `### caption`) | `parse_md` + relevant `apply_content` branch |
| Change font size globally | `config.TEXT_PT` |
| Change Solarized palette | `config.SOLAR_*` |
| Add Python keyword | `config.PY_KEYWORDS` / `PY_BUILTINS` |
| Translate to another language | new `slides_<lang>.md` + new `.pptx` with translated templates 1-2 (cover, agenda) + run `build_slides.py --md slides_<lang>.md --pptx <output>.pptx` |
| Adopt new template same schema | swap the .pptx, no config change |
| Adopt new template different positions | edit `config.TYPE_TO_TEMPLATE` |

## Adding a new slide type

1. Add the template slide to the `.pptx` (typical position: right before the start marker)
2. Add `N: position` to `config.TYPE_TO_TEMPLATE` (and shift `AGENDA_POSITION` if you inserted before slide 2)
3. If the type needs custom content (sections beyond `### subtitle`/`### left`/`### right`/`### image`/`### table`), add a `if typ == N:` block in `apply_content`
4. If a new MD section name is introduced, extend `parse_md` to recognize it
5. Update `README.md` MD format section with an example
6. Build to verify

## Scaffolding a new workshop

```bash
mkdir -p <workshop_dir>
cd <workshop_dir>
# copy script files from this skill
cp <skill_dir>/scripts/* .
cp <skill_dir>/templates/python_workshop_template.pptx python_workshop.pptx
# write content
$EDITOR slides_it.md
# build
uv run python build_slides.py
```

For uv: the workshop dir needs `pyproject.toml` with `python-pptx`, `pillow` (used by `replace_picture`):

```toml
[project]
name = "workshop-<name>"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["python-pptx>=1.0.0", "pillow>=10.0.0"]
```

Then `uv sync` once.

## Anti-patterns

- **Manually editing slides between markers** : next build wipes them. Always edit through `slides_it.md`
- **Changing the code box fill color** in a template : breaks `is_code_box` detection; if needed, update the hardcoded `"002B36"` in `is_code_box` in `build_slides.py`
- **Removing a marker** : build aborts with "Need 2 BLANK marker slides"
- **Using `## type:N` in MD without N in `config.TYPE_TO_TEMPLATE`** (except `type:2`, special-cased for in-place agenda) : the slide is silently skipped (warning to stderr only)
- **Re-running `build_slides.py` after deep manual edits** : the rebuild discards them. Keep the MD as the source of truth

## Generalization note

When 2+ templates exist with different conventions (positions, layouts, marker styles), consider:
- Moving template-specific knobs out of `config.py` constants into a per-template config file (e.g. `templates/<name>/config.py`)
- Adding a `--template <name>` CLI flag to `build_slides.py` that loads the right config
- Currently `config.py` has one set of constants; this is fine for 1 template
