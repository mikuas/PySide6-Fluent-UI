# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, QPoint

from examples.window.splitWidget.demo import Interface
from PySide6FluentUI import DropDownColorPalette, ToolTipSlider



class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(648, 512)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.__bgcColor: QColor = QColor(255, 255, 255, 32)
        self.__position: QPoint = None

        self.slider: ToolTipSlider = ToolTipSlider(Qt.Orientation.Horizontal, self)
        self.slider.setRange(0, 255)
        self.slider.setValue(255)
        self.slider.setFixedWidth(488)

        self.viewLayout.setContentsMargins(11, 35, 11, 11)
        self.viewLayout.addWidget(self.slider, 0, Qt.AlignTop | Qt.AlignHCenter)
        self.slider.valueChanged.connect(self.update)


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

        self.cw.show()
        self.connectSignalSlot()

        self.colorPalette.setDefaultColor('red')

    def closeEvent(self, event):
        super().closeEvent(event)
        self.cw.close()

    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.colorPalette.colorChanged.connect(self.cw.setBackgroundColor)

        self.colorPalette.colorChanged.connect(lambda color: print(
            color, self.colorPalette.currentColor()
        ))


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
