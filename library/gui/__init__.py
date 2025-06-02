from .MainPanel import *
from sys import argv



class GUI():
    def __init__(self):
        # 预定义
        self.app = QApplication(argv)
        self.app.setStyle("Fusion")
        self.panel = MainPanel()
        self.dots = [()]
        self.main_value = 0
        self.direction = ""
        self.time = ""
        self.percent = [0, 100, 0]
        self.settings = {}


    def run(self):
        self.panel.show()
        self.app.exec()
    def update_values(self,new_value):
        self.main_value = new_value
        self.panel.update_values(self.percent,self.main_value,self.direction,self.time,self.dots)
    def update_percent(self,new_percent):
        self.percent = new_percent
        self.panel.update_values(self.percent,self.main_value,self.direction,self.time,self.dots)
    def update_direction(self,new_direction):
        self.direction = new_direction
        self.panel.update_values(self.percent,self.main_value,self.direction,self.time,self.dots)
    def update_time(self,new_time):
        self.time = new_time
        self.panel.update_values(self.percent,self.main_value,self.direction,self.time,self.dots)
    def update_dots(self,new_dots):
        self.dots = new_dots
        self.panel.update_values(self.percent,self.main_value,self.direction,self.time,self.dots)
    def update_settings(self,new_settings):
        self.settings = new_settings
        self.panel.update_settings(self.settings)
    def set_button_check(self,fuction):
        # def button_check(button_order):
        #     print(button_order)
        self.panel.info_panel.button_check = fuction
    def update_all(self,new_value,new_percent,new_direction,new_time,new_dots):
        self.main_value = new_value
        self.percent = new_percent
        self.direction = new_direction
        self.time = new_time
        self.dots = new_dots
        self.panel.update_values(self.percent,self.main_value,self.direction,self.time,self.dots)
    def update_lines(self,low,high):
        self.panel.settings['low_line'] = low
        self.panel.settings['high_line'] = high
        self.panel.update_settings(self.settings)
    def set_save_setting(self,fuction):
        self.panel.save_setting = fuction
    def get_settings(self):
        return self.panel.settings
    def load_settings(self,settings):
       self.panel.settings = settings


