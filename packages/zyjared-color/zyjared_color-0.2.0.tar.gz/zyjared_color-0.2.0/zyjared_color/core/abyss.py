from typing import Self, Type, TypeVar, Tuple
from .types.method import ColorMethod
from .constant import _EXPORT_STYLES
from .style import Style


__all__ = [
    'ColorAbyss'
]

_CA = TypeVar('_CA', bound='ColorAbyss')


def gen_style_method(attr: str):
    def wrapper(self: _CA):
        for style in self.styles:
            getattr(style, attr)()
        return self
    return wrapper


def setup_style_methods(cls: Type):
    for attr in _EXPORT_STYLES:
        setattr(cls, attr, gen_style_method(attr))


class ColorAbyssMeta(type):
    def __new__(cls: Type[Self], name: str, bases: tuple, dct: dict):
        ncls = super().__new__(cls, name, bases, dct)
        setup_style_methods(ncls)
        return ncls


class ColorAbyss(ColorMethod, metaclass=ColorAbyssMeta):

    styles: Tuple[Style, ...]

    def __init__(self, *styles:  str | Style):
        self.styles = tuple(ColorAbyss._v(style)
                            for style in styles if ColorAbyss._bool(style))

    @staticmethod
    def _bool(src: str | Style):
        return bool(src.text) if isinstance(src, Style) else bool(src)

    @staticmethod
    def _v(src: str | Style):
        """
        Return:
            A new style
        """
        return Style(src.text, bytearray(src._seq)) if isinstance(src, Style) else Style(src)

    def to_str(self):
        if not bool(self.styles):
            return ''

        ba = bytearray()
        for style in self.styles:
            ba.extend(style.to_bytearray())

        return ba.decode()

    def __str__(self):
        return self.to_str()

    def __format__(self, format_spec: str):
        return f'{self.to_str():{format_spec}}'

    def __add__(self, other: str | Style | Type[Self]):
        if isinstance(other, ColorAbyss):
            return ColorAbyss(*self.styles, *other.styles)
        else:
            return ColorAbyss(*self.styles, other)

    def __radd__(self, other: str | Style | Type[Self]):
        if isinstance(other, ColorAbyss):
            return ColorAbyss(*other.styles, *self.styles)
        else:
            return ColorAbyss(other, *self.styles)

    def __repr__(self) -> str:
        return f'\n{Style("ColorAbyss:").green().bold().italic()}\n' \
            + '\n'.join(f'{Style(str(i + 1)).red()
                        :>12} {repr(self.styles[i])}' for i in range(len(self.styles)))
