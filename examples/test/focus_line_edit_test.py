# coding:utf-8
import sys

from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton

from build.lib.PySide6FluentUI import setCustomStyleSheet
from examples.window.splitWidget.demo import Interface


class FocusLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(
            """
                FocusLineEdit {
                    color: black;
                    background-color: rgba(255, 255, 255, 0.7);
                    border: none;
                    border-radius: 5px;
                    padding: 0px 10px;
                    selection-background-color: --ThemeColorLight1;
                }

                FocusLineEdit:hover {
                    background-color: rgba(249, 249, 249, 0.5);
                }

                FocusLineEdit:disabled{
                    color: rgba(0, 0, 0, 92);
                    background-color: rgba(249, 249, 249, 0.3);
                }
            """
        )

    def paintEvent(self, e):
        painter = QPainter(self)



class Window(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.focusLineEdit: FocusLineEdit = FocusLineEdit(self)

        self.button: QPushButton = QPushButton(self)

        self.viewLayout.addWidget(self.focusLineEdit)
        self.viewLayout.addWidget(self.button)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()