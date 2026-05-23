# Workshop slides

Build the IT/EN workshop deck from a Markdown source.

## Files

- `python_workshop.pptx` : the deck (output)
- `slides_it.md` / `slides_en.md` : slide content per language
- `config.py` : type-to-template map, fonts, colors, keywords
- `build_slides.py` : read MD, rebuild .pptx between markers
- `extract_slides.py` : read .pptx, write MD (one-shot bootstrap)

## .pptx setup

The deck must contain, in order:

1. **Cover** : slide 1, `BLANK` with background (manual content)
2. **Agenda** : slide 2, `BIG_NUMBER` with background (in-place update from MD `type:2`)
3. **Templates** at fixed positions (1-indexed; cloned by the script per MD type)
   3. Section stacco : `TITLE` with background
   4. List + code : `TITLE_AND_BODY`; left bullet list with `●` (lvl 0) and `○` (lvl 1); right Solarized Dark code
   5. Practice stacco : `TITLE` no background
   6. Code + terminal : `TITLE_AND_BODY`; both Solarized Dark
   7. Title only : `TITLE_ONLY_1` with a decorative picture (e.g. reference slides)
   8. Title only : `TITLE_ONLY_1` with a minimal table (1 header row + 1 data row + 2 columns); script expands to match the MD table and re-centers horizontally
4. **Marker start** : 1 empty `BLANK` slide right after the templates
5. **Content slides** : built by the script
6. **Marker end** : 1 empty `BLANK` slide
7. **Footer** : References, Thank you, etc.

The script:
- Updates slide 2 in place if the MD has a `type:2` block
- Clears everything between the two markers and rebuilds it from the MD `type:3/4/5/6` blocks
- Leaves the footer untouched

## Workflow

```
extract : .pptx between markers -> slides_it.md  (one-shot)
build   : slides_it.md -> .pptx between markers  (every change)
```

## MD format

Each slide is a `## type:N Title` block.

Agenda (type 2, in-place on slide 2):

```markdown
## type:2 Agenda
### items
- ABC di Python al REPL
- Scaffold del package e primo commit
- Primo ciclo TDD: caso felice
- Ciclo TDD avanzato: caso negativo
```

Section stacco (type 3):

```markdown
## type:3 Scaffold del package e primo commit
### subtitle
@PyVenice #workshop #PythonItalia #Python
```

List + code (type 4):

````markdown
## type:4 ABC - Classe
### left
- Assegnazione
- Condizione
- Ciclo
- Funzione
- **Classe**
  - [Metodo](https://docs.python.org/3/glossary.html#term-method)
### right
```python
class Counter:
    def __init__(self):
        self.value = 0
```
````

Practice stacco (type 5):

```markdown
## type:5 Passiamo alla pratica !
```

Title only with decorative image (type 7):

```markdown
## type:7 venice.python.it
### image
images/venice.png
```

The `### image` section is optional; if omitted the template image is kept. Path is relative to the directory where `build_slides.py` runs (typically `workshop/basic/`).

Table (type 8):

```markdown
## type:8 Quando serve `import pytest`
### table
| Caso | Cosa scrivi | Serve import? |
|---|---|---|
| Solo `assert`     | `assert x == 5`              | NO |
| Test di eccezione | `with pytest.raises(...): ...` | SI |
```

The MD table follows standard markdown syntax (header row, separator `|---|`, data rows). The template's first row keeps its header styling, subsequent rows clone the last data row style. Columns are cloned per-row, so header columns keep header style. The table is re-centered horizontally based on the total column width.

Sizing rules across all `type:7` slides in the MD:
- The **last** `type:7` slide sets the reference: width is computed from its aspect ratio with the template's `top` and `height`
- All earlier `type:7` slides use the same reference width and the template's `top`; their height is computed proportionally to their own aspect ratio
- The image is always centered horizontally on the slide

This way a sequence of images that grow in height (e.g. progressive diagrams) stays aligned at the same `top` and `width`.

Code + terminal (type 6):

````markdown
## type:6 Pratica - Assegnazione
### left
```python
x = 5
print(x)
```
### right
```shell
$ python assegnazione.py
5
```
````

### Inline syntax in lists

- `**text**` : bold (use for the active item)
- `[text](url)` : hyperlink
- `**[text](url)**` : bold + hyperlink
- Nested lists : 2-space indent per level

### Code blocks

- ` ```python ` : Python syntax highlighting
- ` ```shell ` : `$ ` prompt and `#` comments highlighted

## Usage

Bootstrap MD from existing .pptx :

```bash
uv run python extract_slides.py
```

Rebuild .pptx from MD :

```bash
uv run python build_slides.py
```

Build EN deck :

```bash
uv run python build_slides.py --md slides_en.md --pptx python_workshop_en.pptx
```

## Configuration (`config.py`)

- `TYPE_TO_TEMPLATE` : type N -> 1-indexed template slide position (cloned types)
- `AGENDA_POSITION` : 1-indexed position of the agenda slide (in-place update from `type:2`)
- `TITLE_FONT` : default `Arial`
- `TEXT_PT` : content text box font size (default 16)
- `SOLAR_*` : Solarized Dark palette
- `PY_KEYWORDS`, `PY_BUILTINS` : words to highlight as keyword/builtin

## Tasks

### Change font size

Edit `TEXT_PT` in `config.py`. Rebuild.

### Translate to English

1. Translate `slides_it.md` to `slides_en.md`
2. Make `python_workshop_en.pptx` : copy IT pptx, translate slides 1-6 (cover, agenda, 4 templates)
3. `uv run python build_slides.py --md slides_en.md --pptx python_workshop_en.pptx`

### Add a new section

1. Add a `## type:3` entry (stacco) to the MD
2. Add content slides (`type:4` or `type:6`)
3. Build
