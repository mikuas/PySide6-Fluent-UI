# coding:utf-8
from PySide6.QtWidgets import QListWidget
from PySide6.QtCore import Qt
from PySide6FluentUI import RoundListWidget, StrongBodyLabel, Pager, DragFileWidget, DragFolderWidget, ToastInfoBar

from ..widgets.basic_interface import Interface
from ..widgets.widget_item import StandardItem


class ViewInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("视图", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("ViewInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        self.__initRoundListWidget()
        self.__initPagerWidget()
        self.__initDragFilesWidget()
        self.__initDragFolderWidget()
        self.connectSignalSlot()

    def __initRoundListWidget(self):
        self.roundListItem: StandardItem = StandardItem("圆角列表组件", self)
        self.roundListItem.card.setFixedHeight(400)
        self.roundListItem.card.widgetLayout.setContentsMargins(10, 10, 10, 10)

        self.roundListWidget: RoundListWidget = RoundListWidget(self)
        self.roundListWidget.setFixedHeight(316)
        self.roundListWidget.addItems(["Lost in the Wind", "Shining Stars", "Dream of Tomorrow", "Ocean Whisper", "Lonely Road", "Dancing Shadows", "Moonlight Journey", "Silent Tears", "Endless Summer", "Midnight Echo", "Wings of Freedom", "Crystal Sky", "Burning Heart", "Falling Snow", "Golden Horizon", "Echoes of Time", "Rising Flame", "Secret Garden", "Stormy Night", "Peaceful Dawn"])
        self.roundListWidget.setCurrentRow(0)
        self.roundListWidget.enableDoubleItemEdit(True)
        self.roundListWidget.setDragDropMode(self.roundListWidget.DragDropMode.InternalMove)

        # icons = list(FluentIcon)
        # [item.setIcon(toQIcon(icons[self.roundListWidget.indexFromItem(item).row()])) for item in self.roundListWidget.allItems()]

        self.roundListItem.addWidget(self.roundListWidget, 1, Qt.AlignTop)
        self.scrollLayout.addWidget(self.roundListItem)

    def __initPagerWidget(self):
        self.pagerItem: StandardItem = StandardItem("分页组件", self)
        self.pageLabel: StrongBodyLabel = StrongBodyLabel("第 1 页", self)
        self.pager: Pager = Pager(1000, 6, self)

        self.pager.setCurrentPage(1)
        self.pager.currentPageChanged.connect(lambda page: self.pageLabel.setText(f"第 {page} 页"))
        self.pagerItem.addWidget(self.pager, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.pagerItem.addWidget(self.pageLabel, 1, Qt.AlignRight | Qt.AlignVCenter)

        self.pagerItem.card.widgetLayout.setContentsMargins(10, 0, 24, 0)
        self.scrollLayout.addWidget(self.pagerItem)

    def __initDragFilesWidget(self):
        self.dragFileItem: StandardItem = StandardItem("拖放文件组件", self)
        self.dragFileWidget: DragFileWidget = DragFileWidget(isDashLine=True, parent=self)

        self.dragFileItem.card.setFixedHeight(300)

        self.dragFileItem.addWidget(self.dragFileWidget)
        self.scrollLayout.addWidget(self.dragFileItem)

    def __initDragFolderWidget(self):
        self.dragFolderItem: StandardItem = StandardItem("拖放文件夹组件", self)
        self.dragFolderWidget: DragFolderWidget = DragFolderWidget(isDashLine=True, parent=self)

        self.dragFolderItem.card.setFixedHeight(300)

        self.dragFolderItem.addWidget(self.dragFolderWidget)
        self.scrollLayout.addWidget(self.dragFolderItem)

    def connectSignalSlot(self):
        self.dragFileWidget.draggedChange.connect(
            lambda file: ToastInfoBar.success(
                "文件",
                f"拖放的文件是: {file}",
                duration=3500,
                orient=Qt.Orientation.Vertical,
                parent=self
            )
        )
        self.dragFileWidget.selectionChange.connect(
            lambda file: ToastInfoBar.success(
                "文件",
                f"选择的文件是: {file}",
                duration=3500,
                orient=Qt.Orientation.Vertical,
                parent=self
            )
        )

        self.dragFolderWidget.draggedChange.connect(
            lambda file: ToastInfoBar.success(
                "文件",
                f"拖放的文件夹是: {file}",
                duration=3500,
                orient=Qt.Orientation.Vertical,
                parent=self
            )
        )
        self.dragFolderWidget.selectionChange.connect(
            lambda file: ToastInfoBar.success(
                "文件",
                f"选择的文件夹是: {file}",
                duration=3500,
                orient=Qt.Orientation.Vertical,
                parent=self
            )
        )