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

# 2. 스트리밍 주소 설정 (server, stream_key)
server_url = "rtmp://a.rtmp.youtube.com/live2"
stream_key = "INPUT YOUR STREAM KEY"

streaming_url = server_url + '/' + stream_key

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
        self.filter = False
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
        self.filter = False
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

# 6. GUI 위젯
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.virtualCam = VirtualCam()
        self.streamming = Streaming()
    
    def initUI(self):
        # [윈도우 타이틀]
        self.setWindowTitle('SECULIVE')

        # [버튼]
        # (1) 버튼 생성
        filter_btn = QPushButton('필터 적용')
        virtual_cam_btn = QPushButton('가상 카메라 시작')
        streaming_btn = QPushButton('방송 시작')
        btn = QPushButton('종료하기')

        # (2) 버튼 클릭 이벤트
        filter_btn.clicked.connect(self.filterClicked)
        virtual_cam_btn.clicked.connect(self.virtualCamClicked)
        streaming_btn.clicked.connect(self.streamClicked)
        btn.clicked.connect(QCoreApplication.instance().quit)

        # [레이아웃]
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(filter_btn)
        hbox.addWidget(virtual_cam_btn)
        hbox.addWidget(streaming_btn)
        hbox.addWidget(btn)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        # 윈도우 사이즈 및 위치
        self.resize(500, 500)
        self.center()

        self.show()

    # [버튼] 버튼 클릭 이벤트 처리 함수
    def filterClicked(self):
        btn = self.sender()
        if (btn.text() == '필터 적용'):
            btn.setText('필터 취소')
            self.virtualCam.filter_on()
            self.streamming.filter_on()
        else:
            btn.setText('필터 적용')
            self.virtualCam.filter_off()
            self.streamming.filter_off()
    
    def virtualCamClicked(self):
        btn = self.sender()
        if (btn.text() == '가상 카메라 시작'):
            btn.setText('가상 카메라 중단')
            self.virtualCam.resume()
            self.virtualCam.start()
        else:
            btn.setText('가상 카메라 시작')
            self.virtualCam.stop()
            self.virtualCam.quit()

    def streamClicked(self):
        btn = self.sender()
        if (btn.text() == '방송 시작'):
            btn.setText('방송 중단')
            self.streamming.resume()
            self.streamming.start()
        else:
            btn.setText('방송 시작')
            self.streamming.stop()
            self.streamming.quit()

    # [레이아웃] 데스크톱 정중앙에 위치
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
