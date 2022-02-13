import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

streaming_url = ""

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 로고 이미지 사용
        pixmap = QPixmap('res/logo.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignHCenter)

        # [기능]
        # 버튼
        learn_data_add_btn = QPushButton('학습 데이터 추가', self)
        transmission_btn = QPushButton('영상 출력 설정', self)

        # 버튼 클릭
        transmission_btn.clicked.connect(self.openTransmissionClass)

        # [디자인]
        # 레이아웃
        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addWidget(logo)
        vbox.addStretch(1)
        vbox.addWidget(learn_data_add_btn)
        vbox.addWidget(transmission_btn)
        vbox.addStretch(3)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def openTransmissionClass(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class TransmissionWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 로고 이미지 사용
        pixmap = QPixmap('res/logo.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignHCenter)


        # [기능]
        # 버튼
        streaming_btn = QPushButton('스트리밍', self)
        virtual_cam_btn = QPushButton('가상 카메라', self)
        before_btn = QPushButton('뒤로가기', self)

        # 버튼 클릭
        streaming_btn.clicked.connect(self.openStreamingClass)
        before_btn.clicked.connect(self.openMainClass)

        # [디자인]
        # 레이아웃
        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addWidget(logo)
        vbox.addStretch(1)
        vbox.addWidget(streaming_btn)
        vbox.addWidget(virtual_cam_btn)
        vbox.addWidget(before_btn)
        vbox.addStretch(3)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def openMainClass(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def openStreamingClass(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class StreamingWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 로고 이미지 사용
        pixmap = QPixmap('res/logo.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignHCenter)

        # [기능]
        # 버튼
        server_label = QLabel("서버 주소")
        self.server_url = QLineEdit()
        key_label = QLabel("스트림 키")
        self.stream_key = QLineEdit()
        self.stream_key.setEchoMode(3)
        before_btn = QPushButton('뒤로가기', self)
        input_btn = QPushButton('확인', self)

        # 버튼 클릭
        before_btn.clicked.connect(self.openMainClass)
        input_btn.clicked.connect(self.getURL)

        # [디자인]
        # 레이아웃
        server_input_hbox = QHBoxLayout()
        server_input_hbox.addWidget(server_label)
        server_input_hbox.addWidget(self.server_url)

        key_input_hbox = QHBoxLayout()
        key_input_hbox.addWidget(key_label)
        key_input_hbox.addWidget(self.stream_key)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(before_btn)
        btn_hbox.addWidget(input_btn)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addWidget(logo)
        vbox.addStretch(1)
        vbox.addLayout(server_input_hbox)
        vbox.addLayout(key_input_hbox)
        vbox.addStretch(1)
        vbox.addLayout(btn_hbox)
        vbox.addStretch(2)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def openMainClass(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def getURL(self):
        streaming_url = self.server_url.text() + "/" + self.stream_key.text()
        widget.setCurrentIndex(widget.currentIndex()+1)

class BroadWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 로고 이미지 사용
        pixmap = QPixmap('res/logo.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignHCenter)

        # [기능]
        # 버튼
        streaming_btn = QPushButton('마스킹 중지', self)
        virtual_cam_btn = QPushButton('방송 중단', self)
        before_btn = QPushButton('메인화면', self)

        # 버튼 클릭
        streaming_btn.clicked.connect(self.openStreamingClass)
        before_btn.clicked.connect(self.openMainClass)

        # [디자인]
        # 레이아웃
        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addWidget(logo)
        vbox.addStretch(1)
        vbox.addWidget(streaming_btn)
        vbox.addWidget(virtual_cam_btn)
        vbox.addWidget(before_btn)
        vbox.addStretch(3)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def openMainClass(self):
        widget.setCurrentIndex(widget.currentIndex()-3)

    def openStreamingClass(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

if __name__ == '__main__':
    def center(widget):
        qr = widget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        widget.move(qr.topLeft())

    app = QApplication(sys.argv)
    
    widget = QStackedWidget()

    # [디자인]
    # 창 제목 및 아이콘 적용
    widget.setWindowTitle('SecuLive')
    widget.setWindowIcon(QIcon('res/live.png'))
    
    # 로고 이미지 사용
    pixmap = QPixmap('res/logo.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(Qt.AlignHCenter)

    # 폰트 설정
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('res/SCDream5.otf')
    app.setFont(QFont('에스코어 드림 5 Medium'))
    
    
    mainWindow = MainWindow()
    transmissionWindow = TransmissionWindow()
    streamingWindow = StreamingWindow()
    broadWindow = BroadWindow()

    widget.addWidget(mainWindow)
    widget.addWidget(transmissionWindow)
    widget.addWidget(streamingWindow)
    widget.addWidget(broadWindow)
    

    # [윈도우 정보]
    widget.resize(640, 480)
    center(widget)
    widget.show()

    sys.exit(app.exec_())