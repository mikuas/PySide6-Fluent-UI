## 使用QPixmap缩放图片

```python
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Qt


pixmap: QPixmap = QPixmap()
width: int = 328
height: int = 328
pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

```

### AspectRatioMode（比例模式）

| 模式 | 枚举值 | 说明 |
|------|--------|------|
| `Qt.IgnoreAspectRatio` | `0` | 忽略宽高比，直接拉伸到目标尺寸，图像可能变形。 |
| `Qt.KeepAspectRatio` | `1` | 保持宽高比例缩放，确保图像不变形，可能留空白区域。 |
| `Qt.KeepAspectRatioByExpanding` | `2` | 保持比例并放大直到充满目标区域，超出部分会被裁剪。 |

---

### TransformationMode（缩放质量）

| 模式 | 枚举值 | 说明 |
|------|--------|------|
| `Qt.FastTransformation` | `0` | 快速缩放（最近邻算法），速度快但质量较差，边缘可能出现锯齿。 |
| `Qt.SmoothTransformation` | `1` | 平滑缩放（双线性插值），速度较慢但质量高，边缘平滑自然。 |
