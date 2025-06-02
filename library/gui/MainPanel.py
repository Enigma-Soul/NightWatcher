from PySide6.QtWidgets import (QApplication, QWidget, QMenu, QLabel, QDialog, QLineEdit,
                               QVBoxLayout, QHBoxLayout, QPushButton, QComboBox,
                               QProgressBar, QDialogButtonBox, QFormLayout)
from PySide6.QtGui import (QPainter, QColor, QPen, QAction, QBrush,
                           QPainterPath, QFont)
from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal, QTimer
from .InfoPanel import InfoPanel
from .SettingsDialog import SettingsDialog
from .DotWidget import DotWidget



"""主面板"""
class MainPanel(QWidget):
    def __init__(self):
        super().__init__()  # 关键父类初始化

        # 窗口设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(120, 60)

        # 初始化数据
        self.main_value = 256
        self.direction = "↑"
        self.settings = {'low_line': 72, 'high_line': 180, 'color_scheme': 0}

        # 创建菜单
        self.menu = self.create_menu()

        # 信息面板
        self.info_panel = InfoPanel(self)
        self.info_panel.hide()

        # 主标签
        self.label = QLabel(f"{self.main_value} {self.direction}", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 20))
        self.label.setGeometry(0, 0, 120, 60)
        self.label.setStyleSheet("color: white;")

        self.save_setting = lambda :1

        # 事件变量
        self.drag_position = None
        self.press_pos = None

    def create_menu(self):
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background: rgba(50, 50, 50, 220);
                border: 1px solid #444;
                color: white;
            }
            QMenu::item {
                padding: 5px 25px;
            }
            QMenu::item:selected {
                background: rgba(80, 80, 80, 200);
            }
        """)
        menu.addAction("设置", self.show_settings)
        menu.addAction("退出", self.close)
        return menu

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            self.press_pos = event.position().toPoint()
        elif event.button() == Qt.RightButton:
            self.menu.exec(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if self.drag_position and event.buttons() & Qt.LeftButton:
            self.info_panel.show()
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
            self.drag_position = event.globalPosition().toPoint()
            self.update_panel_position()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            moved = event.position().toPoint() - self.press_pos
            if moved.manhattanLength() < QApplication.startDragDistance():
                self.toggle_info_panel()
            self.drag_position = None
            self.press_pos = None

    def toggle_info_panel(self):
        if self.info_panel.isVisible():
            self.info_panel.hide()
        else:
            self.info_panel.show()
            self.update_panel_position()

    def update_panel_position(self):
        self.info_panel.move(
            self.x() + (self.width() - self.info_panel.width()) // 2,
            self.y() + self.height() + 5
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(self.rect(), 5, 5)
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.setBrush(QBrush(QColor(40, 40, 40, 220)))
        painter.drawPath(path)

    def show_settings(self):
        dialog = SettingsDialog(self.settings, self)
        dialog.settings_updated.connect(self.update_settings)
        dialog.exec()

    def update_settings(self, new_settings):
        self.settings.update(new_settings)
        color_schemes = [
            [QColor(100, 150, 250), QColor(250, 150, 100), QColor(150, 250, 100)],
            [QColor(255, 0, 0), QColor(255, 255, 0), QColor(160, 32, 240)],
            [QColor(0, 255, 255), QColor(255, 192, 203), QColor(128, 128, 128)]
        ]

        dot_widget = self.info_panel.findChild(DotWidget)
        if dot_widget:
            height_unit = 60 / self.settings["max"]
            dot_widget.line_positions = sorted([self.settings['low_line']*height_unit, self.settings['high_line']*height_unit])
            dot_widget.colors = color_schemes[self.settings['color_scheme']]
            dot_widget.update()
        self.save_setting()



    def update_values(self,percent,main_value,direction,time,dots):
        self.info_panel.update_data(percent,main_value,direction,time)
        height_unit = 60 / self.settings["max"]
        dot_widget = self.info_panel.findChild(DotWidget)
        dot_widget.update_data(dots, sorted([self.settings['low_line']*height_unit, self.settings['high_line']*height_unit]))
        self.main_value = main_value
        self.direction = direction
        self.label.setText(f"{self.main_value} {self.direction}")





