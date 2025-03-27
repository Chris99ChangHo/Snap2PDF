import cv2

# 이미지 로드
image = cv2.imread("image.png")

# 이미지 크기 조정 (너무 크면 축소)
scale = 0.5  # 필요하면 0.3, 0.4 등으로 조정 가능
resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

# 마우스 클릭 이벤트 함수
def get_mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 클릭하면 좌표 출력
        original_x = int(x / scale)  # 원본 좌표로 변환
        original_y = int(y / scale)
        print(f"클릭한 좌표: x={original_x}, y={original_y}")

# 창에 이미지 표시
cv2.imshow("좌표 확인용 이미지", resized_image)
cv2.setMouseCallback("좌표 확인용 이미지", get_mouse_click)

cv2.waitKey(0)
cv2.destroyAllWindows()

# 노트북 모니터
# 클릭한 좌표: x=622, y=152
# 클릭한 좌표: x=1304, y=1022



