from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QLabel, QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, \
    QSizePolicy, QAction

from gui.property import ConnectStatu


class MainWindow(QMainWindow):
    connect_action = pyqtSignal()
    get_code_action = pyqtSignal()
    exchange_action = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("Auto Controller")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        v_layout = QVBoxLayout(central_widget)

        window_width = 500
        window_height = 600
        # 创建一个 QLabel 用来显示图片
        self.ImageLabel = QLabel(self)
        self.ImageLabel.setPixmap(self._get_head_scaled_width_image(window_width))
        v_layout.addWidget(self.ImageLabel, alignment=Qt.AlignTop)
        v_layout.setStretchFactor(self.ImageLabel, 3)

        self.Label = QLabel(self)
        self.Label.setText("未连接")
        v_layout.addWidget(self.Label, alignment=Qt.AlignTop)
        v_layout.setStretchFactor(self.Label, 1)

        self.log_display = QPlainTextEdit(self)
        self.log_display.setReadOnly(True)  # 设置为只读，避免用户编辑
        self.log_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        v_layout.addWidget(self.log_display)
        v_layout.setStretchFactor(self.log_display, 6)

        self.botton_h_layout = QHBoxLayout()

        self.connect_button = QPushButton("连接PTCGL", self)
        self.connect_button.clicked.connect(self.connect_to_ptcgl)
        self.botton_h_layout.addWidget(self.connect_button, alignment=Qt.AlignTop)

        self.get_code_button = QPushButton("获取粘贴板code", self)
        self.get_code_button.clicked.connect(self.get_code)
        self.botton_h_layout.addWidget(self.get_code_button, alignment=Qt.AlignTop)

        self.exchange_button = QPushButton("开始兑换", self)
        self.exchange_button.clicked.connect(self.exchange)
        self.botton_h_layout.addWidget(self.exchange_button, alignment=Qt.AlignTop)

        button_widget = QWidget(self)
        button_widget.setLayout(self.botton_h_layout)

        v_layout.addWidget(button_widget, alignment=Qt.AlignBottom)
        v_layout.setStretchFactor(button_widget, 1)

        self.setFixedSize(window_width, window_height)

    def _get_head_scaled_width_image(self, width):
        background_pixmap = QPixmap("assets/background.jpg")
        icon_pixmap = QPixmap("assets/logo.png")

        # 创建一个新的QPixmap，大小为背景图的大小
        result_pixmap = background_pixmap.copy()  # 复制一份背景图，用于绘制图标

        # 创建QPainter对象
        painter = QPainter(result_pixmap)

        # 图标居中绘制位置
        icon_pos = (result_pixmap.width() - icon_pixmap.width()) // 2, (
                    result_pixmap.height() - icon_pixmap.height()) // 2
        painter.drawPixmap(icon_pos[0], icon_pos[1], icon_pixmap)
        painter.end()

        # 缩放图片到目标宽度
        scaled_pixmap = result_pixmap.scaledToWidth(width, Qt.SmoothTransformation)

        return scaled_pixmap

    def connect_to_ptcgl(self):
        self.connect_button.setDisabled(True)
        self.log_display.appendPlainText("连接中......")
        self.connect_action.emit()

    def get_code(self):
        self.get_code_action.emit()

    def exchange(self):
        self.exchange_action.emit()

    def update_connect_label(self, connect_statu: ConnectStatu):
        if connect_statu.value == 0:
            self.Label.setText("未连接")
            self.append_log("连接失败")
        elif connect_statu.value == 1:
            self.Label.setText("已连接")
            self.append_log("连接成功")
        else:
            self.Label.setText("请重试")
            self.append_log("错误，请重试")
        self.connect_button.setDisabled(False)

    def append_log(self, log_message):
        self.log_display.appendPlainText(log_message)