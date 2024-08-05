from typing import Dict, Union, Any, TypeVar, List, Optional, Type

_S = TypeVar("_S", bound="Style")


def convert_to_style_list(cls: Type[_S], arr: List[str]):
    children = []
    for item in arr:
        if isinstance(item, Style):
            if item.children:
                children.extend(convert_to_style_list(cls, item.children))
            else:
                children.append(cls(
                    item.text, item._cp_style()))
        else:
            children.append(cls(item))
    return children


class Style:

    def __init__(self, text: Optional[Union[str | _S]] = None, _style: Optional[Dict[_S, Any]] = None, _children: Optional[List[Union[_S, str]]] = None, _propagate: Optional[bool] = True):
        """
        参数:
            - `text`:
                - `Style`: 拷贝其属性, `_style` 和 `_children` 将作为扩展。
                - `str`: 直接赋值。
        """
        if isinstance(text, Style):
            self.text = text.text if text.text else None
            self.style = text._cp_style()
            if _style:
                self.style = {**self.style, **_style}
            self.children = text._cp_children(
                _propagate) if text.children else []
            if _children:
                self.children.extend(
                    convert_to_style_list(self.__class__, _children))
        else:
            self.text = text
            self.style = _style if _style else {}
            self.children = convert_to_style_list(
                self.__class__, _children) if _children else []

    def propagate(self):
        """
        如果 `children` 不为空, 则将 `style` 传递给 `children`
        """
        if not self.children:
            return self

        for k, v in self.style.items():
            for s in self.children:
                s.style[k] = v
        return self

    def _cp_style(self):
        return {**self.style}

    def _cp_children(self, propagate=False):
        """
        参数:
            - `propagate`: 是否将 `style` 传递给 `children`
        """
        if propagate:
            return [self.__class__(child.text, {**child.style, **self.style}) for child in self.children]
        return [self.__class__(child.text, child._cp_style()) for child in self.children]

    def copy(self, propagate=False):
        """
        返回一个拷贝

        参数:
            - `propagate`: 是否将 `style` 传递给 `children`
        """
        return self.__class__(self.text, self._cp_style(), self._cp_children(propagate))

    def extend(self, color: _S):
        if not self.text:
            self.text = color.text
        self.style = {**self.style, **color.style}
        self.children.extend(color._cp_children(True))
        return self

    def __add__(self, other: Union[str, _S]):
        return self.__class__(_children=[self, other])

    def __radd__(self, other: Union[str, _S]):
        return self.__class__(_children=[other, self])

    def __repr__(self):
        result = {
            "text": self.text,
            "style": self.style,
            "children": [
                {'text': i.text, 'style': i.style} for i in self.children
            ]
        }
        return str(result)

    # 字符串操作

    def _to_str_shallow(self):
        """
        子类应当重写此方法
        """
        return self.text

    def _to_str(self, propagate=True):
        if self.children:
            if propagate:
                self.propagate()
            return ''.join([c._to_str_shallow() for c in self.children])
        return self._to_str_shallow()

    def __str__(self):
        return self._to_str()

    def __format__(self, format_spec: str):
        return f'{self._to_str():{format_spec}}'
