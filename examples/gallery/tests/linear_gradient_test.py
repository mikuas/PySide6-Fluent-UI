# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPixmap
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        painter.drawPixmap(rect, QPixmap(r"C:\Users\Administrator\OneDrive\Pictures\Background\1758009253862.jpeg"))

        height = rect.height()
        gradient = QLinearGradient(0, height * 0.5, 0, height)
        gradient.setColorAt(0, QColor(255, 255, 255, 64))
        gradient.setColorAt(1, QColor(255, 255, 255))

        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawRect(rect)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()