import pyautogui
import cv2
import pytesseract
import numpy as np
from PIL import Image, ImageEnhance
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

# Tesseract 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 이미지 전처리 함수 - 작은 글씨 최적화
def enhance_image_for_small_text(image_path, save_path=None):
    # OpenCV로 이미지 로드
    img = cv2.imread(image_path)
    
    # 1. 업스케일링 (작은 글씨를 위해 중요)
    scale_factor = 2.0
    img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    
    # 2. 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 3. 가우시안 블러로 미세한 노이즈 제거 (작은 값 사용)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    
    # 4. 언샤프 마스킹(Unsharp Masking)을 통한 선명도 향상
    # 블러된 이미지를 원본에서 빼서 엣지를 찾고, 이를 다시 원본에 더함
    unsharp_mask = cv2.addWeighted(gray, 1.5, blur, -0.5, 0)
    
    # 5. 적응형 이진화 - 로컬 영역에 맞게 임계값 조정
    # 작은 글씨에 최적화된 파라미터
    binary = cv2.adaptiveThreshold(
        unsharp_mask, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11,  # 블록 크기
        2    # 상수 C 값
    )
    
    # 6. 모폴로지 연산 - 텍스트 강화
    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    # 7. 작은 글씨를 위한 색상 개선 (원본에 적용)
    enhanced_color = img.copy()
    # 컬러 채널 분리 및 개선
    b, g, r = cv2.split(enhanced_color)
    # 각 채널 대비 강화
    for channel in [b, g, r]:
        cv2.normalize(channel, channel, 0, 255, cv2.NORM_MINMAX)
    # 채널 병합
    enhanced_color = cv2.merge([b, g, r])
    
    # 8. 원본 컬러 이미지에 선명도 적용
    lab = cv2.cvtColor(enhanced_color, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # L 채널에만 CLAHE 적용 (작은 글씨의 디테일 강화)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    # 채널 합치기
    enhanced_lab = cv2.merge([cl, a, b])
    enhanced_color = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # 저장할 경로가 제공되면 저장
    if save_path:
        cv2.imwrite(save_path, enhanced_color)
    
    # 흑백 버전과 컬러 버전 둘 다 반환 (OCR과 PDF용)
    return binary, enhanced_color

# 메인 프로그램 시작
print("2초 후 캡처를 시작합니다. 캡처할 화면으로 이동하세요...")
time.sleep(2)

# 크롭할 좌표 설정 (수동으로 찾은 값)
x1, y1 = 622, 152   # 왼쪽 상단
x2, y2 = 1304, 1022 # 오른쪽 하단

# 페이지 넘기기 버튼 좌표
next_page_x, next_page_y = 1872, 595

# 마우스를 이동할 빈 공간 (URL 툴팁 방지)
empty_x, empty_y = 100, 100  # 예: 화면 상단 좌측

# OCR 결과 저장 리스트
ocr_texts = []

# 캡처 및 OCR 실행
image_files = []
enhanced_image_files = []
binary_image_files = []

# 캡쳐 전 화면 확대 옵션
# 페이지를 먼저 확대할 수 있으면 아래 코드 활성화 (Ctrl + '+' 누르기)
# pyautogui.hotkey('ctrl', '+')
# pyautogui.hotkey('ctrl', '+')
# time.sleep(1)

for i in range(5):  # 5페이지 캡처
    page_num = i + 1
    print(f"페이지 {page_num} 처리 중...")
    time.sleep(1.5)  # 페이지가 완전히 로딩될 시간 확보
    
    # 페이지 넘기기 버튼 클릭
    pyautogui.click(next_page_x, next_page_y)
    time.sleep(0.5)  # 클릭 후 반응 시간
    
    # 마우스를 빈 공간으로 이동해서 URL 툴팁 숨기기
    pyautogui.moveTo(empty_x, empty_y)
    time.sleep(0.5)  # 이동 후 잠시 대기
    
    # 화면 캡처
    screenshot = pyautogui.screenshot()
    screenshot.save(f"page_{page_num}.png")  # 전체 화면 저장
    
    # OpenCV로 크롭
    image = cv2.imread(f"page_{page_num}.png")
    cropped_page = image[y1:y2, x1:x2]
    
    # 크롭된 이미지 저장
    cropped_filename = f"cropped_page_{page_num}.png"
    cv2.imwrite(cropped_filename, cropped_page)
    
    # 화질 개선 적용 - 작은 글씨 최적화
    enhanced_filename = f"enhanced_page_{page_num}.png"
    binary_filename = f"binary_page_{page_num}.png"
    
    binary_image, enhanced_image = enhance_image_for_small_text(cropped_filename)
    cv2.imwrite(enhanced_filename, enhanced_image)
    cv2.imwrite(binary_filename, binary_image)
    
    image_files.append(cropped_filename)
    enhanced_image_files.append(enhanced_filename)
    binary_image_files.append(binary_filename)
    
    # OCR 적용 (이진화된 이미지 사용 - 작은 글씨 인식에 더 효과적)
    # PIL 이미지로 변환
    binary_pil = Image.fromarray(binary_image)
    text = pytesseract.image_to_string(binary_pil, lang="kor", config='--psm 6')
    ocr_texts.append(f"=== Page {page_num} ===\n{text}\n")

# OCR 결과 저장 (텍스트 파일)
with open("ocr_result.txt", "w", encoding="utf-8") as f:
    f.writelines(ocr_texts)

# PDF 변환 함수 - DPI 및 품질 개선
def images_to_pdf(image_list, output_pdf, dpi=300, width=500, height=700):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    for img_path in image_list:
        # 종횡비 유지하며 이미지 삽입
        c.drawImage(img_path, 50, 50, width=width, height=height, preserveAspectRatio=True)
        c.showPage()
    c.save()

# 세 가지 버전의 PDF 저장
images_to_pdf(image_files, "output_original.pdf")
images_to_pdf(enhanced_image_files, "output_enhanced_color.pdf", width=520, height=720)
images_to_pdf(binary_image_files, "output_enhanced_binary.pdf", width=520, height=720)

print("✅ 5페이지 캡처, 화질 개선, OCR, PDF 변환 완료!")
print("다음 파일이 생성되었습니다:")
print("1. output_original.pdf - 원본 이미지")
print("2. output_enhanced_color.pdf - 컬러 개선 버전 (시각적 검토용)")
print("3. output_enhanced_binary.pdf - 이진화 버전 (작은 글씨 가독성 최적화)")