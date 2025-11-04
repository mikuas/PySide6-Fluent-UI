from typing import Union

from PySide6.QtCore import QRect, QRectF
from PySide6.QtGui import QPainterPath, QPainter


def addRoundPath(rect: Union[QRect, QRectF], tl: Union[int, float], tr: Union[int, float], br: Union[int, float], bl: Union[int, float]) -> QPainterPath:
    path = QPainterPath()

    path.moveTo(rect.left() + tl, rect.top())

    path.lineTo(rect.right() - tr, rect.top())
    path.quadTo(rect.right(), rect.top(), rect.right(), rect.top() + tr)

    path.lineTo(rect.right(), rect.bottom() - br)
    path.quadTo(rect.right(), rect.bottom(), rect.right() - br, rect.bottom())

    path.lineTo(rect.left() + bl, rect.bottom())
    path.quadTo(rect.left(), rect.bottom(), rect.left(), rect.bottom() - bl)

    path.lineTo(rect.left(), rect.top() + tl)
    path.quadTo(rect.left(), rect.top(), rect.left() + tl, rect.top())

    return path

def drawRoundRect(painter: QPainter, rect: Union[QRect, QRectF], tl: Union[int, float], tr: Union[int, float], br: Union[int, float], bl: Union[int, float]) -> None:
    painter.drawPath(addRoundPath(rect, tl, tr, br, bl))