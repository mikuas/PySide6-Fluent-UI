# coding:utf-8
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices
from PySide6FluentUI import TitleLabel, SubtitleLabel, CaptionLabel, PushButton, FluentIcon, ToolButton, \
    setToolTipInfos, ToolTipPosition, ImageLabel, MessageBoxBase, toggleTheme, ScrollArea

from ..common.config import update


class PaymentMessageBox(MessageBoxBase):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        # self.__PATH__: str = str(Path(__file__).resolve().parents[2] / "resources" / "images")
        self.__PATH__: str = ":/gallery/images"
        self.titleLabel: SubtitleLabel = SubtitleLabel(title, self)
        self.paymentWidget: ImageLabel = ImageLabel(f"{self.__PATH__}/Alipay.png", self)
        self.paymentWidget.setProperty("Pay", "Alipay")

        self.paymentWidget.setFixedSize(256, 328)
        self.paymentWidget.setBorderRadius(8, 8, 8, 8)

        self.viewLayout.addWidget(self.titleLabel, alignment=Qt.AlignHCenter)
        self.viewLayout.addWidget(self.paymentWidget)

        self.cancelButton.setText("下次一定")
        self.yesButton.setText("切换支付方式")

        self.hide()

    def showEvent(self, e):
        self.raise_()
        super().showEvent(e)

    def validate(self):
        pay = "Alipay" if self.paymentWidget.property("Pay") == "WeChat" else "WeChat"
        self.paymentWidget.setProperty("Pay", pay)
        self.paymentWidget.setImage(f"{self.__PATH__}/{pay}.png")
        self.paymentWidget.setFixedSize(256, 328)
        return False


class Interface(QWidget):
    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent)
        self.vBoxLayout: QVBoxLayout = QVBoxLayout(self)

        self.__initWidget(title, content)
        self.__initScrollArea()
        self.initPaymentMessageBox()
        self.documentButton.clicked.connect(self._openDocumentPage)
        self.sourceCodeButton.clicked.connect(self._openSourceCodePage)
        self.toggleThemeButton.clicked.connect(self._onToggleButton)

        setToolTipInfos(
            [self.documentButton, self.sourceCodeButton, self.toggleThemeButton, self.likeButton],
            ["查看在线文档", "查看源代码", "切换主题", "支持一下作者🥰"], 2500, ToolTipPosition.TOP
        )

    def __initWidget(self, title: str, content: str):
        self.title: TitleLabel = TitleLabel(title, self)
        self.content: CaptionLabel = CaptionLabel(content, self)
        self.documentButton: PushButton = PushButton(FluentIcon.DOCUMENT, "在线文档", self)
        self.sourceCodeButton: PushButton = PushButton(FluentIcon.GITHUB, "源代码", self)
        self.toggleThemeButton: ToolButton = ToolButton(FluentIcon.CONSTRACT, self)
        self.likeButton: ToolButton = ToolButton(FluentIcon.HEART, self)

        self.__initLayout()

    def __initLayout(self):
        self.vBoxLayout.setContentsMargins(28, 25, 0, 20)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        
        self.vBoxLayout.addWidget(self.title)
        self.vBoxLayout.addWidget(self.content)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(0, 0, 28, 0)
        buttonLayout.addWidget(self.documentButton, 0, Qt.AlignLeft)
        buttonLayout.addWidget(self.sourceCodeButton, 0, Qt.AlignLeft)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.toggleThemeButton, 0, Qt.AlignLeft)
        buttonLayout.addWidget(self.likeButton, 0, Qt.AlignRight)

        self.vBoxLayout.addLayout(buttonLayout)
        self.vBoxLayout.addSpacing(20)

    def __initScrollArea(self):
        self._widget: QWidget = QWidget()
        self.scrollLayout: QVBoxLayout = QVBoxLayout(self._widget)
        self.scrollArea: ScrollArea = ScrollArea(self)

        self.scrollArea.setWidget(self._widget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.enableTransparentBackground()
        self.scrollArea.setContentsMargins(0, 0, 0, 0)

        self._widget.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setContentsMargins(0, 0, 18, 0)
        self.scrollLayout.setAlignment(Qt.AlignTop)
    
    def initPaymentMessageBox(self):
        self.paymentMessageBox: PaymentMessageBox = PaymentMessageBox("支持作者", self)
        self.likeButton.clicked.connect(self.paymentMessageBox.show)

    @staticmethod
    def openUrl(url: str) -> bool:
        return QDesktopServices.openUrl(url)

    def _openDocumentPage(self):
        self.openUrl("https://github.com/mikuass/PythonModule.git")

    def _openSourceCodePage(self):
        self.openUrl("https://github.com/mikuass/PythonModule.git")

    def _onToggleButton(self):
        toggleTheme(True)
        update()