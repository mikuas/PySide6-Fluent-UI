# # coding:utf-8
# from PySide6.QtWidgets import QWidget, QApplication
# from PySide6.QtGui import QPainter, QColor, QPen
# from PySide6.QtCore import Qt, QRect
# import sys
#
#
# class ColorPalette(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.rows = 6
#         self.cols = 8
#         self.cell_size = 40
#         self.spacing = 5
#         self.radius = 6
#         self.selected = (2, 5)  # 默认选中 (row=2, col=5)
#
#         # 定义颜色表（这里只写了一部分，可以自己扩展）
#         self.colors = [
#             ["#ffffff", "#000000", "#4472C4", "#5B9BD5", "#A5A5A5", "#FFC000", "#70AD47", "#264478"],
#             ["#F2F2F2", "#7F7F7F", "#D9E1F2", "#DEEAF6", "#EDEDED", "#FFF2CC", "#E2EFDA", "#D9EAD3"],
#             ["#D9D9D9", "#595959", "#B4C6E7", "#BDD7EE", "#F4B084", "#FFE699", "#C6E0B4", "#9BC2E6"],
#             ["#BFBFBF", "#404040", "#8EA9DB", "#9DC3E6", "#E7A38D", "#FFD966", "#A9D08E", "#8EAADB"],
#             ["#A6A6A6", "#262626", "#2F5597", "#4472C4", "#C65911", "#BF9000", "#548235", "#385723"],
#             ["#7F7F7F", "#0D0D0D", "#1F3864", "#203864", "#833C0C", "#7F6000", "#375623", "#274E13"]
#         ]
#
#         self.setFixedSize(self.cols * (self.cell_size + self.spacing),
#                           self.rows * (self.cell_size + self.spacing))
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#
#         for r in range(self.rows):
#             for c in range(self.cols):
#                 color = QColor(self.colors[r][c])
#                 x = c * (self.cell_size + self.spacing)
#                 y = r * (self.cell_size + self.spacing)
#                 rect = QRect(x, y, self.cell_size, self.cell_size)
#
#                 painter.setBrush(color)
#                 painter.setPen(Qt.NoPen)
#                 painter.drawRoundedRect(rect, self.radius, self.radius)
#
#                 # 选中状态：加边框
#                 if (r, c) == self.selected:
#                     pen = QPen(Qt.black, 2)
#                     painter.setPen(pen)
#                     painter.setBrush(Qt.NoBrush)
#                     painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1),
#                                             self.radius, self.radius)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = ColorPalette()
#     w.show()
#     sys.exit(app.exec())

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QRect
import math
import sys

# ------- 辅助色彩转换函数（sRGB <-> XYZ <-> Lab） -------
# 常量
_Xn, _Yn, _Zn = 0.95047, 1.00000, 1.08883  # D65 参考白

def hex_to_rgb01(hexstr):
    s = hexstr.lstrip("#")
    r = int(s[0:2], 16) / 255.0
    g = int(s[2:4], 16) / 255.0
    b = int(s[4:6], 16) / 255.0
    return r, g, b

def srgb_to_linear(c):
    # gamma 解码
    if c <= 0.04045:
        return c / 12.92
    else:
        return ((c + 0.055) / 1.055) ** 2.4

def linear_to_srgb(c):
    if c <= 0.0031308:
        return 12.92 * c
    else:
        return 1.055 * (c ** (1 / 2.4)) - 0.055

def rgb01_to_xyz(r, g, b):
    # 先 gamma -> linear
    r_l = srgb_to_linear(r)
    g_l = srgb_to_linear(g)
    b_l = srgb_to_linear(b)
    # sRGB -> XYZ (D65)
    X = 0.4124564 * r_l + 0.3575761 * g_l + 0.1804375 * b_l
    Y = 0.2126729 * r_l + 0.7151522 * g_l + 0.0721750 * b_l
    Z = 0.0193339 * r_l + 0.1191920 * g_l + 0.9503041 * b_l
    return X, Y, Z

def xyz_to_rgb01(X, Y, Z):
    # XYZ -> linear RGB
    r_l =  3.2404542 * X - 1.5371385 * Y - 0.4985314 * Z
    g_l = -0.9692660 * X + 1.8760108 * Y + 0.0415560 * Z
    b_l =  0.0556434 * X - 0.2040259 * Y + 1.0572252 * Z
    # linear -> srgb
    r = linear_to_srgb(r_l)
    g = linear_to_srgb(g_l)
    b = linear_to_srgb(b_l)
    # clip 0..1
    return max(0.0, min(1.0, r)), max(0.0, min(1.0, g)), max(0.0, min(1.0, b))

def f_inv(t):
    # Lab 反函数的一部分
    epsilon = 0.008856
    kappa = 903.3
    if t ** 3 > epsilon:
        return t ** 3
    else:
        return (116 * t - 16) / kappa

def f_forward(t):
    epsilon = 0.008856
    if t > epsilon:
        return t ** (1/3)
    else:
        kappa = 903.3
        return (kappa * t + 16) / 116

def xyz_to_lab(X, Y, Z):
    xr = X / _Xn
    yr = Y / _Yn
    zr = Z / _Zn
    fx = f_forward(xr)
    fy = f_forward(yr)
    fz = f_forward(zr)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return L, a, b

def lab_to_xyz(L, a, b):
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200
    X = _Xn * f_inv(fx)
    Y = _Yn * f_inv(fy)
    Z = _Zn * f_inv(fz)
    return X, Y, Z

def lab_to_rgb_qcolor(L, a, b):
    X, Y, Z = lab_to_xyz(L, a, b)
    r, g, bb = xyz_to_rgb01(X, Y, Z)
    return QColor(int(r * 255), int(g * 255), int(bb * 255))


# ------- Widget 实现 -------
class ColorPalette(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 你可以把这里替换成你想要的基色（每列一个）
        self.base_colors = [
            "#ffffff", "#d40000", "#2f5597", "#5b9bd5",
            "#a5a5a5", "#ffc000", "#70ad47", "#2b65b0"
        ]
        self.cols = len(self.base_colors)
        self.rows = 5

        self.cell_size = 48
        self.spacing = 8
        self.radius = 8
        self.selected = (0, 0)

        # 目标 L 值（从上到下）：你可以调这些值来得到更接近你想要的视觉效果
        # Lab 中 L 范围通常 0..100
        self.lightness_levels = [88, 68, 51, 39, 24]

        # 每行的 chroma 缩放（避免浅色时过饱和或失真）
        self.chroma_scale = [0.7, 0.9, 1.0, 1.0, 1.0]

        # 生成颜色矩阵
        self.colors = self._generate_colors_lab()

        total_w = self.spacing + self.cols * (self.cell_size + self.spacing)
        total_h = self.spacing + self.rows * (self.cell_size + self.spacing)
        self.setFixedSize(total_w, total_h)

    def _generate_colors_lab(self):
        matrix = []
        for row in range(self.rows):
            L_target = self.lightness_levels[row]
            c_scale = self.chroma_scale[row] if row < len(self.chroma_scale) else 1.0
            row_colors = []
            for col, base_hex in enumerate(self.base_colors):
                r, g, b = hex_to_rgb01(base_hex)
                X, Y, Z = rgb01_to_xyz(r, g, b)
                L0, a0, b0 = xyz_to_lab(X, Y, Z)
                # 计算新的 a,b（按 chroma scale 缩放）
                C0 = math.hypot(a0, b0)
                if C0 < 1e-6:
                    # 基色接近灰/白/黑，保持 a,b 小幅度处理
                    a_new = a0 * 0.3
                    b_new = b0 * 0.3
                else:
                    scale = c_scale
                    a_new = a0 * scale
                    b_new = b0 * scale

                # 构造 Lab -> RGB（若超出 gamut 会被裁切）
                qc = lab_to_rgb_qcolor(L_target, a_new, b_new)
                row_colors.append(qc)
            matrix.append(row_colors)
        return matrix

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.colors[r][c]
                x = self.spacing + c * (self.cell_size + self.spacing)
                y = self.spacing + r * (self.cell_size + self.spacing)
                rect = QRect(x, y, self.cell_size, self.cell_size)

                painter.setPen(Qt.NoPen)
                painter.setBrush(color)
                painter.drawRoundedRect(rect, self.radius, self.radius)

                if (r, c) == self.selected:
                    pen = QPen(QColor(0, 0, 0), 3)
                    painter.setPen(pen)
                    painter.setBrush(Qt.NoBrush)
                    painter.drawRoundedRect(rect.adjusted(2, 2, -2, -2),
                                            self.radius, self.radius)

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        for r in range(self.rows):
            for c in range(self.cols):
                rx = self.spacing + c * (self.cell_size + self.spacing)
                ry = self.spacing + r * (self.cell_size + self.spacing)
                rect = QRect(rx, ry, self.cell_size, self.cell_size)
                if rect.contains(x, y):
                    self.selected = (r, c)
                    chosen = self.colors[r][c]
                    print("Selected:", chosen.name())  # 输出 hex 值
                    self.update()
                    return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ColorPalette()
    w.show()
    sys.exit(app.exec())
