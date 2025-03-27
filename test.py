import pyautogui
import time

time.sleep(5)  # 5초 동안 마우스를 원하는 위치로 이동
print(pyautogui.position())  # 현재 노트북 마우스 좌표 출력 --> Point(x=1872, y=595)

# 피벗 모니터 마우스 좌표 --> Point(x=1047, y=998)