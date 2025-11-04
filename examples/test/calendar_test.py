from PySide6.QtWidgets import QApplication, QWidget, QCalendarWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class CustomCalendar(QCalendarWidget):
    def __init__(self):
        super().__init__()
        self.setGridVisible(True)
        self.setFirstDayOfWeek(Qt.Monday)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # 设置图标（可选）
        self.setNavigationBarVisible(True)

        # 设置样式表（QSS）
        self.setStyleSheet("""
            /* 整体背景 */
            QCalendarWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border-radius: 10px;
            }

            /* 顶部导航栏 */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #3c3f41;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                height: 40px;
            }

            /* 年月按钮 */
            QCalendarWidget QToolButton {
                background-color: #4c5052;
                color: #ffffff;
                border-radius: 6px;
                padding: 4px 10px;
                font: bold 13px "Microsoft YaHei";
            }

            /* 悬停效果 */
            QCalendarWidget QToolButton:hover {
                background-color: #5e9eff;
            }

            /* 左右箭头按钮 */
            QCalendarWidget QToolButton#qt_calendar_prevmonth,
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                width: 30px;
                height: 30px;
                icon-size: 20px;
                border-radius: 15px;
                background-color: #4c5052;
            }

            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
                background-color: #5e9eff;
            }

            /* 星期标题 */
            QCalendarWidget QTableView {
                selection-background-color: #88c0d0;
                selection-color: black;
                font: 12px "Microsoft YaHei";
                outline: none;
            }

            QCalendarWidget QTableView::item {
                border: none;
                margin: 3px;
            }

            /* 当前日期 */
            QCalendarWidget QTableView::item:selected {
                background-color: #81a1c1;
                color: black;
                border-radius: 10px;
            }

            /* 今天的日期加亮显示 */
            QCalendarWidget QTableView::item:focus {
                background-color: #a3be8c;
                border-radius: 10px;
            }

            /* 星期标题栏 */
            QCalendarWidget QHeaderView::section {
                background-color: #43484d;
                color: #ffffff;
                font-weight: bold;
                border: none;
                height: 25px;
            }
        """)


class CalendarDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自定义日历控件")
        self.resize(400, 350)

        layout = QVBoxLayout(self)
        self.calendar = CustomCalendar()
        layout.addWidget(self.calendar)

if __name__ == "__main__":
    app = QApplication([])
    window = CalendarDemo()
    window.show()
    app.exec()
