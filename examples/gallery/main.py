# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication

import resources.app_resources
from app.main_window import MainWindow


def main():

    # PATH = Path(__file__).resolve().parents[0] / "logs"
    # if not Path.exists(PATH):
    #     Path.mkdir(PATH)
    #
    # logging.basicConfig(
    #         filename=f"{PATH}/app.log",
    #         level=logging.INFO,
    #         format="%(asctime)s [%(levelname)s]: %(message)s",
    #         datefmt="%Y-%m-%d %H:%M:%S",
    #         encoding="utf-8"
    # )

    app = QApplication(sys.argv)
    window = MainWindow()
    window.setMinimumSize(700, 600)
    window.show()
    sys.exit(app.exec())


main()