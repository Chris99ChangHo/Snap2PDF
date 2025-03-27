import os
import pyautogui
import cv2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

def create_folders():
    folders = ["original", "crop", "upscale", "pdf"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def upscale_image(image_path, save_path=None, scale=2.0):
    img = cv2.imread(image_path)
    upscaled = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    if save_path:
        cv2.imwrite(save_path, upscaled, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    return upscaled

def images_to_pdf(image_list, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=letter)
    for img_path in image_list:
        c.drawImage(img_path, 50, 50, width=500, height=700, preserveAspectRatio=True)
        c.showPage()
    c.save()

def check_missing_upscaled():
    missing_pages = []
    for i in range(1, 642):
        filename = f"upscale/upscaled_page_{i}.png"
        if not os.path.exists(filename):
            missing_pages.append(i)
    if missing_pages:
        print("❌ 누락된 페이지:", missing_pages)
    else:
        print("✅ 모든 페이지 업스케일링 완료!")

def main():
    create_folders()
    print("3초 후 캡처를 시작합니다. 캡처할 화면으로 이동하세요...")
    time.sleep(3)

    x1, y1, x2, y2 = 71, 394, 1009, 1600
    next_page_x, next_page_y = 1047, 998
    empty_x, empty_y = 100, 100

    for i in range(641):
        page_num = i + 1
        print(f"페이지 {page_num}/641 캡처 중...")

        if i > 0:
            pyautogui.click(next_page_x, next_page_y)
            time.sleep(0.5)
        pyautogui.moveTo(empty_x, empty_y)
        time.sleep(0.5)
        time.sleep(1.5)
        
        screenshot = pyautogui.screenshot()
        original_path = f"original/page_{page_num}.png"
        screenshot.save(original_path)

        image = cv2.imread(original_path)
        cropped_page = image[y1:y2, x1:x2]
        cropped_filename = f"crop/cropped_page_{page_num}.png"
        cv2.imwrite(cropped_filename, cropped_page)
        
        upscaled_filename = f"upscale/upscaled_page_{page_num}.png"
        upscale_image(cropped_filename, upscaled_filename, scale=2.0)

        if page_num % 100 == 0:
            print(f"🔍 {page_num}페이지 완료, 누락 검사 중...")
            check_missing_upscaled()

    images_to_pdf([f"crop/cropped_page_{i}.png" for i in range(1, 642)], "pdf/output_original.pdf")
    images_to_pdf([f"upscale/upscaled_page_{i}.png" for i in range(1, 642)], "pdf/output_upscaled.pdf")
    print("🎉 모든 작업 완료! PDF 변환까지 끝났습니다!")

if __name__ == "__main__":
    main()
