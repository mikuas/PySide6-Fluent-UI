# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QFrame
from PySide6.QtGui import QColor, QPainter, QFontMetrics
from PySide6.QtCore import Qt, QPoint, QTimer, QSize

from examples.window.splitWidget.demo import Interface
from PySide6FluentUI import Slider, isDarkTheme, ToolTipSlider


# class SliderToolTipView(QFrame):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setAttribute(Qt.WA_TransparentForMouseEvents)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
#         self.__text = ""
#         self.__fontMetrics: QFontMetrics = QFontMetrics(self.font())
#
#     def sizeHint(self):
#         return QSize(self.__fontMetrics.horizontalAdvance(self.text()) + 22, 32)
#
#     def setText(self, text: str):
#         self.__text = text
#         self.adjustSize()
#         self.update()
#
#     def text(self) -> str:
#         return self.__text
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
#         if isDarkTheme():
#             pc = 255
#             bc = 38
#         else:
#             pc = 0
#             bc = 255
#         painter.setPen(QColor(pc, pc, pc, 32))
#         painter.setBrush(QColor(bc, bc, bc))
#         painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)
#
#         painter.setPen(QColor(pc, pc, pc))
#         painter.drawText(self.rect(), Qt.AlignCenter, self.text())
#
#
# class ToolTipSlider(Slider):
#     """ A slider can be clicked
#
#     Constructors
#     ------------
#     * ToolTipSlider(`parent`: QWidget = None)
#     * ToolTipSlider(`orient`: Qt.Orientation, `parent`: QWidget = None)
#     """
#
#     def _postInit(self):
#         super()._postInit()
#         self.toolTipView: SliderToolTipView = SliderToolTipView()
#
#         self.__timer: QTimer = QTimer(self)
#         self.__timer.timeout.connect(lambda: self.toolTipView.setVisible(False))
#         self.valueChanged.connect(self.__adjustToolTipPos)
#
#     def __adjustToolTipPos(self):
#         if not self.toolTipView.isVisible():
#             self.toolTipView.setVisible(True)
#         self.__timer.stop()
#         pos = self.parent().mapToGlobal(self.pos())
#         if self.orientation() == Qt.Horizontal:
#             x = self.handle.pos().x() - self.toolTipView.width() // 2.8
#             y = -42
#         else:
#             x = -self.toolTipView.width() - 6
#             y = self.handle.pos().y() - 6
#         pos += QPoint(x, y)
#         self.toolTipView.move(pos)
#         self.toolTipView.setText(str(self.value()))
#         self.__timer.start(300)


class Window(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.box: QHBoxLayout = QHBoxLayout(self)
        self.box.setContentsMargins(11, 38, 11, 11)

        self.hSlider: ToolTipSlider = ToolTipSlider(Qt.Orientation.Horizontal, self)
        self.vSlider: ToolTipSlider = ToolTipSlider(self)

        self.hSlider.setRange(0, 114514)
        self.vSlider.setRange(0, 114514)

        self.box.addWidget(self.hSlider, 1)
        self.box.addWidget(self.vSlider, 1)

        self.connectSignalSlot()
        
    def connectSignalSlot(self):
        super().connectSignalSlot()
        

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
    

if __name__ == '__main__':
    main()