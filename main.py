# [라이브러리]
import cv2 
import time

# PyQt5
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# obs 가상 카메라
import pyvirtualcam

# ffmpeg 명령어 실행 및 pipe 사용
import subprocess as sp

# [코드]
# 0. 내장 카메라 및 오디오 선택
camera = cv2.VideoCapture(0)
audio = "마이크 배열(Realtek(R) Audio)"

# 1. 내장 카메라 정보 저장 (fps, width, height)
fps = int(camera.get(cv2.CAP_PROP_FPS))
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 2. 스트리밍 주소
streaming_url = ""

# 3. 카툰 필터 및 fps 출력
def cartoon_filter(img):
    h, w = img.shape[:2]
    img2 = cv2.resize(img, (w//2, h//2))

    blr = cv2.bilateralFilter(img2, -1, 20, 7)
    edge = 255 - cv2.Canny(img2, 80, 120)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    dst = cv2.bitwise_and(blr, edge)
    dst = cv2.resize(dst, (w, h), interpolation=cv2.INTER_NEAREST)
                                                                  
    return dst

def print_fps_on_video(prevtime, fps, frame):
    curtime = time.time()
    sec = curtime - prevtime
    prevtime = curtime
    fps = 1/(sec)
    str = "FPS: %0.1f" % fps
    cv2.putText(frame, str, (0,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

    return prevtime, fps

# 4. 가상 카메라 스레드
class VirtualCam(QThread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.filter = True
        self.prevtime = 0
        self.fps = fps

    def resume(self):
        self.running = True

    def stop(self):
        self.running = False

    def filter_on(self):
        self.filter = True
    
    def filter_off(self):
        self.filter = False

    def run(self):
        with pyvirtualcam.Camera(width=width, height=height, fps=fps) as cam:
            while True:
                ret, frame = camera.read()
                if not ret:
                    break
                
                if self.filter:
                    frame = cartoon_filter(frame)
                
                self.prevtime, self.fps = print_fps_on_video(self.prevtime, self.fps, frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cam.send(frame)
                cam.sleep_until_next_frame()
                if self.running == False:
                    break

# 5. 방송 스레드
class Streaming(QThread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.filter = True
        self.prevtime = 0
        self.fps = fps
    
    def resume(self):
        self.running = True

    def stop(self):
        self.running = False

    def filter_on(self):
        self.filter = True
    
    def filter_off(self):
        self.filter = False
        
    def run(self):
        command = ['ffmpeg',
        '-y',
        '-re',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-pix_fmt', 'bgr24',
        '-r', '10',
        '-s', "{}x{}".format(width, height),
        '-i', '-',
        '-f', 'dshow',
        '-rtbufsize', '10M',
        '-i', f"audio={audio}",
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-c:a', 'aac',
        '-f', 'flv', 
        streaming_url]

        p = sp.Popen(command, stdin=sp.PIPE)

        while True:
            ret, frame = camera.read()
            if not ret:
                break

            if self.filter:
                    frame = cartoon_filter(frame)

            self.prevtime, self.fps = print_fps_on_video(self.prevtime, self.fps, frame)

            p.stdin.write(frame.tobytes())

            if self.running == False:
                break
        p.stdin.close()
        p.terminate()

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
        virtual_cam_btn.clicked.connect(self.openBroadClass)
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

    def openBroadClass(self):
        widget.setCurrentIndex(widget.currentIndex()+2)

    def openStreamingClass(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

class StreamingWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.streaming = Streaming()

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
        global streaming_url
        streaming_url = self.server_url.text() + "/" + self.stream_key.text()
        if (len(streaming_url) < 2):
            QMessageBox.about(self, '경고', '입력값이 없습니다.')
        else:
            widget.setCurrentIndex(widget.currentIndex()+2)

class StreamingBroadWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.streaming = Streaming()

    def initUI(self):
        # 로고 이미지 사용
        pixmap = QPixmap('res/logo.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignHCenter)

        # [기능]
        # 버튼
        self.work_btn = QPushButton('방송 시작', self)
        filter_btn = QPushButton('마스킹 제거', self)
        main_btn = QPushButton('송출 중단 후 메인화면', self)

        # 버튼 클릭
        self.work_btn.clicked.connect(self.streamClicked)
        filter_btn.clicked.connect(self.filterClicked)
        main_btn.clicked.connect(self.stopAndOpenMainClass)

        # [디자인]
        # 레이아웃
        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addWidget(logo)
        vbox.addStretch(1)
        vbox.addWidget(self.work_btn)
        vbox.addWidget(filter_btn)
        vbox.addWidget(main_btn)
        vbox.addStretch(3)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    # [버튼] 버튼 클릭 이벤트 처리 함수
    def filterClicked(self):
        btn = self.sender()
        if (btn.text() == '마스킹 적용'):
            btn.setText('마스킹 제거')
            self.streaming.filter_on()
        else:
            btn.setText('마스킹 적용')
            self.streaming.filter_off()

    def streamClicked(self):
        btn = self.sender()
        if (btn.text() == '방송 시작'):
            btn.setText('방송 중단')
            self.streaming.resume()
            self.streaming.start()
        else:
            btn.setText('방송 시작')
            self.streaming.stop()
            self.streaming.quit()

    def stopAndOpenMainClass(self):
        if  (self.work_btn.text() == '방송 중단'):
            self.streaming.stop()
            self.streaming.quit()
        widget.setCurrentIndex(widget.currentIndex()-4)

class VirtualCamBroadWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.virtualCam = VirtualCam()

    def initUI(self):
        # 로고 이미지 사용
        pixmap = QPixmap('res/logo.png')
        logo = QLabel()
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignHCenter)

        # [기능]
        # 버튼
        self.work_btn = QPushButton('가상 카메라 시작', self)
        filter_btn = QPushButton('마스킹 제거', self)
        main_btn = QPushButton('송출 중단 후 메인화면', self)

        # 버튼 클릭
        self.work_btn.clicked.connect(self.streamClicked)
        filter_btn.clicked.connect(self.filterClicked)
        main_btn.clicked.connect(self.stopAndOpenMainClass)

        # [디자인]
        # 레이아웃
        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addWidget(logo)
        vbox.addStretch(1)
        vbox.addWidget(self.work_btn)
        vbox.addWidget(filter_btn)
        vbox.addWidget(main_btn)
        vbox.addStretch(3)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    # [버튼] 버튼 클릭 이벤트 처리 함수
    def filterClicked(self):
        btn = self.sender()
        if (btn.text() == '마스킹 적용'):
            btn.setText('마스킹 제거')
            self.virtualCam.filter_on()
        else:
            btn.setText('마스킹 적용')
            self.virtualCam.filter_off()

    def streamClicked(self):
        btn = self.sender()
        if (btn.text() == '가상 카메라 시작'):
            btn.setText('가상 카메라 중단')
            self.virtualCam.resume()
            self.virtualCam.start()
        else:
            btn.setText('가상 카메라 시작')
            self.virtualCam.stop()
            self.virtualCam.quit()

    def stopAndOpenMainClass(self):
        if  (self.work_btn.text() == '가상 카메라 중단'):
            self.virtualCam.stop()
            self.virtualCam.quit()
        widget.setCurrentIndex(widget.currentIndex()-3)

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
    virtualCamBroadWindow = VirtualCamBroadWindow()
    streamingBroadWindow = StreamingBroadWindow()

    widget.addWidget(mainWindow)
    widget.addWidget(transmissionWindow)
    widget.addWidget(streamingWindow)
    widget.addWidget(virtualCamBroadWindow)
    widget.addWidget(streamingBroadWindow)


    # [트레이 아이콘]
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QIcon('res/live.png'))

    show_action = QAction("Show")
    hide_action = QAction("Hide")
    quit_action = QAction("Exit")

    show_action.triggered.connect(widget.show)
    hide_action.triggered.connect(widget.hide)
    quit_action.triggered.connect(qApp.quit)
    
    tray_menu = QMenu()
    tray_menu.addAction(show_action)
    tray_menu.addAction(hide_action)
    tray_menu.addAction(quit_action)
    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()
    

    # [윈도우 정보]
    widget.resize(640, 480)
    center(widget)
    widget.show()

    sys.exit(app.exec_())
