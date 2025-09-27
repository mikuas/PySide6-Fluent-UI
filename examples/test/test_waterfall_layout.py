from PySide6.QtWidgets import (
    QApplication, QWidget, QLayout, QSizePolicy,
    QPushButton, QScrollArea, QVBoxLayout
)
from PySide6.QtCore import QRect, QSize
import sys, random


class FixedWaterfallLayout(QLayout):
    def __init__(self, min_item_width=120, spacing=10, parent=None):
        super().__init__(parent)
        self.setContentsMargins(11, 11, 11, 11)
        self.min_item_width = min_item_width
        self.spacing = spacing
        self.items = []

    def addItem(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)

    def itemAt(self, index):
        return self.items[index] if 0 <= index < len(self.items) else None

    def takeAt(self, index):
        if 0 <= index < len(self.items):
            return self.items.pop(index)
        return None

    def setGeometry(self, rect):
        super().setGeometry(rect)
        if not self.items:
            return

        # 用控件的 sizeHint 来决定宽度
        item_width = self.items[0].sizeHint().width()
        columns = max(1, rect.width() // (item_width + self.spacing))

        col_heights = [0] * columns

        for item in self.items:
            hint = item.sizeHint()
            # 找最矮列
            col = col_heights.index(min(col_heights))
            x = rect.x() + col * (item_width + self.spacing)
            y = rect.y() + col_heights[col]

            item.setGeometry(QRect(x, y, hint.width(), hint.height()))
            col_heights[col] += hint.height() + self.spacing

        self._total_height = max(col_heights)

    def sizeHint(self):
        return QSize(400, getattr(self, "_total_height", 300))


class WaterfallWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = FixedWaterfallLayout(min_item_width=120, spacing=10)
        self.setLayout(layout)

        # 添加测试 item（固定宽度 + 不同高度）
        for i in range(30):
            btn = QPushButton(f"Item {i}")
            btn.setFixedSize(120, random.randint(150, 450))
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addWidget(btn)


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("固定大小的响应式瀑布流")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = WaterfallWidget()
        scroll.setWidget(content)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.resize(800, 600)
    w.show()
    sys.exit(app.exec())
