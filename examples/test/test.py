from typing import Union
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property, QObject
from PySide6.QtGui import QPainter, QColor, QPen
import sys, math


class Segment(QObject):
    def __init__(self, ratio: float, color: Union[QColor, str], parent: QWidget = None):
        super().__init__(parent)
        self._currentValue = 0.0
        self._hoverScale = 0.0  # 用于放大动画
        self._ratio = ratio
        self._color = QColor(color) if isinstance(color, str) else color

        # 动画：进度变化
        self.currentValueAni = QPropertyAnimation(self, b"currentValue")
        self.currentValueAni.setDuration(800)
        self.currentValueAni.setEasingCurve(QEasingCurve.OutCubic)

        # 动画：放大效果
        self.hoverAni = QPropertyAnimation(self, b"hoverScale")
        self.hoverAni.setDuration(200)
        self.hoverAni.setEasingCurve(QEasingCurve.OutCubic)

    # --- 进度属性 ---
    def getCurrent(self):
        return self._currentValue

    def setCurrent(self, v):
        self._currentValue = v
        if self.parent():
            self.parent().update()

    currentValue = Property(float, getCurrent, setCurrent)

    # --- 悬停放大属性 ---
    def getHoverScale(self):
        return self._hoverScale

    def setHoverScale(self, v):
        self._hoverScale = v
        if self.parent():
            self.parent().update()

    hoverScale = Property(float, getHoverScale, setHoverScale)

    def ratio(self): return self._ratio
    def color(self): return self._color


class MultiSegmentProgressRing(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.segments = []
        self.hoverIndex = -1
        self.setMouseTracking(True)

    def addSegment(self, ratio: float, color: Union[QColor, str]):
        seg = Segment(ratio, color, self)
        self.segments.append(seg)
        seg.currentValueAni.setStartValue(0)
        seg.currentValueAni.setEndValue(seg.ratio())
        seg.currentValueAni.start()
        self.update()

    def paintEvent(self, event):
        if not self.segments:
            return

        size = min(self.width(), self.height())
        baseRadius = size / 2 - 12
        center = self.rect().center()
        startAngle = -90
        totalGap = len(self.segments)
        totalCurrent = sum(seg.currentValue for seg in self.segments)
        if totalCurrent == 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for i, seg in enumerate(self.segments):
            spanAngle = (seg.currentValue / totalCurrent) * (360 - totalGap)
            radius = baseRadius + 6 * seg.hoverScale
            penWidth = 12 + 4 * seg.hoverScale

            pen = QPen(seg.color(), penWidth)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawArc(
                center.x() - radius,
                center.y() - radius,
                radius * 2,
                radius * 2,
                int(startAngle * 16),
                int(spanAngle * 16)
            )
            startAngle += spanAngle

    def mouseMoveEvent(self, event):
        """检测悬停的弧段并触发动画"""
        pos = event.position()
        center = self.rect().center()
        dx, dy = pos.x() - center.x(), pos.y() - center.y()
        distance = math.hypot(dx, dy)

        size = min(self.width(), self.height())
        baseRadius = size / 2 - 12
        inner = baseRadius - 12
        outer = baseRadius + 12

        if not (inner <= distance <= outer):
            self._clearHover()
            return

        angle = math.degrees(math.atan2(-dy, dx))
        angle = (angle + 360 + 90) % 360

        totalCurrent = sum(seg.currentValue for seg in self.segments)
        totalGap = 5 * len(self.segments)
        startAngle = 0
        newHover = -1

        for i, seg in enumerate(self.segments):
            spanAngle = (seg.currentValue / totalCurrent) * (360 - totalGap)
            if startAngle <= angle <= startAngle + spanAngle:
                newHover = i
                break
            startAngle += spanAngle + 5

        if newHover != self.hoverIndex:
            self._applyHover(newHover)

    def leaveEvent(self, event):
        self._clearHover()

    # --- 动画控制 ---
    def _applyHover(self, index: int):
        if self.hoverIndex == index:
            return
        if 0 <= self.hoverIndex < len(self.segments):
            seg = self.segments[self.hoverIndex]
            seg.hoverAni.stop()
            seg.hoverAni.setStartValue(seg.hoverScale)
            seg.hoverAni.setEndValue(0.0)
            seg.hoverAni.start()
        self.hoverIndex = index
        if 0 <= index < len(self.segments):
            seg = self.segments[index]
            seg.hoverAni.stop()
            seg.hoverAni.setStartValue(seg.hoverScale)
            seg.hoverAni.setEndValue(1.0)
            seg.hoverAni.start()

    def _clearHover(self):
        if 0 <= self.hoverIndex < len(self.segments):
            seg = self.segments[self.hoverIndex]
            seg.hoverAni.stop()
            seg.hoverAni.setStartValue(seg.hoverScale)
            seg.hoverAni.setEndValue(0.0)
            seg.hoverAni.start()
        self.hoverIndex = -1


class DemoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 520)
        layout = QVBoxLayout(self)
        self.progress = MultiSegmentProgressRing(self)
        layout.addWidget(self.progress)

        self.progress.addSegment(10, "red")
        self.progress.addSegment(10, "blue")
        self.progress.addSegment(80, "green")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec())
