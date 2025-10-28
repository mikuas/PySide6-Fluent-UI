# coding:utf-8
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, Qt


def customRoundPixmap(image: str, tl: int, tr: int, br: int, bl: int) -> QPixmap:
    pixmap = QPixmap(image)
    w, h = pixmap.width(), pixmap.height()

    result = QPixmap(w, h)
    result.fill(Qt.transparent)

    painter = QPainter(result)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()

    path.moveTo(tl, 0)
    path.lineTo(w - tr, 0)
    path.quadTo(w, 0, w, tr)
    path.lineTo(w, h - br)
    path.quadTo(w, h, w - br, h)
    path.lineTo(bl, h)
    path.quadTo(0, h, 0, h - bl)
    path.lineTo(0, tl)
    path.quadTo(0, 0, tl, 0)
    path.closeSubpath()

    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return result