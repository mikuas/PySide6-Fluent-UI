from PySide6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QWidget

app = QApplication([])

w = QWidget()
layout = QVBoxLayout(w)
file_dialog = QFileDialog()
file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, True)
file_dialog.setFileMode(QFileDialog.FileMode.AnyFile)
layout.addWidget(file_dialog)

w.resize(600, 400)
w.show()
app.exec()
