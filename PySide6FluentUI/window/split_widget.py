# coding:utf-8
import sys

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, Qt, QPainter
from PySide6.QtCore import QSize, QRect

from .fluent_window_titlebar import SplitTitleBar, TitleBarBase
from ..common.style_sheet import isDarkTheme
from ..common.config import qconfig
from ..components.widgets.frameless_window import FramelessWindow
from ..common.animation import BackgroundAnimationWidget


class SplitWidget(BackgroundAnimationWidget, FramelessWindow):
    def __init__(self, parent: QWidget = None):
        self._isMicaEnabled: bool = False
        self._lightBackgroundColor: QColor = QColor(240, 244, 249)
        self._darkBackgroundColor: QColor = QColor(39, 39, 39)
        super().__init__(parent)
        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.setMicaEffectEnabled(True)

        if sys.platform == "darwin":
            self.titleBar.setFixedHeight(48)
        
        qconfig.themeChangedFinished.connect(self._onThemeChangedFinished)
            
    def setCustomBackgroundColor(self, light, dark):
        """ set custom background color

        Parameters
        ----------
        light, dark: QColor | Qt.GlobalColor | str
            background color in light/dark theme mode
        """
        self._lightBackgroundColor = QColor(light)
        self._darkBackgroundColor = QColor(dark)
        self._updateBackgroundColor()

    def _normalBackgroundColor(self):
        if not self.isMicaEffectEnabled():
            return self._darkBackgroundColor if isDarkTheme() else self._lightBackgroundColor

        return QColor(0, 0, 0, 0)

    def _onThemeChangedFinished(self):
        if self.isMicaEffectEnabled():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.backgroundColor)
        painter.drawRect(self.rect())

    def setMicaEffectEnabled(self, isEnabled: bool):
        """ set whether the mica effect is enabled, only available on Win11 """
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled

    def systemTitleBarRect(self, size: QSize) -> QRect:
        """ Returns the system title bar rect, only works for macOS

        Parameters
        ----------
        size: QSize
            original system title bar rect
        """
        return QRect(size.width() - 75, 0 if self.isFullScreen() else 9, 75, size.height())

    def setTitleBar(self, titleBar):
        super().setTitleBar(titleBar)

        # hide title bar buttons on macOS
        if sys.platform == "darwin" and self.isSystemButtonVisible() and isinstance(titleBar, TitleBarBase):
            titleBar.minBtn.hide()
            titleBar.maxBtn.hide()
            titleBar.closeBtn.hide()