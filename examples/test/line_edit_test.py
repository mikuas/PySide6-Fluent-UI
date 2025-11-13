# coding:utf-8
import sys
from typing import Union

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QCompleter
from PySide6.QtGui import QColor, QPainter, QPen, QFontMetrics, QPainterPath, QFont, QAction, QIcon, QPalette
from PySide6.QtCore import Qt, QPropertyAnimation, Property, QParallelAnimationGroup, QEasingCurve, QPoint, QTimer

from PySide6FluentUI import FluentStyleSheet, LineEditMenu, LineEditButton, FluentIcon, FillPushButton, themeColor, \
    setFont, getFont, LineEdit, MotionLineEdit, FocusLineEdit
from PySide6FluentUI.common.color import autoFallbackThemeColor
from examples.window.splitWidget.demo import Interface

"""

FocusLineEdit
MotionLineEdit

"""

class T_FocusLineEdit(LineEdit):

    def paintEvent(self, e):
        QLineEdit.paintEvent(self, e)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(self.focusedBorderColor() if self.hasFocus() else autoFallbackThemeColor(QColor(0, 0, 0, 32), QColor(255, 255, 255, 32)))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class T_MotionLineEdit(T_FocusLineEdit):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self._titleText: str = title
        self._placeholderText: str = ""
        self._underlineValue: int = 0
        self._textPos: QPoint = QPoint()
        self.setFixedHeight(34)
        self.__initAnimation()

    def __initAnimation(self):
        self._underlineAni: QPropertyAnimation = QPropertyAnimation(self, b"underlineValue")
        self._titlePosAni: QPropertyAnimation = QPropertyAnimation(self, b"titlePosValue")

        self._underlineAni.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._underlineAni.setDuration(300)
        self._titlePosAni.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._titlePosAni.setDuration(400)

    def getUnderlineValue(self) -> int:
        return self._underlineValue

    def setUnderlineValue(self, value: int) -> None:
        self._underlineValue = value
        self.update()

    def getTextPos(self) -> QPoint:
        return self._textPos

    def setTextPos(self, pos: QPoint) -> None:
        self._textPos = pos

    def setTitle(self, title: str) -> None:
        if title == self._titleText:
            return
        self._titleText = title
        self.update()

    def title(self) -> str:
        return self._titleText

    def setPlaceholderText(self, text: str):
        if text == self._placeholderText:
            return
        self._placeholderText = text
        self.update()

    def placeholderText(self) -> str:
        return self._placeholderText

    def paintEvent(self, e):
        QLineEdit.paintEvent(self, e)
        x = self.width()
        y = self.height() - 18

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setBrush(Qt.NoBrush)
        alpha = 128 if self.isEnabled() else 64
        pen = QPen(autoFallbackThemeColor(QColor(0, 0, 0, alpha), QColor(255, 255, 255, alpha)), 1.5)
        painter.setPen(pen)
        painter.drawLine(0, y, x, y)

        """ draw placeholder text """
        self._drawPlaceholderText(painter, pen)

        """ draw title """
        self._drawTitle(painter, pen)

        """ draw focus line """
        self._drawFocusLine(painter, pen, y)

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self._changeAniValue(self.getUnderlineValue(), 0, self.getTextPos(), QPoint(29 * len(self.actions()), 0))

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self._changeAniValue(0, self.width(), QPoint(29 * len(self.actions()), 0), QPoint(0, self.height() - 19))

    def _drawFocusLine(self, painter: QPainter, pen: QPen, y: int):
        value = self.getUnderlineValue()
        if value > 0:
            pen.setWidthF(2.5)
            pen.setBrush(self.focusedBorderColor())
            painter.setPen(pen)
            painter.drawLine(0, y, value, y)

    def _drawPlaceholderText(self, painter: QPainter, pen: QPen):
        if self.hasFocus():
            painter.setPen(pen)
            painter.setFont(getFont(14))
            painter.drawText(self.rect(), self.placeholderText(), Qt.AlignBottom)

    def _drawTitle(self, painter: QPainter, pen: QPen):
        painter.setPen(pen)
        painter.setFont(getFont(16))
        pos = self.getTextPos()
        painter.drawText(self.rect().adjusted(5 + pos.x(), 0, 5, -pos.y()), self.title(), Qt.AlignVCenter)

    def _changeAniValue(self, usv: int, uev: int, tsp: QPoint, tep: QPoint):
        self._underlineAni.stop()
        self._titlePosAni.stop()

        self._underlineAni.setStartValue(usv)
        self._underlineAni.setEndValue(uev)
        self._underlineAni.start()
        if not self.text():
            self._titlePosAni.setStartValue(tsp)
            self._titlePosAni.setEndValue(tep)
            self._titlePosAni.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        value = self.getUnderlineValue()
        if value == 0:
            return
        self._underlineAni.stop()
        self._underlineAni.setStartValue(value)
        self._underlineAni.setEndValue(self.width())
        self._underlineAni.start()

    underlineValue = Property(int, getUnderlineValue, setUnderlineValue)
    titlePosValue = Property(QPoint, getTextPos, setTextPos)


class MainWindow(Interface):
# class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)

        self.userNameEdit: MotionLineEdit = MotionLineEdit("用户名", self)
        self.passwordEdit: MotionLineEdit = MotionLineEdit("密码", self)
        self.phoneEdit: MotionLineEdit = MotionLineEdit("手机号", self)
        self.fe: FocusLineEdit = FocusLineEdit(self)
        self.submitButton: FillPushButton = FillPushButton("提交", self)

        self.userNameEdit.setPlaceholderText("请输入用户名")
        self.passwordEdit.setPlaceholderText("请输入密码")
        self.phoneEdit.setPlaceholderText("请输入手机号")
        self.fe.setPlaceholderText("None")

        self.viewLayout.addWidget(self.userNameEdit)#, 0, Qt.AlignmentFlag.AlignCenter)
        self.viewLayout.addWidget(self.passwordEdit)#, 0, Qt.AlignmentFlag.AlignCenter)
        self.viewLayout.addWidget(self.phoneEdit)#, 0, Qt.AlignmentFlag.AlignCenter)
        self.viewLayout.addWidget(self.fe)#, 0, Qt.AlignmentFlag.AlignCenter)

        self.userNameEdit.setClearButtonEnabled(True)
        self.passwordEdit.setClearButtonEnabled(True)
        self.phoneEdit.setClearButtonEnabled(True)
        self.fe.setClearButtonEnabled(True)

        items = ["Interval", "Int", "Im", "Is"]
        completer = QCompleter(items, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        self.userNameEdit.setCompleter(completer)
        self.passwordEdit.setCompleter(completer)
        self.phoneEdit.setCompleter(completer)
        self.fe.setCompleter(completer)

        self.submitButton.setFillColor("#c6eeb0")
        self.viewLayout.addWidget(self.submitButton)
        self.userNameEdit.setEnabled(False)
        self.connectSignalSlot()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

    ...

if __name__ == '__main__':
    main()