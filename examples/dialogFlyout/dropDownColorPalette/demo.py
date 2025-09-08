# coding:utf-8
import random
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QFrame
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, QPoint, QTimer

from examples.wiindow.splitWidget.demo import Interface
from PySide6FluentUI import DropDownColorPalette, Slider, ToolTip, isDarkTheme


class SliderInfo(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setFixedSize(36, 28)
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.__text = ""

    def setText(self, text: str):
        self.__text = text
        self.update()

    def text(self) -> str:
        return self.__text

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        if isDarkTheme():
            pc = 255
            bc = 38
        else:
            pc = 0
            bc = 255
        painter.setPen(QColor(pc, pc, pc, 32))
        painter.setBrush(QColor(bc, bc, bc))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)

        painter.setPen(QColor(pc, pc, pc))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())


class CustomSlider(Slider):
    
    def _postInit(self):
        super()._postInit()
        self.valueInfo = SliderInfo()

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.valueInfo.setVisible(False))
        self.valueChanged.connect(self.updatePos)

    def updatePos(self):
        if not self.valueInfo.isVisible():
            self.valueInfo.setVisible(True)
        self.timer.stop()
        pos = self.parent().mapToGlobal(self.pos())
        pos += QPoint(self.handle.pos().x() - 10, -42)
        self.valueInfo.move(pos)
        self.valueInfo.setText(str(self.value()))
        self.timer.start(300)


class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(648, 512)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.__bgcColor: QColor = QColor(255, 255, 255, 32)
        self.__position: QPoint = None

        self.slider: CustomSlider = CustomSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0, 255)
        self.slider.setValue(255)
        self.slider.setFixedWidth(488)

        self.viewLayout.setContentsMargins(11, 35, 11, 11)
        self.viewLayout.addWidget(self.slider, 0, Qt.AlignTop | Qt.AlignHCenter)
        self.slider.valueChanged.connect(self.update)

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(lambda: self.setBackgroundColor(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
        # self.timer.start(100)

    def mousePressEvent(self, event):
        self.__position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.move(event.globalPosition().toPoint() - self.__position)
        super().mouseMoveEvent(event)

    def setBackgroundColor(self, color: QColor):
        if self.__bgcColor == color:
            return
        self.__bgcColor = color
        self.update()

    def backgroundColor(self) -> QColor:
        return self.__bgcColor

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        painter.setPen(Qt.NoPen)
        bgc = self.backgroundColor()
        bgc.setAlpha(self.slider.value())
        painter.setBrush(bgc)
        painter.drawRoundedRect(self.rect(), 8, 8)

        painter.setPen(QColor(0, 0, 0))
        font = self.font()
        font.setPixelSize(32)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "迪亚我是你爸爸")


class Window(Interface):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.box: QVBoxLayout = QVBoxLayout(self)
        self.colorPalette: DropDownColorPalette = DropDownColorPalette(self)
        self.cw: CustomWidget = CustomWidget()

        self.box.addWidget(self.colorPalette, 0, Qt.AlignCenter)

        self.s = CustomSlider(Qt.Orientation.Horizontal, self)
        self.s.setRange(0, 100)
        self.box.addWidget(self.s)

        self.cw.show()
        self.connectSignalSlot()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.cw.close()

    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.colorPalette.colorChanged.connect(self.cw.setBackgroundColor)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
