import pyautogui
import cv2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

# 간단한 업스케일링 함수
def upscale_image(image_path, save_path=None, scale=2.0):
    # OpenCV로 이미지 로드
    img = cv2.imread(image_path)
    
    # 고품질 업스케일링만 적용 (INTER_CUBIC 알고리즘)
    upscaled = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    # 저장할 경로가 제공되면 저장
    if save_path:
        cv2.imwrite(save_path, upscaled, [cv2.IMWRITE_PNG_COMPRESSION, 0])  # 최고 품질로 저장
    
    return upscaled

# 메인 프로그램 시작
print("2초 후 캡처를 시작합니다. 캡처할 화면으로 이동하세요...")
time.sleep(2)

# 크롭할 좌표 설정 (수동으로 찾은 값)
x1, y1 = 71, 394   # 왼쪽 상단
x2, y2 = 1009, 1600 # 오른쪽 하단

# 페이지 넘기기 버튼 좌표
next_page_x, next_page_y = 1047, 1236

# 마우스를 이동할 빈 공간 (URL 툴팁 방지)
empty_x, empty_y = 100, 100  # 예: 화면 상단 좌측

# 캡처 실행
original_images = []
upscaled_images = []

for i in range(5):  # 5페이지 캡처
    page_num = i + 1
    print(f"페이지 {page_num} 처리 중...")

    # 첫 페이지는 넘기지 않고 바로 캡처
    if i > 0:  # 첫 페이지가 아닐 경우에만 페이지 넘기기
        # 페이지 넘기기 버튼 클릭
        pyautogui.click(next_page_x, next_page_y)
        time.sleep(0.5)  # 클릭 후 반응 시간
    
    # 마우스를 빈 공간으로 이동해서 URL 툴팁 숨기기
    pyautogui.moveTo(empty_x, empty_y)
    time.sleep(0.5)  # 이동 후 잠시 대기

    time.sleep(1.5)  # 페이지가 완전히 로딩될 시간 확보
    
    # 화면 캡처
    screenshot = pyautogui.screenshot()
    screenshot.save(f"page_{page_num}.png")  # 전체 화면 저장
    
    # OpenCV로 크롭
    image = cv2.imread(f"page_{page_num}.png")
    cropped_page = image[y1:y2, x1:x2]
    
    # 크롭된 이미지 저장
    cropped_filename = f"cropped_page_{page_num}.png"
    cv2.imwrite(cropped_filename, cropped_page)
    original_images.append(cropped_filename)
    
    # 업스케일링만 적용
    upscaled_filename = f"upscaled_page_{page_num}.png"
    upscale_image(cropped_filename, upscaled_filename, scale=2.0)
    upscaled_images.append(upscaled_filename)

# PDF 변환 함수 - 고품질 설정
def images_to_pdf(image_list, output_pdf, width=500, height=700):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    for img_path in image_list:
        # 종횡비 유지하며 이미지 삽입
        c.drawImage(img_path, 50, 50, width=width, height=height, preserveAspectRatio=True)
        c.showPage()
    c.save()

# 원본과 업스케일링 PDF 저장
images_to_pdf(original_images, "output_original.pdf")
images_to_pdf(upscaled_images, "output_upscaled.pdf", width=520, height=720)

print("✅ 5페이지 캡처, 업스케일링, PDF 변환 완료!")
print("생성된 파일:")
print("1. output_original.pdf - 원본 이미지")
print("2. output_upscaled.pdf - 업스케일링된 이미지")

# 피벗 모니터 마우스 좌표
# Point(x=1047, y=998)

# 피벗 모니터 크롭 좌표
# 클릭한 좌표: x=71, y=394
# 클릭한 좌표: x=1009, y=1600