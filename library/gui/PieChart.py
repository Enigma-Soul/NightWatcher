from PySide6.QtWidgets import (QApplication, QWidget, QMenu, QLabel, QDialog, QLineEdit,
                               QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
                               QProgressBar, QDialogButtonBox, QFormLayout)
from PySide6.QtGui import (QPainter, QColor, QPen, QAction, QBrush,
                           QPainterPath, QFont)
from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal, QTimer

"""饼图组件"""
class PieChart(QWidget):
    def __init__(self, values):
        super().__init__()  # 正确初始化父类
        self.values = values
        self.setFixedSize(80, 80)

    def set_values(self, values):
        self.values = values
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        colors = [ QColor(242, 201, 76), QColor(106, 174, 129),QColor(235, 87, 87)]
        rect = QRect(10, 10, 60, 60)
        start_angle = 0
        for i, value in enumerate(self.values):
            painter.setBrush(colors[i])
            span_angle = int(value * 360 * 16 / 100)
            painter.drawPie(rect, start_angle, span_angle)
            start_angle += span_angle