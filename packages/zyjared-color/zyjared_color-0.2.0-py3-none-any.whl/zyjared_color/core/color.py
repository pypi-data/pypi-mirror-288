from typing import Type, Self, TypeVar, overload, Optional, Union
from .constant import _STYLES_LENGTH
from .style import Style
from .abyss import ColorAbyss

__all__ = [
    'Color',
    'ColorAbyss'
]

_C = TypeVar('_C', bound='Color')
_CA = TypeVar('_CA', bound='ColorAbyss')


class Color(Style):
    @overload
    def __new__(cls, text: Optional[Union[_C]] = None) -> _C: ...

    @overload
    def __new__(cls, text: _CA = None) -> _CA: ...

    def __new__(cls, text: Optional[Union[str, _C, _CA]] = None) -> Self:
        if isinstance(text, ColorAbyss):
            return ColorAbyss(*text.styles)
        else:
            instance = super().__new__(cls)
            if isinstance(text, Color):
                instance._seq = bytearray(text._seq)
            else:
                instance.set_text(text)
            return instance

    def extend(self, src: Type[Self]):
        """
        Extend the style with another style.

        If `self.text` is None, text will be set to `src.text`.
        """
        if not self.text and not src.text:
            self.text = src.text

        for i in range(_STYLES_LENGTH):
            if src._seq[i]:
                self._seq[i] = src._seq[i]
        return self

    def clean(self):
        """
        Clean the style, but not the text.
        """
        self._seq = bytearray(_STYLES_LENGTH)
        return self

    def __add__(self, other: str | Style | ColorAbyss):
        if isinstance(other, ColorAbyss):
            return ColorAbyss(self, *other.styles)
        else:
            return ColorAbyss(self, other)

    def __radd__(self, other: str | Style | ColorAbyss):
        if isinstance(other, ColorAbyss):
            return ColorAbyss(*other.styles, self)
        else:
            return ColorAbyss(other, self)

    def __repr__(self):
        return f'{Style('Color:').green().bold().italic()} {super().__repr__()}'
