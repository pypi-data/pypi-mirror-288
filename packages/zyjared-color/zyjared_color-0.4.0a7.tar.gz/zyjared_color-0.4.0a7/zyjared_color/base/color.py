from ..core import Style, create_style_method_meta
from .styles import STYLES


class Color(Style, metaclass=create_style_method_meta(STYLES)):

    def _compose_style(self):
        return f'\033[{';'.join([str(i) for i in self.style.values()])}m{self.text}\033[0m'
