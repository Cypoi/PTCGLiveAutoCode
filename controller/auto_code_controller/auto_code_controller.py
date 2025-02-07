import math
from gc import callbacks
from time import sleep

import pywinauto
import threading
from gui.property import ConnectStatu


class AutoCodeController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.value = "Singleton Data"
        return cls._instance

    def __init__(self):
        self.app = pywinauto.Application(backend="uia")
        self.connect_statu = ConnectStatu()

    def connect_to_ptcgl(self):
        def connect():
            try:
                self.app.connect(path="Pokemon TCG Live.exe")
                self.connect_statu.value = 1
                print("连接成功")
            except:
                self.connect_statu.value = 0
                print("连接失败")

        # 启动一个子线程来执行连接操作
        connection_thread = threading.Thread(target=connect)
        connection_thread.start()

    def exchange(self, codes):
        for window in self.app.windows():
            print(window.window_text())
        window = self.app.windows()[0]
        rect = window.rectangle()
        print(f"窗口位置和大小: {rect}")

        width = rect.width()
        height = rect.height()

        x_ratio = 0.146
        y_ratio = 0.125

        click_x = rect.left + x_ratio * width
        click_y = rect.top + y_ratio * height

        print(f"点击位置: ({click_x}, {click_y})")
        window.click_input(coords=(math.ceil(click_x), math.ceil(click_y)))

        sleep(2)

        click_x1 = rect.left + 131
        click_y1 = rect.top - 10
        window.click_input(coords=(click_x1, click_y1))

        sleep(2)

        window.type_keys("Hello, pywinauto!")

instance = AutoCodeController()