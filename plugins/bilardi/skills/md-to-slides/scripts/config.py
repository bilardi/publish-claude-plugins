"""Configuration for build_slides.py.

The .pptx must have:
- Templates at slide positions matching TYPE_TO_TEMPLATE (1-indexed)
- Two empty BLANK marker slides: one right after templates,
  one right before footer slides
- Content slides go between the two markers
"""

DEFAULT_PPTX = "python_workshop.pptx"
DEFAULT_MD = "slides_it.md"

TITLE_FONT = "Arial"
TEXT_PT = 16

# slide type N --> position of template slide in the .pptx (1-indexed).
# These types are CLONED from the template and inserted between markers.
TYPE_TO_TEMPLATE = {
    3: 3,  # section stacco (with BG)
    4: 4,  # list + code (ABC/Scaffold content)
    5: 5,  # practice stacco (no BG)
    6: 6,  # code + terminal (Practice content)
    7: 7,  # title only (TITLE_ONLY_1 with decorative picture)
    8: 8,  # title only with a table (header + data rows)
}

# Fixed-position slides: updated in-place from the MD (not cloned).
# type:2 is the Agenda, which is unique and stays at its position.
AGENDA_POSITION = 2  # 1-indexed

# Solarized Dark palette (RGB tuples)
SOLAR_BG = (0x00, 0x2B, 0x36)
SOLAR_DEFAULT = (0x93, 0xA1, 0xA1)
SOLAR_COMMENT = (0x58, 0x6E, 0x75)
SOLAR_KEYWORD = (0x85, 0x99, 0x00)
SOLAR_STRING = (0x2A, 0xA1, 0x98)
SOLAR_NUMBER = (0xD3, 0x36, 0x82)
SOLAR_BUILTIN = (0xB5, 0x89, 0x00)

PY_KEYWORDS = {
    "def", "class", "if", "elif", "else", "for", "while", "return",
    "in", "not", "and", "or", "is", "True", "False", "None",
}
PY_BUILTINS = {"print", "range", "self"}
