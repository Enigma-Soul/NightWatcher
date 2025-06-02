from PySide6.QtWidgets import (QApplication, QWidget, QMenu, QLabel, QDialog, QLineEdit,
                               QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
                               QProgressBar, QDialogButtonBox, QFormLayout)
from PySide6.QtGui import (QPainter, QColor, QPen, QAction, QBrush,
                           QPainterPath, QFont)
from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal, QTimer
from math import log2

"""点阵图组件"""
class DotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # 正确初始化父类
        self.setFixedSize(200, 60)
        self.dots = []
        self.colors = [QColor(100, 150, 250), QColor(250, 150, 100), QColor(150, 250, 100)]
        self.line_positions = [20, 40]  # 水平分割线y坐标

    def update_data(self,dots,line_positions):
        self.line_positions = line_positions
        self.dots = dots
        self.update()

    def get_region_color(self, y):
        """根据y坐标确定区域颜色"""
        if y < self.line_positions[0]:
            return self.colors[0]
        elif y < self.line_positions[1]:
            return self.colors[1]
        else:
            return self.colors[2]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制水平分割线
        painter.setPen(QPen(Qt.gray, 1, Qt.DashLine))
        for i in range(len(self.line_positions)):
            pos = 60-self.line_positions[(len(self.line_positions)-1)-i]
            painter.drawLine(0, pos, self.width(), pos)

        # 绘制点
        r = max(1.0,float(format(20/log2(float(len(self.dots))),".2f")))
        print(r)
        for x, y in self.dots:
            painter.setBrush(self.get_region_color(y))
            painter.drawEllipse(QPoint(x, y), r, r)
