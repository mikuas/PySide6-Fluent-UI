# coding:utf-8
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, Qt


def customRoundPixmap(image: str, r1: int, r2: int, r3: int, r4: int) -> QPixmap:
    pixmap = QPixmap(image)
    w, h = pixmap.width(), pixmap.height()

    result = QPixmap(w, h)
    result.fill(Qt.transparent)

    painter = QPainter(result)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()

    path.moveTo(r1, 0)
    path.lineTo(w - r2, 0)
    path.quadTo(w, 0, w, r2)
    path.lineTo(w, h - r3)
    path.quadTo(w, h, w - r3, h)
    path.lineTo(r4, h)
    path.quadTo(0, h, 0, h - r4)
    path.lineTo(0, r1)
    path.quadTo(0, 0, r1, 0)
    path.closeSubpath()

    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return result