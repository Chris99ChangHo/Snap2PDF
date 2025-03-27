import pyautogui
import cv2
import pytesseract
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

# ✅ Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# cmd에서 실행시키고 캡처할 화면으로 이동하는 시간 확보
time.sleep(2)

# 크롭할 좌표 설정 (수동으로 찾은 값)
x1, y1 = 622, 152   # 왼쪽 상단
x2, y2 = 1304, 1022 # 오른쪽 하단

# 페이지 넘기기 버튼 좌표
next_page_x, next_page_y = 1872, 595

# OCR 결과 저장 리스트
ocr_texts = []

# 캡처 및 OCR 실행
image_files = []
for i in range(5):  # 5페이지 캡처
    time.sleep(1.5)  # 페이지가 완전히 로딩될 시간 확보
    
    # 화면 캡처
    screenshot = pyautogui.screenshot()
    screenshot.save(f"page_{i+1}.png")  # 전체 화면 저장
    
    # OpenCV로 크롭
    image = cv2.imread(f"page_{i+1}.png")
    cropped_page = image[y1:y2, x1:x2]
    
    # 크롭된 이미지 저장
    cropped_filename = f"cropped_page_{i+1}.png"
    cv2.imwrite(cropped_filename, cropped_page)
    image_files.append(cropped_filename)
    
    # OCR 적용
    text = pytesseract.image_to_string(Image.open(cropped_filename), lang="kor")
    ocr_texts.append(f"=== Page {i+1} ===\n{text}\n")
    
    # 다음 페이지 넘기기
    pyautogui.click(next_page_x, next_page_y)
    time.sleep(1)  # 페이지 전환 딜레이

# OCR 결과 저장 (텍스트 파일)
with open("ocr_result.txt", "w", encoding="utf-8") as f:
    f.writelines(ocr_texts)

# PDF 변환 함수
def images_to_pdf(image_list, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    for img_path in image_list:
        c.drawImage(img_path, 50, 100, width=500, height=700)  # 적절한 위치 조정
        c.showPage()
    c.save()

# PDF 저장
images_to_pdf(image_files, "output.pdf")

print("✅ 5페이지 캡처, OCR, PDF 변환 완료!")
