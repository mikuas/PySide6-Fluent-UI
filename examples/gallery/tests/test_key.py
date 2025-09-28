# coding:utf-8
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QKeySequenceEdit, QLabel

app = QApplication([])

win = QWidget()
layout = QVBoxLayout(win)

label = QLabel("当前快捷键: ")
key_edit = QKeySequenceEdit()

def on_key_changed(seq):
    label.setText("当前快捷键: " + seq.toString())

key_edit.keySequenceChanged.connect(on_key_changed)

layout.addWidget(key_edit)
layout.addWidget(label)

win.show()
app.exec()
