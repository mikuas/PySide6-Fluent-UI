from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QColor, QFont
import math, sys

class WaveText(QWidget):
    def __init__(self, text="你好，爸爸~"):
        super().__init__()
        self.text = text
        self.phase = 0
        self.amplitude = 10  # 振幅
        self.speed = 0.15    # 速度
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_wave)
        self.timer.start(16)  # ~60fps
        self.resize(400, 120)

    def update_wave(self):
        self.phase += self.speed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont("Microsoft YaHei", 24))
        painter.setPen(QColor(60, 130, 255))

        base_y = self.height() // 2
        start_x = 30
        spacing = 24

        for i, ch in enumerate(self.text):
            # 每个字符相位错开，形成波浪
            dy = math.sin(self.phase + i * 0.5) * self.amplitude
            x = start_x + i * spacing
            y = base_y + dy
            painter.drawText(x, y, ch)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WaveText("Hello PySide6")
    w.show()
    sys.exit(app.exec())
