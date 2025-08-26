# coding:utf-8
from typing import List
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QPen, QValidator
from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QWidget

from .line_edit import LineEdit
from ...common.style_sheet import themeColor


class PinBoxLineEdit(LineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__isTop: bool = False
        self.__isEnd: bool = False
        self.setAlignment(Qt.AlignCenter)
        self.setMaxLength(1)
        self.textChanged.connect(self._onTextChanged)

    def keyReleaseEvent(self, e):
        super().keyReleaseEvent(e)
        if e.key() == Qt.Key.Key_Backspace and not self.__isTop:
            self.focusPreviousChild()

    def _onTextChanged(self):
        if len(self.text()) >= 1 and not self.__isEnd:
            self.focusNextChild()

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.hasFocus():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(themeColor())
            pen.setCapStyle(Qt.RoundCap)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class PinBox(QWidget):

    textChanged = Signal(list)

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.hBoxLayout: QHBoxLayout = QHBoxLayout(self)
        self.__totas: int = 4
        self.__pinBoxWidth: int = 45
        self.__pinBoxHeight: int = 35
        self.__echoMode: QLineEdit.echoMode = None
        self.__validator: QValidator = None
        self.__pinBoxLineEdits: List[PinBoxLineEdit] = []  # type: List[PinBoxLineEdit]

        self.__initPinBox()
        self.hBoxLayout.setAlignment(Qt.AlignCenter)
    
    def __initPinBox(self):
        for _ in range(self.__totas):
            pinBox = PinBoxLineEdit(self)
            pinBox.setFixedSize(self.__pinBoxWidth, self.__pinBoxHeight)
            
            if self.__echoMode:
                pinBox.setEchoMode(self.__echoMode)
            if self.__validator:
                pinBox.setValidator(self.__validator)
            
            self.hBoxLayout.addWidget(pinBox)
            self.__pinBoxLineEdits.append(pinBox)
            
            pinBox.textChanged.connect(self.__onTextChange)
            
        self.__pinBoxLineEdits[0].__isTop = True
        self.__pinBoxLineEdits[-1].__isEnd = True

    def __onTextChange(self):
        result = []
        for w in self.__pinBoxLineEdits:
            result.append(w.text())
        self.textChanged.emit(result)

    def setEchoMode(self, mode: QLineEdit.EchoMode):
        if mode == self.__echoMode:
            return
        self.__echoMode == mode
        for edit in self.__pinBoxLineEdits:
            edit.setEchoMode(mode)
        
    def setPinBoxFixedWidth(self, w: int):
        if w == self.__pinBoxWidth:
            return
        self.__pinBoxWidth = w
        for box in self.__pinBoxLineEdits:
            box.setFixedWidth(w)

    def setPinBoxFixedHeight(self, h: int):
        if h == self.__pinBoxHeight:
            return
        self.__pinBoxHeight = h
        for box in self.__pinBoxLineEdits:
            box.setFixedHeight(h)
    
    def setPinBoxValidator(self, validator: QValidator):
        self.__validator = validator
        for box in self.__pinBoxLineEdits:
            box.setValidator(validator)

    def setPinBoxCount(self, num: int):
        if num == self.__totas:
            return
        self.__totas = num
        for edit in self.__pinBoxLineEdits:
            edit.deleteLater()
        self.__pinBoxLineEdits.clear()
        self.__initPinBox()
        
    def count(self):
        return self.__totas