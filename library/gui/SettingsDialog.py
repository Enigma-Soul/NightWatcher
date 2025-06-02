from PySide6.QtWidgets import (QApplication, QWidget, QMenu, QLabel, QDialog, QLineEdit,
                               QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
                               QProgressBar, QDialogButtonBox, QFormLayout,QApplication, QMessageBox)
from PySide6.QtGui import (QPainter, QColor, QPen, QAction, QBrush,
                           QPainterPath, QFont)
from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal, QTimer
from sys import exit
"""设置对话框"""
class SettingsDialog(QDialog):
    settings_updated = Signal(dict)

    def __init__(self, initial_settings, parent=None):
        super().__init__(parent)  # 正确初始化父类
        self.setWindowTitle("设置")
        self.setFixedSize(400, 300)

        # 初始化控件

        self._flag_18 = False
        if initial_settings["unit"]==0:
            self.low_line_edit = QLineEdit(str(initial_settings['low_line']))
            self.high_line_edit = QLineEdit(str(initial_settings['high_line']))
            self.max_edit = QLineEdit(str(initial_settings['max']))
        else:
            self._flag_18 = True
            self.low_line_edit = QLineEdit(str(format(initial_settings['low_line']/18,".1f")))
            self.high_line_edit = QLineEdit(str(format(initial_settings['high_line']/18,".1f")))
            self.max_edit = QLineEdit(str(format(initial_settings['max']/18,".1f")))
        self.color_combo = QComboBox()
        self.color_combo.addItems(["默认蓝-橙-绿", "红-黄-紫", "青-粉-灰"])
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["mmol/L", "mg/dL"])
        self.unit_combo.setCurrentIndex(0 if initial_settings["unit"]==0 else 1)
        self.url_edit = QLineEdit(str(initial_settings['NS-url']))


        # 底部按钮
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.apply_settings)
        self.button_box.rejected.connect(self.reject)

        self.old_settings = initial_settings
        self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout()

        # 表单布局
        form_layout = QFormLayout()
        form_layout.addRow("低警报线:", self.low_line_edit)
        form_layout.addRow("高警报线:", self.high_line_edit)
        form_layout.addRow("框内最大值:", self.max_edit)
        form_layout.addRow("颜色方案:", self.color_combo)
        form_layout.addRow("血糖单位:", self.unit_combo)
        form_layout.addRow("NightScout地址", self.url_edit)

        # 组合布局
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def apply_settings(self):
        global config
        """应用设置"""
        new_settings = {}
        try:
            new_settings = {
                'low_line': min(max(float(self.low_line_edit.text()), 0), 60),
                'high_line': min(max(float(self.high_line_edit.text()), 0), 60),
                'color_scheme': self.color_combo.currentIndex(),
                'unit': self.unit_combo.currentIndex(),
                'max': min(max(float(self.max_edit.text()), 0), 30),
                'NS-url': self.url_edit.text()
            }
            if self._flag_18:
                new_settings['low_line'] = new_settings['low_line']*18
                new_settings['high_line'] = new_settings['high_line']*18
                new_settings['max'] = new_settings['max']*18
        except ValueError:
            print("请输入有效的数字")


        self.settings_updated.emit(new_settings)
        self.accept()
