# coding: utf-8
from enum import Enum

from PySide6FluentUI import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    ICON_INTERFACE = "icon_interface"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/gallery/qss/{theme.value.lower()}/{self.value}.qss"
