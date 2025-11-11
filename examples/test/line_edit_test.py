# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtGui import QColor, QPainter, QPen, QFontMetrics
from PySide6.QtCore import Qt, QPropertyAnimation, Property, QParallelAnimationGroup, QEasingCurve, QPoint

from PySide6FluentUI import FluentStyleSheet, LineEditMenu, LineEditButton, FluentIcon


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._titleText: str = ""
        self._placeholderText: str = ""
        self._underlineValue: int = 0
        self._textXPos: int = 0
        self._isValidationError: bool = False
        self._isClearButtonEnabled: bool = False
        self.hBoxLayout: QHBoxLayout = QHBoxLayout(self)
        self.clearButton: LineEditButton = LineEditButton(FluentIcon.CLOSE, self)

        self.clearButton.setFixedSize(29, 25)
        self.clearButton.hide()

        self.hBoxLayout.setSpacing(3)
        self.hBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.hBoxLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignRight)

        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.__onTextChanged)
        self.__initAnimation()
        FluentStyleSheet.LINE_EDIT.apply(self)

    def __initAnimation(self):
        self._underlineAni: QPropertyAnimation = QPropertyAnimation(self, b"underlineValue")
        self._titleXPosAni: QPropertyAnimation = QPropertyAnimation(self, b"titleXPosValue")

        self._underlineAni.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._underlineAni.setDuration(500)
        self._titleXPosAni.setEasingCurve(QEasingCurve.Type.InOutBack)
        self._titleXPosAni.setDuration(400)

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        self._adjustTextMargins()

    def isClearButtonEnabled(self) -> bool:
        return self._isClearButtonEnabled

    def _adjustTextMargins(self):
        m = self.textMargins()
        self.setTextMargins(0, m.top(), 28, m.bottom())

    def isValidationError(self) -> bool:
        return self._isValidationError

    def setValidationValue(self, value: bool):
        self._isValidationError = value
        self.update()

    def getUnderlineValue(self) -> int:
        return self._underlineValue

    def setUnderlineValue(self, value: int) -> None:
        self._underlineValue = value
        self.update()

    def getTextXPos(self) -> int:
        return self._textXPos

    def setTextXPos(self, x: int) -> None:
        self._textXPos = x

    def setTitle(self, title: str) -> None:
        if title == self._titleText:
            return
        self._titleText = title
        self.update()

    def title(self) -> str:
        return self._titleText

    def setPlaceholderText(self, text: str):
        self._placeholderText = text
        self.update()

    def placeholderText(self) -> str:
        return self._placeholderText

    def contextMenuEvent(self, e):
        LineEditMenu(self).exec(e.globalPos(), ani=True)

    def paintEvent(self, e):
        super().paintEvent(e)
        x = self.width()
        y = self.height() - 16

        painter = QPainter(self)
        painter.setBrush(Qt.NoBrush)
        pen = QPen(QColor(0, 0, 0, 96), 3)
        painter.setPen(pen)
        painter.drawLine(0, y, x, y)

        value = self.getUnderlineValue()
        if value > 0:
            pen.setBrush(QColor(255, 0, 0))
            painter.setPen(pen)
            painter.drawLine(0, y, value, y)

        if self.isValidationError():
            pen.setBrush(QColor(255, 0, 0))
        else:
            pen.setBrush(QColor(0, 0, 0, 114))
        painter.setPen(pen)
        painter.drawText(self.rect(), self.placeholderText(), Qt.AlignBottom)

        pen.setBrush(QColor(0, 0, 0, 114))
        painter.setPen(pen)
        font = self.font()
        font.setPixelSize(16)
        painter.setFont(font)
        painter.drawText(self.rect().adjusted(5, 0, 0, -self.getTextXPos()), self.title(), Qt.AlignVCenter)

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.clearButton.hide()
        self._changeAniValue(self.getUnderlineValue(), 0, self.getTextXPos(), 0)

    def focusInEvent(self, e):
        super().focusInEvent(e)
        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(self.text()))
        self._changeAniValue(0, self.width(), 0, self.height() - 15)

    def _changeAniValue(self, usv: int, uev: int, tsv: int, tev: int):
        self._underlineAni.stop()
        self._titleXPosAni.stop()

        if not self.isValidationError():
            self._underlineAni.setStartValue(usv)
            self._underlineAni.setEndValue(uev)
            self._underlineAni.start()
        if not self.text():
            self._titleXPosAni.setStartValue(tsv)
            self._titleXPosAni.setEndValue(tev)
            self._titleXPosAni.start()

    def __onTextChanged(self, text):
        """ text changed slot """
        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(text) and self.hasFocus())

    underlineValue = Property(int, getUnderlineValue, setUnderlineValue)
    titleXPosValue = Property(int, getTextXPos, setTextXPos)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        value = self.getUnderlineValue()
        if value == 0:
            return
        self._underlineAni.stop()
        self._underlineAni.setStartValue(value)
        self._underlineAni.setEndValue(self.width())
        self._underlineAni.start()


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)

        self.userNameEdit: CustomLineEdit = CustomLineEdit(self)
        self.passwordEdit: CustomLineEdit = CustomLineEdit(self)

        self.userNameEdit.setTitle("用户名")
        self.userNameEdit.setPlaceholderText("请输入用户名")
        self.passwordEdit.setTitle("密码")
        self.passwordEdit.setPlaceholderText("请输入密码")

        self.viewLayout.addWidget(self.userNameEdit)#, 0, Qt.AlignmentFlag.AlignCenter)
        self.viewLayout.addWidget(self.passwordEdit)#, 0, Qt.AlignmentFlag.AlignCenter)

        self.passwordEdit.setClearButtonEnabled(True)
        self.userNameEdit.textChanged.connect(
            lambda text: {
                (
                    self.userNameEdit.setPlaceholderText("用户名已存在!"),
                    self.userNameEdit.setValidationValue(True)
                ) if text == "interval" else
                (
                    self.userNameEdit.setPlaceholderText("请输入用户名"),
                    self.userNameEdit.setValidationValue(False)
                )
            }
        )
        self.passwordEdit.textChanged.connect(
            lambda text: {
                (
                    self.passwordEdit.setPlaceholderText("密码已存在!"),
                    self.passwordEdit.setValidationValue(True)
                ) if text == "114514" else
                (
                    self.passwordEdit.setPlaceholderText("请输入密码"),
                    self.passwordEdit.setValidationValue(False)
                )
            }
        )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

    ...

if __name__ == '__main__':
    main()