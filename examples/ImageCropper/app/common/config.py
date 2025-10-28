# coding:utf-8
from pathlib import Path

from PySide6FluentUI import QConfig, ConfigItem, Theme, qconfig, BoolValidator, FolderValidator


class Config(QConfig):

    saveDir: ConfigItem = ConfigItem("Save", "SaveDir", "", FolderValidator())
    isMemorySavePath: ConfigItem = ConfigItem("Save", "IsMemorySavePath", False, BoolValidator())


CONFIG_PATH: Path = Path(__file__).resolve().parents[2] / "config" / "config.json"
cfg: Config = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(CONFIG_PATH, cfg)