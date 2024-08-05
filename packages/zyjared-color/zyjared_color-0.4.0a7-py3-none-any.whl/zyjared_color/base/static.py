from .color import Color
from .styles import STYLES
from ..core import create_static_style_meta

class StaticColor(metaclass=create_static_style_meta(Color, STYLES)):
    pass
