# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout

from PySide6FluentUI import SmoothScrollArea

from ..widgets.sample_card_view import SampleCardView
from ..widgets.banner_widget import BannerWidget


class HomeInterface(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HomeInterface")
        self.bannerWidget: BannerWidget = BannerWidget(self)
        self.__initScrollArea()

        self.viewLayout.addWidget(self.bannerWidget)
        self.__initSampleCardView()

    def __initSampleCardView(self):
        basicInputSampleView: SampleCardView = SampleCardView("Basic Input Samples", self)
        basicInputSampleView.addSampleCard(
            QIcon(":/gallery/controls/Button.png"),
            "按钮",
            "一个响应用户输入并发出点击信号的控制器."
        )
        basicInputSampleView.addSampleCard(
            QIcon(":/gallery/controls/Button.png"),
            "Chip",
            "一个响应用户输入并发出点击信号的控制器."
        )
        basicInputSampleView.addSampleCard(
            QIcon(":/gallery/controls/ComboBox.png"),
            "多选下拉框",
            "一个用户可选的下拉菜单."
        )
        basicInputSampleView.addSampleCard(
            QIcon(":/gallery/controls/Slider.png"),
            "滑块",
            "该控制键允许用户通过沿轨道移动拇指控制来从多个数值中选择."
        )
        self.viewLayout.addWidget(basicInputSampleView)

        dateTimeSamplesView: SampleCardView = SampleCardView("Date&Time Sa,[;es", self)
        dateTimeSamplesView.addSampleCard(
            QIcon(":/gallery/controls/CalendarDatePicker.png"),
            "日历选择器",
            "一个允许用户通过日历选择日期值的控件."
        )
        self.viewLayout.addWidget(dateTimeSamplesView)

        dialogSamplesView: SampleCardView = SampleCardView("Dialog Samples", self)
        dialogSamplesView.addSampleCard(
            QIcon(":/gallery/controls/ColorPicker.png"),
            "下拉调色板",
            "一个允许用户选择颜色的下拉调色板."
        )
        dialogSamplesView.addSampleCard(
            QIcon(":/gallery/controls/RelativePanel.png"),
            "浮出控件对话框",
            "一个允许自定义布局的飞出对话框."
        )
        self.viewLayout.addWidget(dialogSamplesView)

        layoutSamplesView: SampleCardView = SampleCardView("Layout Samples", self)
        layoutSamplesView.addSampleCard(
            QIcon(":/gallery/controls/SplitView.png"),
            "拆分器",
            "一个允许用户调整内部小部件大小的小部件."
        )
        self.viewLayout.addWidget(layoutSamplesView)

        viewSamplesView: SampleCardView = SampleCardView("View Samples", self)
        viewSamplesView.addSampleCard(
            QIcon(":/gallery/controls/Grid.png"),
            "分页器",
            "一个控制功能，允许用户在页码无法直观显示时，在分页集合中导航."
        )
        self.viewLayout.addWidget(viewSamplesView)

    def __initScrollArea(self):
        self._widget: QWidget = QWidget()
        self.viewLayout: QVBoxLayout = QVBoxLayout(self._widget)

        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidget(self._widget)
        self.setWidgetResizable(True)
        self.enableTransparentBackground()

    def resizeEvent(self, e):
        super().resizeEvent(e)


def main():
    import sys
    import examples.gallery.resources.gallery_resources
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = HomeInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()