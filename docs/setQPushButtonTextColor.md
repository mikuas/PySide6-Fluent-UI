### 通过QPalette设置QPushButton的文字颜色

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt

button: QPushButton = QPushButton("Button")
palette = button.palette()

palette.setColor(QPalette.ColorRole.ButtonText, QColor("deeppink"))
button.setPalette(palette)

```