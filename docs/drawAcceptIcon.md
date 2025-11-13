#### 绘制✔️
```python

painter = QPainter(self)
painter.setPen(QPen(QColor(0, 0, 0), 2))
painter.setBrush(Qt.NoBrush)

path = QPainterPath()
w, h = self.width(), self.height()
path.moveTo(w - 30, h - 25)     # 移动到点
path.lineTo(w - 25, h - 20)     # 从当前点到目标点画一条线
path.lineTo(w - 12, h - 32)
painter.drawPath(path)          # 绘制路径
```