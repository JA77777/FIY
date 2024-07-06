import cv2 as cv
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox, QInputDialog
from recognition import recognize_image


class AnimalPlantRecognitionApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(AnimalPlantRecognitionApp, self).__init__()
        uic.loadUi('main.ui', self)

        # 连接按钮点击事件到相应的方法
        self.selectButton.clicked.connect(self.select_recognition_type)
        self.loadVideoButton.clicked.connect(self.load_video_file)

        self.recognition_type = None

        # 设置视频显示区域的属性
        self.videoLabel.setScaledContents(True)
        self.resultLabel.setWordWrap(True)

        # 美化界面
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333;
            }
        """)

        self.video_path = None  # 视频文件路径
        self.cap = None  # 视频捕捉对象
        self.timer = QtCore.QTimer()  # 定时器用于控制视频帧显示
        self.timer.timeout.connect(self.display_video_stream)
        self.frame_skip_count = 0  # 用于控制帧跳过数量

    def select_recognition_type(self):
        """弹出对话框让用户选择识别类型（动物或植物）"""
        items = ("动物", "植物")
        item, ok = QInputDialog.getItem(self, "选择识别类型", "请选择识别类型:", items, 0, False)
        if ok and item:
            self.recognition_type = item

    def load_video_file(self):
        """弹出文件选择对话框让用户选择视频文件并开始视频播放"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "/mnt/data/", "Videos (*.mp4 *.avi *.mkv)",
                                                   options=options)
        if file_path:
            self.video_path = file_path
            self.cap = cv.VideoCapture(self.video_path)
            self.timer.start(40)  # 设置定时器间隔时间为40毫秒

    def display_video_stream(self):
        """定时器回调函数，用于显示视频帧和进行识别"""
        if self.cap.isOpened():
            ret, frame = self.cap.read()  # 读取一帧视频
            if ret:
                # 将视频帧从BGR格式转换为RGB格式
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                # 将视频帧转换为QImage格式
                image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0],
                                     QtGui.QImage.Format_RGB888)
                # 在videoLabel上显示视频帧
                self.videoLabel.setPixmap(QtGui.QPixmap.fromImage(image))

                # 每10帧进行一次识别以减少处理时间
                if self.frame_skip_count % 10 == 0:
                    result = recognize_image(frame, self.recognition_type)  # 调用识别函数进行识别
                    if result:
                        self.resultLabel.setText(result)  # 显示识别结果

                self.frame_skip_count += 1

    def closeEvent(self, event):
        """在关闭窗口时释放视频捕捉对象"""
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        super().closeEvent(event)  # 调用父类的关闭事件处理方法
