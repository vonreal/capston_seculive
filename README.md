# capston_seculive
2021 - 2022 캡스톤 프로젝트입니다. 가상 카메라 연동 및 유튜브 실시간 방송 구현을 맡았습니다.<br>
내장 카메라와 마이크를 선택(변수에 대입)하면 해당 카메라에서 영상을 가져와 원하는 방식(obs 가상 카메라, Youtube streamming: stream url 설정 필요)으로 실시간 송출해줍니다.
사용을 위해서는 ffmpeg와 obs가 미리 설치되어 있어야합니다. <br>
obs 가상 카메라는 Zoom 등의 화상 회의 플랫폼에서 선택 가능하니 영상에 어떠한 처리(이번 Capston에서는 본인 이외의 모자이크가 목적)를 진행하면 처리가 진행된 영상이 송출됩니다.

# 진행 상태(개발 일지)
<a href=https://potent-justice-4a9.notion.site/PyQt5-ON-OFF-615bb4137e8c417996f8abb1a99add91>2022-02-11<br>
<a href=https://potent-justice-4a9.notion.site/5fc2c0f9794a4a6387b5f099dbc5ca4a>2022-02-12<br>
<a href=https://potent-justice-4a9.notion.site/GUI-80-914dbf10b13947ddabf2ce61f55baef9>2022-02-13<br>
<a href=https://potent-justice-4a9.notion.site/GUI-95-2726c85bdcad4d1a8af71978ef55f774>2022-02-17<br>

# 의존성
<a href=https://ffmpeg.org/download.html>ffmpeg<br>
<a href=https://obsproject.com/ko>obs-virtual-camera<br>

# 의존 라이브러리
opencv<br>
```
  pip install opencv-python
```
pyvirtualcam<br>
```
  pip install pyvirtualcam
```
PyQt5<br>
```
  pip install PyQt5
```
