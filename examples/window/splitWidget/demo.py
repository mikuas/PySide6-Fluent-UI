# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication

from PySide6FluentUI import SplitWidget, TransparentToolButton, FluentIcon, setToolTipInfo, toggleTheme, themeColor


def update():
    for w in QApplication.allWidgets():
        try:
            w.update()
        except Exception:
            continue


class Interface(SplitWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.toggleThemeButton: TransparentToolButton = TransparentToolButton(FluentIcon.BRUSH, self)
        self.enableMicaEffectButton: TransparentToolButton = TransparentToolButton(FluentIcon.TRANSPARENT.colored(themeColor(), themeColor()), self)

        self.toggleThemeButton.setFixedSize(46, 32)
        self.enableMicaEffectButton.setFixedSize(46, 32)

        self.titleBar.hBoxLayout.insertWidget(4, self.toggleThemeButton)
        self.titleBar.hBoxLayout.insertWidget(6, self.enableMicaEffectButton)

        setToolTipInfo(self.toggleThemeButton, "切换当前主题", 2500)
        setToolTipInfo(self.enableMicaEffectButton, "启用MicaEffect", 2500)

        info = sys.getwindowsversion()
        self.enableMicaEffectButton.setEnabled(info.major == 10 and info.build >= 22000)

        if __name__ == "__main__":
            self.connectSignalSlot()

    def verify(self, value: str):
        try:
            return int(value)
        except ValueError:
            return False

    def connectSignalSlot(self):
        self.toggleThemeButton.clicked.connect(lambda: {toggleTheme(), update()})
        self.enableMicaEffectButton.clicked.connect(
            lambda: {
                self.setMicaEffectEnabled(not self.isMicaEffectEnabled()),
                self.enableMicaEffectButton.setIcon(FluentIcon.TRANSPARENT.colored(themeColor(), themeColor()) if self.isMicaEffectEnabled() else FluentIcon.TRANSPARENT)
            }
        )

def main():
    import sys
    app = QApplication(sys.argv)
    window = Interface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()