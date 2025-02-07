import sys

import pyperclip
from PyQt5.QtWidgets import QApplication
import controller.auto_code_controller as auto_code_controller
import gui
import re

class AppController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = "Singleton Data"
        return cls._instance

    def __init__(self):
        self.auto_code_controller_instance = auto_code_controller.instance
        self.codes = []
        self.window = None

    def init_window(self):
        app = QApplication(sys.argv)
        window = gui.MainWindow()
        window.show()
        self.window = window
        self.auto_code_controller_instance.connect_statu.valueChanged.connect(self.connect_statu_valueChanged)
        self.window.connect_action.connect(self.connect_to_ptcgl)
        self.window.get_code_action.connect(self.get_code)
        self.window.exchange_action.connect(self.exchange)
        return app

    def connect_statu_valueChanged(self):
        self.window.update_connect_label(self.auto_code_controller_instance.connect_statu)

    def connect_to_ptcgl(self):
        self.auto_code_controller_instance.connect_to_ptcgl()

    def get_code(self):
        text = pyperclip.paste()
        text = text.strip()
        if text == "":
            self.window.append_log("粘贴板为空!")
        pattern = r'[A-Z0-9]{3}-[A-Z0-9]{4}-[A-Z0-9]{3}-[A-Z0-9]{3}'
        codes = re.findall(pattern, text)
        if codes.__len__() == 0:
            self.window.append_log("粘贴板中未检测到code！")
        else:
            self.window.append_log("检测到如下code:")
            for code in codes:
                self.window.append_log(code)
        self.codes = codes

    def exchange(self):
        self.auto_code_controller_instance.exchange(self.codes)
instance = AppController()