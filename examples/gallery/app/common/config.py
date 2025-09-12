# coding:utf-8
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6FluentUI import Theme, qconfig, QConfig, ConfigItem, BoolValidator

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000

def update():
    for w in QApplication.allWidgets():
        try:
            w.update()
        except TypeError:
            continue


class Config(QConfig):

    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    acrylicEnabled = ConfigItem("MainWindow", "AcrylicEnabled", False, BoolValidator())


CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.json"
cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(CONFIG_PATH, cfg)