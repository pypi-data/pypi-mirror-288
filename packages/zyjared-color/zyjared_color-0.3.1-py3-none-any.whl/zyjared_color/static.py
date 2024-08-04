from typing import Any, Callable, Dict, TypeVar
from .color import Color, STYLES

__all__ = [
    "ColorStatic",
    "gen_static_meta",
]

_C = TypeVar("_C", bound="Color")


def _gen_static_method(attr: str):
    def handler(text: str | _C) -> _C:
        return getattr(Color(text), attr)()
    return handler


def gen_static_meta(styles: Dict[str, Any], callback: Callable[[str], Callable] = _gen_static_method):
    class ColorMeta(type):
        def __new__(cls, name, bases, attrs):
            ncls = super().__new__(cls, name, bases, attrs)
            for k, v in styles.items():
                if isinstance(v, dict):
                    for k1, _ in v.items():
                        setattr(ncls, k1, staticmethod(callback(k1)))
                else:
                    setattr(ncls, k, staticmethod(callback(k)))
            return ncls

    return ColorMeta


class ColorStatic(metaclass=gen_static_meta(STYLES, _gen_static_method)):
    pass
