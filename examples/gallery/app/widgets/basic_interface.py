# coding:utf-8
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices, QPainter, QColor, QFont
from PySide6FluentUI import TitleLabel, SubtitleLabel, CaptionLabel, PushButton, FluentIcon, ToolButton, \
    setToolTipInfos, ToolTipPosition, ImageLabel, MessageBoxBase, toggleTheme, ScrollArea, isDarkTheme, drawRoundRect, \
    setFont, BodyLabel, IconWidget

from ..common.config import update
from ..utils.url_utils import openUrl


class WidgetCard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(114)
        self.viewLayout: QHBoxLayout = QHBoxLayout(self)
        self.viewLayout.setContentsMargins(11, 11, 24, 11)
        self.viewLayout.setSpacing(0)
        self.viewLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if isDarkTheme():
            pc = 255
            bc = 0
            a = 32
        else:
            pc = 0
            bc = 243
            a = 170
        painter.setPen(QColor(pc, pc, pc, 16))
        painter.setBrush(QColor(bc, bc, bc, a))
        drawRoundRect(painter, self.rect(), 10, 10, 0, 0)


class CodeLinkCard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isHover: bool = False
        self.setMinimumHeight(57)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self.isHover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.isHover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if isDarkTheme():
            pc = 255
            bc = 52
            a = 64
        else:
            pc = 0
            bc = 255
            a = 170
        painter.setPen(QColor(pc, pc, pc, 16))
        painter.setBrush(QColor(bc, bc, bc, a))
        painter.setOpacity(0.678 if self.isHover else 1)
        drawRoundRect(painter, self.rect(), 0, 0, 10, 10)

    def mouseReleaseEvent(self, event):
        QDesktopServices.openUrl("https://github.com/mikuas/PySide6-Fluent-UI.git")
        super().mouseReleaseEvent(event)


class CardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout: QVBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        self.widgetCard: WidgetCard = WidgetCard(self)
        self.codeLineCard: CodeLinkCard = CodeLinkCard(self)

        self.sourceTitle: BodyLabel = BodyLabel("源代码", self)
        self.iconWidget: IconWidget = IconWidget(FluentIcon.LINK, self)
        self.iconWidget.setFixedSize(16, 16)
        layout: QHBoxLayout = QHBoxLayout(self.codeLineCard)
        layout.addWidget(self.sourceTitle, 0, Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.iconWidget, 1, Qt.AlignRight | Qt.AlignVCenter)

        self.vBoxLayout.addWidget(self.widgetCard, 1)
        self.vBoxLayout.addWidget(self.codeLineCard, 0)


class ExamplesCard(QWidget):
    def __init__(self, title: str, widget: QWidget, stretch=0, parent=None):
        super().__init__(parent)
        self.vBoxLayout: QVBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.title: SubtitleLabel = SubtitleLabel(title, self)
        self.widget: CardWidget = CardWidget(self)

        self.widget.widgetCard.viewLayout.addWidget(widget, 0)
        self.vBoxLayout.addWidget(self.title)
        self.vBoxLayout.addWidget(self.widget, 1)
        # self.vBoxLayout.addStretch(1)

        widget.setParent(self.widget.widgetCard)
        if stretch == 0:
            self.widget.widgetCard.viewLayout.addStretch(1)

        setFont(self.title, 16, QFont.DemiBold)


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
        self.documentButton.clicked.connect(self._openDocumentPage)
        self.sourceCodeButton.clicked.connect(self._openSourceCodePage)
        self.toggleThemeButton.clicked.connect(self._onToggleButton)

        setToolTipInfos(
            [self.documentButton, self.sourceCodeButton, self.toggleThemeButton, self.likeButton],
            ["查看在线文档", "查看源代码", "切换主题", "支持一下作者🥰"], 2500, ToolTipPosition.TOP
        )
        self.likeButton.clicked.connect(lambda: PaymentMessageBox("支持作者", self.window()).exec())

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
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)

        self._widget.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setContentsMargins(0, 0, 18, 0)
        self.scrollLayout.setSpacing(18)
        self.scrollLayout.setAlignment(Qt.AlignTop)

    def addExamplesCard(self, title: str, widget: QWidget, stretch=0):
        card = ExamplesCard(title, widget, stretch, self)
        self.scrollLayout.addWidget(card)
        return card

    def _openDocumentPage(self):
        openUrl("https://github.com/mikuas/PySide6-Fluent-UI")

    def _openSourceCodePage(self):
        openUrl("https://github.com/mikuas/PySide6-Fluent-UI.git")

    def _onToggleButton(self):
        toggleTheme(True)
        update()