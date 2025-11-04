# coding:utf-8
from typing import Union

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices


def openUrl(url: Union[str, QUrl]) -> bool:
    return QDesktopServices.openUrl(url)