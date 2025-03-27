import cv2

# 이미지 로드
image = cv2.imread("image.png")

# 크롭할 좌표 (위에서 얻은 값으로 변경!)
x1, y1 = 622, 152   # 왼쪽 상단
x2, y2 = 1304, 1022 # 오른쪽 하단

# 이미지 크롭
cropped_page = image[y1:y2, x1:x2]

# 결과 저장
cv2.imwrite("cropped_page.png", cropped_page)

# 크롭된 이미지 확인
cv2.imshow("크롭된 이미지", cropped_page)
cv2.waitKey(0)
cv2.destroyAllWindows()
