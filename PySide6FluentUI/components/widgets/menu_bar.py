# coding:utf-8
from PySide6.QtWidgets import QMenuBar

from .menu import RoundMenu, MenuAnimationType
from ...common.icon import Action


class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menus = []
    
    def addMenu(self, title: str):
        menu = RoundMenu(title, self)
        action = Action(title, self)
        action.triggered.connect(lambda: self.showMenu(menu, action))
        self.addAction(action)
        self.menus.append(menu)
        return menu

    def showMenu(self, menu: RoundMenu, action: Action):
        pos = self.mapToGlobal(self.actionGeometry(action).bottomLeft())
        pos.setX(pos.x() + 10)
        menu.exec(pos)
    
    def enterEvent(self, event):
        print("ENTER")
        return super().enterEvent(event)