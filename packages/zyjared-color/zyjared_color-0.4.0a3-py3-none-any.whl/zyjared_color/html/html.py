from typing import Dict, Union, Any, TypeVar, List, Optional
from ..base.color import gen_color_meta
from ..core import Style

_CH = TypeVar("_CH", bound="ColorHTML")

STYLES = {
    "font-weight": {
        "thin": "lighter",
        "bold": "bolder",
    },
    "font-style": {
        "italic": "italic",
    },
    "text-decoration": {
        "through": "line-through",
        "underline": "underline"
    },
    "opacity": {
        "hidden": 0,
    },
    "color": {
        "black": "#030712",
        "red": "#dc2626",
        "green": "#84cc16",
        "yellow": "#eab308",
        "blue": "#0284c7",
        "magenta": "#c026d3",
        "cyan": "#22d3ee",
        "white": "#f8fafc",
        "bright_black": "#4b5563",
        "bright_red": "#f87171",
        "bright_green": "#bef264",
        "bright_yellow": "#fde047",
        "bright_blue": "#7dd3fc",
        "bright_magenta": "#e879f9",
        "bright_cyan": "#a5f3fc",
        "bright_white": "#ffffff",
    },
    "background-color": {
        "bg_black": "#030712",
        "bg_red": "#dc2626",
        "bg_green": "#84cc16",
        "bg_yellow": "#eab308",
        "bg_blue": "#0284c7",
        "bg_magenta": "#c026d3",
        "bg_cyan": "#22d3ee",
        "bg_white": "#f8fafc",
        "bg_bright_black": "#4b5563",
        "bg_bright_red": "#f87171",
        "bg_bright_green": "#bef264",
        "bg_bright_yellow": "#fde047",
        "bg_bright_blue": "#7dd3fc",
        "bg_bright_magenta": "#e879f9",
        "bg_bright_cyan": "#a5f3fc",
        "bg_bright_white": "#ffffff",
    }
}

# -+-+-+-+-+--+-+-+-+-+--+-+-+-+-+--+-+-+-+-+--+-+-+-+-+--+-+
#
# ColorHtml
#
# -+-+-+-+-+--+-+-+-+-+--+-+-+-+-+--+-+-+-+-+--+-+-+-+-+--+-+


class ColorHTML(Style, metaclass=gen_color_meta(STYLES)):

    def __init__(self, text: Optional[Union[str | _CH]] = None, _style: Optional[Dict[_CH, Any]] = None, _children: Optional[List[Union[_CH, str]]] = None, _propagate: Optional[bool] = False):
        super().__init__(text, _style, _children, _propagate)

    def _to_str_shallow(self):
        if self.text:
            if self.style:
                return f'<span style="{";".join([f'{k}:{v}' for k, v in self.style.items()])};">{self.text}</span>'
            else:
                return self.text
        else:
            return ""

    def _to_str(self, propagate=False):
        return super()._to_str(propagate)
