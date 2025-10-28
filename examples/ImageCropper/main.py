# coding:utf-8
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("圆角图片裁剪工具")
    window.setWindowIcon(QIcon("./app.ico"))
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()