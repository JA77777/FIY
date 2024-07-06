import warnings
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtGui import QPixmap
from app import AnimalPlantRecognitionApp

# 忽略弃用警告
warnings.filterwarnings("ignore", category=DeprecationWarning)


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.recognition_app = None
        uic.loadUi('login.ui', self)
        self.loginButton.clicked.connect(self.login)

        # 设置背景图片
        pixmap = QPixmap('data/image.png')
        self.backgroundLabel.setPixmap(pixmap)
        self.backgroundLabel.setScaledContents(True)

    def login(self):
        self.recognition_app = AnimalPlantRecognitionApp()
        self.recognition_app.show()
        self.close()
