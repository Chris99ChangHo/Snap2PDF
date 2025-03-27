import sys
import os
import pyautogui
import cv2
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tqdm import tqdm
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QLineEdit

class EbookCaptureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.x1 = self.y1 = self.x2 = self.y2 = None
        self.next_page_x = self.next_page_y = None
        self.pdf_name = "output"
        
    def initUI(self):
        self.setWindowTitle("E-Book PDF 자동화 도구")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label_info = QLabel("좌표 설정 후 PDF 변환을 실행하세요.")
        layout.addWidget(self.label_info)
        
        self.btn_set_crop_start = QPushButton("크롭 좌상단 좌표 설정")
        self.btn_set_crop_start.clicked.connect(lambda: self.get_position("좌상단"))
        layout.addWidget(self.btn_set_crop_start)
        
        self.btn_set_crop_end = QPushButton("크롭 우하단 좌표 설정")
        self.btn_set_crop_end.clicked.connect(lambda: self.get_position("우하단"))
        layout.addWidget(self.btn_set_crop_end)
        
        self.btn_set_next_page = QPushButton("페이지 넘김 버튼 좌표 설정")
        self.btn_set_next_page.clicked.connect(lambda: self.get_position("페이지 넘김 버튼"))
        layout.addWidget(self.btn_set_next_page)
        
        self.pdf_name_input = QLineEdit(self)
        self.pdf_name_input.setPlaceholderText("저장할 PDF 파일명을 입력하세요")
        layout.addWidget(self.pdf_name_input)
        
        self.btn_start_capture = QPushButton("캡처 및 PDF 변환 시작")
        self.btn_start_capture.clicked.connect(self.start_capture)
        layout.addWidget(self.btn_start_capture)
        
        self.setLayout(layout)
    
    def get_position(self, label):
        time.sleep(5)  # 사용자가 마우스를 원하는 위치로 이동할 시간 제공
        x, y = pyautogui.position()
        self.label_info.setText(f"{label} 좌표 설정 완료: ({x}, {y})")
        
        if label == "좌상단":
            self.x1, self.y1 = x, y
        elif label == "우하단":
            self.x2, self.y2 = x, y
        elif label == "페이지 넘김 버튼":
            self.next_page_x, self.next_page_y = x, y
    
    def create_folders(self):
        folders = ["original", "crop", "upscale", "pdf"]
        for folder in folders:
            os.makedirs(folder, exist_ok=True)

    def upscale_image(self, image_path, save_path=None, scale=2.0):
        img = cv2.imread(image_path)
        upscaled = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        if save_path:
            cv2.imwrite(save_path, upscaled, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        return upscaled

    def images_to_pdf(self, image_list, output_pdf):
        c = canvas.Canvas(output_pdf, pagesize=letter)
        for img_path in image_list:
            c.drawImage(img_path, 50, 50, width=500, height=700, preserveAspectRatio=True)
            c.showPage()
        c.save()

    def start_capture(self):
        if None in [self.x1, self.y1, self.x2, self.y2, self.next_page_x, self.next_page_y]:
            self.label_info.setText("모든 좌표를 설정하세요!")
            return

        self.create_folders()
        self.pdf_name = self.pdf_name_input.text() or "output"
        original_pdf = f"pdf/{self.pdf_name}_original.pdf"
        upscaled_pdf = f"pdf/{self.pdf_name}_upscaled.pdf"
        empty_x, empty_y = 100, 100  
        
        for i in tqdm(range(641), desc="📸 캡처 진행 중", unit="page"):
            page_num = i + 1
            
            if i > 0:
                pyautogui.click(self.next_page_x, self.next_page_y)
                time.sleep(0.5)

            pyautogui.moveTo(empty_x, empty_y)
            time.sleep(0.5)
            time.sleep(1.5)

            screenshot = pyautogui.screenshot()
            original_path = f"original/page_{page_num}.png"
            screenshot.save(original_path)

            image = cv2.imread(original_path)
            cropped_page = image[self.y1:self.y2, self.x1:self.x2]
            cropped_filename = f"crop/cropped_page_{page_num}.png"
            cv2.imwrite(cropped_filename, cropped_page)

            upscaled_filename = f"upscale/upscaled_page_{page_num}.png"
            self.upscale_image(cropped_filename, upscaled_filename, scale=2.0)
        
        self.images_to_pdf([f"crop/cropped_page_{i}.png" for i in range(1, 642)], original_pdf)
        self.images_to_pdf([f"upscale/upscaled_page_{i}.png" for i in range(1, 642)], upscaled_pdf)
        
        self.label_info.setText(f"🎉 PDF 저장 완료! {original_pdf}, {upscaled_pdf}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EbookCaptureApp()
    ex.show()
    sys.exit(app.exec())
