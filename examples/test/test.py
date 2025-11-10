from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QColorDialog
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QObject
from PySide6.QtGui import QPainter, QColor, QPen, QFont
import sys
import random

# ----------------- Segment 类 -----------------
class Segment(QObject):
    def __init__(self, ratio=0.0, color="#0078D7"):
        super().__init__()
        self._current = 0.0
        self.ratio = ratio
        self.color = color

    def getCurrent(self):
        return self._current

    def setCurrent(self, value):
        self._current = value

    current = Property(float, getCurrent, setCurrent)

# ----------------- MultiSegmentProgressRing -----------------
class MultiSegmentProgressRing(QWidget):
    def __init__(self, segments_percent=None, line_width=12, gap_angle=5, parent=None):
        """
        初始化环形进度条
        segments_percent = [{"percent": 40, "color": "#0078D7"}, {"percent": None, "color": "#E81123"}, ...]
        """
        super().__init__(parent)
        self.line_width = line_width
        self.gap_angle = gap_angle
        self.animations = []
        self.segments = []
        if segments_percent:
            self.setSegmentsPercent(segments_percent, animate=False)

    # ----------------- 设置段百分比 -----------------
    def setSegmentsPercent(self, segments_percent, animate=True):
        """
        segments_percent:
        - 每个段 {"percent": float or None, "color": str}
        - percent 为 None 表示剩余百分比分配
        - 总百分比固定为 100
        """
        # 计算已固定百分比总和
        total_fixed = sum(item["percent"] for item in segments_percent if item["percent"] is not None)
        total_fixed = min(total_fixed, 100)  # 最大不超过100
        remaining_percent = max(0, 100 - total_fixed)

        # 剩余段数
        remaining_count = sum(1 for item in segments_percent if item["percent"] is None)

        # 分配剩余百分比
        for item in segments_percent:
            if item["percent"] is None:
                if remaining_count > 0:
                    item["percent"] = remaining_percent / remaining_count
                else:
                    item["percent"] = 0

        # 转换成比例
        segments_data = [{"ratio": item["percent"]/100, "color": item["color"]} for item in segments_percent]
        self.setSegments(segments_data, animate)

    # ----------------- 内部设置段比例 -----------------
    def setSegments(self, segments_data, animate=True):
        if len(segments_data) != len(self.segments):
            self.segments = [Segment(d["ratio"], d["color"]) for d in segments_data]

        # 停止之前动画
        for anim in self.animations:
            anim.stop()
        self.animations.clear()

        for seg, new in zip(self.segments, segments_data):
            seg.color = new.get("color", seg.color)
            target_ratio = new.get("ratio", seg.ratio)
            seg.ratio = target_ratio
            if animate:
                anim = QPropertyAnimation(seg, b"current", self)
                anim.setDuration(800)
                anim.setStartValue(seg.current)
                anim.setEndValue(target_ratio)
                anim.setEasingCurve(QEasingCurve.OutCubic)
                anim.valueChanged.connect(self.update)
                anim.start()
                self.animations.append(anim)
            else:
                seg._current = target_ratio
        self.update()

    # ----------------- 增加段 -----------------
    def addSegment(self, percent=None, color="#0078D7"):
        """
        percent: 百分比，可为 None 表示剩余自动分配
        """
        if percent is None:
            percent = 0  # 初始动画从0
        ratio = percent / 100
        new_seg = Segment(ratio, color)
        self.segments.append(new_seg)
        anim = QPropertyAnimation(new_seg, b"current", self)
        anim.setDuration(800)
        anim.setStartValue(0.0)
        anim.setEndValue(ratio)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.valueChanged.connect(self.update)
        anim.start()
        self.animations.append(anim)
        self.update()

    # ----------------- 减少段 -----------------
    def removeSegment(self, index=-1):
        if self.segments:
            if index < 0 or index >= len(self.segments):
                index = len(self.segments) - 1
            self.segments.pop(index)
            self.update()

    # ----------------- 改变某段百分比 -----------------
    def setSegmentPercent(self, index, percent):
        if 0 <= index < len(self.segments):
            ratio = percent / 100
            seg = self.segments[index]
            anim = QPropertyAnimation(seg, b"current", self)
            anim.setDuration(800)
            anim.setStartValue(seg.current)
            anim.setEndValue(ratio)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.valueChanged.connect(self.update)
            anim.start()
            self.animations.append(anim)
            seg.ratio = ratio
        self.update()

    # ----------------- 绘制 -----------------
    def paintEvent(self, event):
        size = min(self.width(), self.height())
        radius = size / 2 - self.line_width
        center = self.rect().center()
        start_angle = -90

        total_current = sum(seg.current for seg in self.segments)
        segment_count = len(self.segments)
        total_gap = self.gap_angle * segment_count

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for seg in self.segments:
            span_angle = (seg.current / total_current) * (360 - total_gap) if total_current > 0 else 0
            pen = QPen(QColor(seg.color), self.line_width)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawArc(
                center.x() - radius,
                center.y() - radius,
                radius*2,
                radius*2,
                int(start_angle*16),
                int(span_angle*16)
            )
            start_angle += span_angle + self.gap_angle

        # 中心百分比显示
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", int(radius/2)))
        percent = int(total_current * 100)
        painter.drawText(self.rect(), Qt.AlignCenter, f"{percent}%")
        painter.end()


# ----------------- 演示窗口 -----------------
class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MultiSegmentProgressRing - 固定总值100版本")
        self.resize(400, 400)

        init_segments = [
            {"percent": 40, "color": "#0078D7"},
            {"percent": 35, "color": "#E81123"},
            {"percent": 25, "color": "#FFB900"}
        ]

        self.progress = MultiSegmentProgressRing(init_segments, gap_angle=5)

        # 按钮
        btn_add = QPushButton("增加段")
        btn_add.clicked.connect(self.addSegmentDialog)
        btn_remove = QPushButton("减少段")
        btn_remove.clicked.connect(lambda: self.progress.removeSegment())
        btn_random = QPushButton("随机更新百分比")
        btn_random.clicked.connect(self.randomUpdate)

        layout = QVBoxLayout(self)
        layout.addWidget(self.progress, 1)
        layout.addWidget(btn_add)
        layout.addWidget(btn_remove)
        layout.addWidget(btn_random)

    # ----------------- 弹窗增加段 -----------------
    def addSegmentDialog(self):
        percent, ok = QInputDialog.getText(self, "增加段", "输入百分比 (0~100, 留空表示自动分配):")
        if not ok:
            return
        if percent.strip() == "":
            percent_val = None
        else:
            try:
                percent_val = float(percent)
                if percent_val < 0 or percent_val > 100:
                    percent_val = None
            except:
                percent_val = None

        color = QColorDialog.getColor(Qt.green, self, "选择颜色")
        if not color.isValid():
            color = QColor("#32CD32")
        self.progress.addSegment(percent_val, color.name())

    # ----------------- 随机更新百分比 -----------------
    def randomUpdate(self):
        n = len(self.progress.segments)
        if n == 0:
            return
        vals = [random.random() for _ in range(n)]
        total = sum(vals)
        percents = [v/total*100 for v in vals]
        new_segments = [{"percent": p, "color": seg.color} for p, seg in zip(percents, self.progress.segments)]
        self.progress.setSegmentsPercent(new_segments)


# ----------------- 主程序 -----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec())
