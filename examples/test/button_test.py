# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt


from PySide6FluentUI import PushButton as PB


class PushButton(PB):

    def _postInit(self):
        super()._postInit()
        self.setStyleSheet("background: transparent;")
        self.setFlat(True)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.NoPen)
        color = QColor("deeppink")
        if not self.isEnabled():
            painter.setOpacity(0.345)
        elif self.isPressed:
            painter.setOpacity(0.567)
        elif self.isHover:
            painter.setOpacity(0.768)
        painter.setBrush(color)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)
        super().paintEvent(e)


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.resize(800, 520)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)

        self.button: PushButton = PushButton()
        self.button.setText("FILL")
        self.button.setMinimumHeight(35)
        # self.button.setEnabled(False)

        self.viewLayout.addWidget(self.button)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    ...

if __name__ == '__main__':
    main()