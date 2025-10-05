# coding:utf-8
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6FluentUI import ScrollArea, TitleLabel, SubtitleLabel, FluentWindow, SwitchSettingCard, \
    FluentIcon, OptionsSettingCard, setTheme, ColorSettingCard, qconfig, HyperlinkCard, PrimaryPushSettingCard, \
    setThemeColor

from ..common.config import cfg, isWin11, update


class SettingInterface(QWidget):
    def __init__(self, parent: FluentWindow = None):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("SettingInterface")
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setContentsMargins(28, 25, 0, 20)
        self.title = TitleLabel("设置", self)

        self.__initScrollArea()
        self.__initStyleCard()
        self.__initAboutCard()
        self.vLayout.addWidget(self.title, 0, Qt.AlignLeft)
        self.vLayout.addSpacing(16)
        self.vLayout.addWidget(self.scrollArea)

        self.connectSignalSlot()

        self.parent.setMicaEffectEnabled(cfg.micaEnabled.value)
        self.parent.navigationInterface.setAcrylicEnabled(cfg.acrylicEnabled.value)
        cfg.themeChanged.connect(setTheme)

        self.viewLayout.addStretch(1)

    def __initScrollArea(self):
        self.scrollArea: ScrollArea = ScrollArea(self)
        self.__widget: QWidget = QWidget()
        self.viewLayout: QVBoxLayout = QVBoxLayout(self.__widget)
        self.scrollArea.setWidget(self.__widget)
        self.scrollArea.enableTransparentBackground()
        self.scrollArea.setWidgetResizable(True)
        self.viewLayout.setContentsMargins(0, 0, 24, 0)
        
    def __initStyleCard(self):
        self.styleTitle: SubtitleLabel = SubtitleLabel("个性化", self)

        self.micaEffectCard: SwitchSettingCard = SwitchSettingCard(
            FluentIcon.TRANSPARENT,
            "云母效果",
            "窗口表面显示半透明",
            cfg.micaEnabled,
            self
        )
        self.micaEffectCard.setEnabled(isWin11())

        self.acrylicCard: SwitchSettingCard = SwitchSettingCard(
            FluentIcon.ALBUM,
            "亚力克效果",
            "导航面板显示亚力克效果",
            cfg.acrylicEnabled,
            self
        )
        
        self.themeCard: OptionsSettingCard = OptionsSettingCard(
            qconfig.themeMode,
            FluentIcon.BRUSH,
            "应用主题",
            "调整你的应用外观",
            ["浅色", "深色", "跟随系统"],
            self
        )
        
        self.themeColorCard: ColorSettingCard = ColorSettingCard(
            qconfig.themeColor,
            FluentIcon.PALETTE,
            "主题颜色",
            "自定义应用主题颜色",
            self
        )
        
        self.viewLayout.addWidget(self.styleTitle)
        self.viewLayout.addWidget(self.micaEffectCard)
        self.viewLayout.addWidget(self.acrylicCard)
        self.viewLayout.addWidget(self.themeCard)
        self.viewLayout.addWidget(self.themeColorCard)
        
    def __initAboutCard(self):
        self.aboutTitle: SubtitleLabel = SubtitleLabel("关于", self)

        self.helpCard: HyperlinkCard = HyperlinkCard(
            "",
            "打开帮助页面",
            FluentIcon.HELP,
            "帮助",
            "了解组件使用技巧",
            self
        )
        self.aboutCard: PrimaryPushSettingCard = PrimaryPushSettingCard(
            "检查更新",
            FluentIcon.INFO,
            "关于",
            "当前版本 0.0.3"
        )

        self.viewLayout.addSpacing(24)
        self.viewLayout.addWidget(self.aboutTitle)
        self.viewLayout.addWidget(self.helpCard)
        self.viewLayout.addWidget(self.aboutCard)

    def connectSignalSlot(self):
        self.micaEffectCard.checkedChanged.connect(self._onMicaEffectChanged)
        self.acrylicCard.checkedChanged.connect(self.parent.navigationInterface.setAcrylicEnabled)
        self.themeCard.optionChanged.connect(update)
        self.themeColorCard.colorChanged.connect(setThemeColor)

    def _onMicaEffectChanged(self, enable: bool):
        cfg.set(cfg.micaEnabled, enable)
        self.parent.setMicaEffectEnabled(enable)