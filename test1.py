import pyautogui
import cv2
import numpy as np
import time

# 화면 캡처 및 저장
print("📸 화면을 캡처합니다. 3초 후에 캡처되니 원하는 화면을 띄워주세요!")
time.sleep(3)
screenshot = pyautogui.screenshot()
screenshot.save("captured_screen.png")  # 현재 화면 캡처 저장

# OpenCV로 이미지 로드
image = cv2.imread("captured_screen.png")

# 화면 크기 조정 (너무 크면 축소)
scale = 1  # 필요하면 조정 가능
resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

# 마우스 클릭 이벤트 함수
def get_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 클릭하면 좌표 출력
        original_x = int(x / scale)  # 원본 좌표로 변환
        original_y = int(y / scale)
        print(f"🖱️ 클릭한 좌표: x={original_x}, y={original_y}")

# 창에 이미지 표시
cv2.imshow("📍 좌표 확인용 캡처 이미지", resized_image)
cv2.setMouseCallback("📍 좌표 확인용 캡처 이미지", get_mouse_click)

cv2.waitKey(0)
cv2.destroyAllWindows()

print("✅ 좌표 확인이 끝났으면, 위 좌표 값을 코드에 반영하세요!")

# 피벗 모니터
# 클릭한 좌표: x=71, y=394
# 클릭한 좌표: x=1009, y=1600