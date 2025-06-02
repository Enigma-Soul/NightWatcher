from PySide6.QtWidgets import (QApplication, QWidget, QMenu, QLabel, QDialog, QLineEdit,
                               QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
                               QProgressBar, QDialogButtonBox, QFormLayout)
from PySide6.QtGui import (QPainter, QColor, QPen, QAction, QBrush,
                           QPainterPath, QFont)
from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal, QTimer
from .DotWidget import DotWidget
from .PieChart import PieChart

"""信息面板"""
class InfoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)  # 正确初始化父类
        self.high_percent = 30
        self.range_percent = 40
        self.low_percent = 30
        self.direction = "↑"
        self.main_value = 123
        self.time = "0分钟前"
        self.progress_bars = {}
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(240, 220)
        self.button_check = lambda x:x
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        # 顶部状态行
        top_row = QHBoxLayout()
        self.sgv_label =QLabel(f"<b>{self.main_value}</b> {self.direction}", styleSheet="font-size: 16px; color: white;")
        top_row.addWidget(self.sgv_label)
        top_row.addStretch()


        self.time_label = QLabel(f"{self.time}", styleSheet="font-size: 12px; color: #DDD;")
        top_row.addWidget(self.time_label)
        layout.addLayout(top_row)


        # 时间按钮
        time_buttons = QHBoxLayout()
        button_text_list = ["1h","6h", "12h", "1day"]
        for i in range(4):
            btn = QPushButton(button_text_list[i])
            btn.setFixedSize(50, 22)
            btn.setStyleSheet("""
                QPushButton {background: transparent; color: #DDD; border: none; font-size: 12px;}
                QPushButton:hover {color: white; background: rgba(255,255,255,0.1);}
            """)


            btn.clicked.connect(lambda checked, button_order=i: self.button_check(button_order))
            time_buttons.addWidget(btn)



        layout.addLayout(time_buttons)

        # 点阵图
        layout.addWidget(DotWidget())

        # 状态区域
        status_layout = QHBoxLayout()
        progress_layout = QVBoxLayout()
        colors = [ "#F2C94C", "#6DAE81","#EB5757"]

        ### High
        row = QHBoxLayout()
        self.high = QLabel(f"High: {self.high_percent}%", styleSheet="color: white; font-size: 12px;")
        row.addWidget(self.high)
        pb = QProgressBar()
        pb.setValue(self.high_percent)
        pb.setTextVisible(False)
        pb.setFixedWidth(24)
        pb.setFixedHeight(6)
        pb.setStyleSheet(f"""
                        QProgressBar {{background: rgba(255,255,255,0.2); border-radius: 3px;}}
                        QProgressBar::chunk {{background-color: {colors[0]}; border-radius: 3px;}}
                    """)
        row.addWidget(pb)
        self.progress_bars["High"] = pb
        progress_layout.addLayout(row)
        ### Range
        row = QHBoxLayout()
        self.range = QLabel(f"Range: {self.range_percent}%", styleSheet="color: white; font-size: 12px;")
        row.addWidget(self.range)
        pb = QProgressBar()
        pb.setValue(self.range_percent)
        pb.setTextVisible(False)
        pb.setFixedHeight(6)
        pb.setFixedWidth(24)
        pb.setStyleSheet(f"""
                                QProgressBar {{background: rgba(255,255,255,0.2); border-radius: 3px;}}
                                QProgressBar::chunk {{background-color: {colors[1]}; border-radius: 3px;}}
                            """)
        row.addWidget(pb)
        self.progress_bars["Range"] = pb
        progress_layout.addLayout(row)
        ### Low
        row = QHBoxLayout()
        self.low = QLabel(f"Low: {self.low_percent}%", styleSheet="color: white; font-size: 12px;")
        row.addWidget(self.low)
        pb = QProgressBar()
        pb.setValue(self.low_percent)
        pb.setTextVisible(False)
        pb.setFixedHeight(6)
        pb.setFixedWidth(24)
        pb.setStyleSheet(f"""
                                        QProgressBar {{background: rgba(255,255,255,0.2); border-radius: 3px;}}
                                        QProgressBar::chunk {{background-color: {colors[2]}; border-radius: 3px;}}
                                    """)
        row.addWidget(pb)
        self.progress_bars["Low"] = pb
        progress_layout.addLayout(row)

        # 饼图
        self.pie_chart = PieChart([30,40,30])
        status_layout.addLayout(progress_layout)
        status_layout.addWidget(self.pie_chart)
        layout.addLayout(status_layout)

        self.setLayout(layout)
        self.setStyleSheet("""
            background: rgba(50, 50, 50, 220);
            border-radius: 8px;
            border: 1px solid rgba(100, 100, 100, 0.5);
        """)

    def update_data(self,percent,value,direction,time):
        self.high_percent = percent[0]
        self.range_percent = percent[1]
        self.low_percent = percent[2]
        # 更新 High 进度条
        self.high_percent = self.high_percent
        self.progress_bars["High"].setValue(self.high_percent)
        self.high.setText(f"High: {self.high_percent}%")

        # 更新 Range 进度条
        self.range_percent = self.range_percent
        self.progress_bars["Range"].setValue(self.range_percent)
        self.range.setText(f"Range: {self.range_percent}%")

        # 更新 Low 进度条
        self.low_percent = self.low_percent
        self.progress_bars["Low"].setValue(self.low_percent)
        self.low.setText(f"Low: {self.low_percent}%")


        self.main_value = value
        self.direction = direction
        self.time = time
        self.high.setText(f"High: {self.high_percent}%")
        self.range.setText(f"Range: {self.range_percent}%")
        self.low.setText(f"Low: {self.low_percent}%")
        self.sgv_label.setText(f"{self.main_value} {self.direction}")
        self.time_label.setText(f"{self.time}")
        self.pie_chart.set_values(percent)
        self.pie_chart.update()