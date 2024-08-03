from typing import Final, Tuple, List

_PKG_NAME: Final = 'zyjared-color'

_COLORS: Final = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,
    'bright_black': 90,
    'bright_red': 91,
    'bright_green': 92,
    'bright_yellow': 93,
    'bright_blue': 94,
    'bright_magenta': 95,
    'bright_cyan': 96,
    'bright_white': 97,
}

_COLORS_BG: Final = {
    'bg_black': 40,
    'bg_red': 41,
    'bg_green': 42,
    'bg_yellow': 43,
    'bg_blue': 44,
    'bg_magenta': 45,
    'bg_cyan': 46,
    'bg_white': 47,
    'bg_bright_black': 100,
    'bg_bright_red': 101,
    'bg_bright_green': 102,
    'bg_bright_yellow': 103,
    'bg_bright_blue': 104,
    'bg_bright_magenta': 105,
    'bg_bright_cyan': 106,
    'bg_bright_white': 107,
}


_STYLES: List[Tuple[str, int | None]] = [
    ('fg', None),
    ('bg', None),
    ('bold', 1),
    ('italic', 3),
    ('underline', 4),
    ('through', 9),
    ('reverse', 7),
    ('dim', 2),
    ('blink', 5),
    ('blink_fast', 6),
    ('hidden', 8)
]

_STYLES_LENGTH: Final = len(_STYLES)

_EXPORT_STYLES: Tuple[str] = (
    *_COLORS.keys(),
    *_COLORS_BG.keys(),
    *[s for (s, _) in _STYLES[2:]]
)
