from typing import Self, Type, TypeVar
from functools import partial
from .color import Color, ColorAbyss
from .constant import _EXPORT_STYLES


__all__ = [
    'ColorStatic',
]

_C = TypeVar('_C', bound='Color')
_CA = TypeVar('_CA', bound='ColorAbyss')


def gen_style_method(attr: str):
    def wrapper(text: str | _C | _CA):
        if isinstance(text, (ColorAbyss, Color)):
            return getattr(text, attr)()
        else:
            return getattr(Color(text), attr)()
    return wrapper


class ColorStaticMeta(type):
    def __new__(cls: Type[Self], name: str, bases: tuple, dct: dict):
        ncls = super().__new__(cls, name, bases, dct)
        for attr in _EXPORT_STYLES:
            setattr(ncls, attr, staticmethod(partial(gen_style_method(attr))))
        return ncls


class ColorStatic(metaclass=ColorStaticMeta):
    @staticmethod
    def extend(style: _C):
        """
        Extend the style with another style.

        If `self.text` is None, text will be set to `src.text`.

        Return:
            A new style
        """
        return Color().extend(style)

    @staticmethod
    def clean(style: _C) -> _C:
        """
        Clean the instance's style.
        """
        return style.clean()
