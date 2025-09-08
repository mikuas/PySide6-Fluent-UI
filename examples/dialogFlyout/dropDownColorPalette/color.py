import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt


def color_scale(base: QColor, steps=6):
    """生成一组从浅到深的颜色"""
    colors = []
    for i in range(steps):
        factor = 100 + (i * 50)  # 100% 基色, 每级 +50
        c = base.darker(factor)
        colors.append(c)
    return colors


class ColorBar(QWidget):
    def __init__(self, base_color=QColor("yellow"), steps=6, parent=None):
        super().__init__(parent)
        self.colors = color_scale(base_color, steps)

    def paintEvent(self, event):
        painter = QPainter(self)
        w = 50
        h = 50

        for i, color in enumerate(self.colors):
            painter.fillRect(0, i * h, w, h, color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorBar(QColor("white"), 7)  # 黄色 → 7个层级
    window.show()
    sys.exit(app.exec())
