from typing import Self, Type,  Optional, TypeVar, Union, overload
from .constant import _COLORS, _COLORS_BG, _STYLES, _STYLES_LENGTH
from .types.method import ColorMethod


__all__ = [
    'Style'
]

_T = TypeVar('_T', bound='Style')


def gen_style_method(code: bytes, index: int):
    def wrapper(self: _T):
        self._seq[index] = code
        return self
    return wrapper


def setup_style_methods(cls: Type):
    for i in range(2, _STYLES_LENGTH):
        setattr(
            cls,
            _STYLES[i][0],
            gen_style_method(_STYLES[i][1], i)
        )

    # Dynamic create color methods
    for (color, code) in _COLORS.items():
        setattr(cls, color, gen_style_method(code, 0))
    for (color, code) in _COLORS_BG.items():
        setattr(cls, color, gen_style_method(code, 1))


class StyleMeta(type):
    def __new__(cls: Type[Self], name: str, bases: tuple, dct: dict):
        ncls = super().__new__(cls, name, bases, dct)
        setup_style_methods(ncls)
        return ncls


class Style(ColorMethod, metaclass=StyleMeta):

    text: str
    _seq: bytearray

    @overload
    def __init__(self, text: _T) -> None: ...
    @overload
    def __init__(self, text: Optional[str] = None, _seq: Optional[bytearray] = None) -> None: ...
    def __init__(self, text: Optional[Union[str, _T]] = None, _seq: Optional[bytearray] = None):
        if isinstance(text, Style):
            self.text = text.text
            self._seq = bytearray(text._seq)
        else:
            self.text = text if text else ''
            self._seq = bytearray(
                _STYLES_LENGTH) if not _seq else bytearray(_seq)

    def set_text(self, text: str):
        """
        Equal to `instance.text = text`
        """
        self.text = text
        return self

    def _compose_styles_no_check(self):
        # start
        ba = bytearray(b'\033[')
        for code in self._seq:
            if code:
                ba.extend(f'{code}'.encode())
                ba.extend(b';')
        ba.pop()
        ba.extend(b'm')

        # text
        ba.extend(self.text.encode())

        # end
        ba.extend(b'\033[0m')

        return ba

    def to_bytearray(self):
        if not self.text:
            return bytearray()
        elif not any(self._seq):
            return self.text.encode()
        else:
            return self._compose_styles_no_check()

    def to_str(self):
        if not any(self._seq) or not self.text:
            return self.text
        else:
            return self._compose_styles_no_check().decode()

    def __str__(self):
        return self.to_str()

    def __format__(self, format_spec: str):
        return f'{self.to_str():{format_spec}}'

    def __repr__(self):
        dic = {}
        dic['text'] = self.text
        if self._seq[0]:
            dic['fg'] = self._seq[0]
        if self._seq[1]:
            dic['bg'] = self._seq[1]
        for i in range(2, _STYLES_LENGTH):
            (style, code) = _STYLES[i]
            if self._seq[i]:
                dic[style] = code
        return f'{dic}'
