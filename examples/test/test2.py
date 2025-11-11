from PySide6.QtWidgets import QApplication, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve
import sys

class ShakeDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 200)
        self.setWindowTitle("左右晃动示例")

        # 主布局
        main_layout = QVBoxLayout(self)

        # 包裹 QLineEdit 的容器，避免布局影响动画
        self.container = QWidget(self)
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        self.line_edit = QLineEdit("左右晃动试试")
        container_layout.addWidget(self.line_edit)
        main_layout.addWidget(self.container)

        # 按钮触发动画
        btn = QPushButton("触发晃动")
        main_layout.addWidget(btn)
        btn.clicked.connect(self.shake)

    def shake(self):
        # 保存原始位置
        orig_pos = self.line_edit.pos()

        # 创建动画
        animation = QPropertyAnimation(self.line_edit, b"pos", self)
        animation.setDuration(500)
        animation.setEasingCurve(QEasingCurve.OutElastic)

        # 左右晃动关键帧，幅度递减
        animation.setKeyValueAt(0, orig_pos)
        animation.setKeyValueAt(0.3, orig_pos + QPoint(-20, 0))
        animation.setKeyValueAt(0.6, orig_pos + QPoint(20, 0))
        animation.setKeyValueAt(0.9, orig_pos + QPoint(-10, 0))
        animation.setKeyValueAt(1.2, orig_pos + QPoint(10, 0))
        animation.setKeyValueAt(1.5, orig_pos)

        # 保存引用，防止被回收
        self.animation = animation
        animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = ShakeDemo()
    demo.show()
    sys.exit(app.exec())
