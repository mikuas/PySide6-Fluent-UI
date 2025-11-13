from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QFont, QColor

class MovingText(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 150)
        self.text = "PySide6 动画文字"
        self.x = self.width()  # 起始位置
        self.direction = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_text)
        self.timer.start(16)

    def move_text(self):
        # 左右移动逻辑
        if self.x > self.width() // 3:
            self.x -= 28 * self.direction
        else:
            self.x -= 12 * self.direction
        if self.x <= 12:
            self.timer.stop()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setFont(QFont("Microsoft YaHei", 26))
        painter.setPen(QColor("#00BFFF"))
        painter.drawText(self.x, 80, self.text)

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        self.x = self.width()
        self.timer.start(16)

app = QApplication([])
win = MovingText()
win.show()
app.exec()
