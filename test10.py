import sys
import os
import pyautogui
import cv2
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tqdm import tqdm
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class EbookCaptureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.x1 = self.y1 = self.x2 = self.y2 = None
        self.next_page_x = self.next_page_y = None
        self.pdf_name = "output"
        self.page_count = 0

    def initUI(self):
        self.setWindowTitle("E-Book PDF 자동화 도구")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QHBoxLayout()

        # 좌측: 이미지 미리보기
        self.preview_label = QLabel("미리보기")
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setFixedSize(400, 500)  # 크기 조정하여 스크롤바 방지

        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_label)
        preview_layout.addWidget(self.graphics_view)

        # 우측: 버튼 및 입력창
        control_layout = QVBoxLayout()
        self.label_info = QLabel("좌표 설정 후 PDF 변환을 실행하세요.")
        control_layout.addWidget(self.label_info)

        self.btn_set_crop_start = QPushButton("크롭 좌상단 좌표 설정")
        self.btn_set_crop_start.clicked.connect(lambda: self.get_position("좌상단"))
        control_layout.addWidget(self.btn_set_crop_start)

        self.btn_set_crop_end = QPushButton("크롭 우하단 좌표 설정")
        self.btn_set_crop_end.clicked.connect(lambda: self.get_position("우하단"))
        control_layout.addWidget(self.btn_set_crop_end)

        self.btn_set_next_page = QPushButton("페이지 넘김 버튼 좌표 설정")
        self.btn_set_next_page.clicked.connect(lambda: self.get_position("페이지 넘김 버튼"))
        control_layout.addWidget(self.btn_set_next_page)

        self.btn_preview_crop = QPushButton("표지(0번 페이지) 캡처 미리보기")
        self.btn_preview_crop.clicked.connect(self.preview_capture)
        control_layout.addWidget(self.btn_preview_crop)

        self.pdf_name_input = QLineEdit(self)
        self.pdf_name_input.setPlaceholderText("저장할 PDF 파일명을 입력하세요")
        control_layout.addWidget(self.pdf_name_input)

        self.page_count_input = QLineEdit(self)
        self.page_count_input.setPlaceholderText("캡처할 총 페이지 수 입력")
        control_layout.addWidget(self.page_count_input)

        self.btn_start_capture = QPushButton("캡처 및 PDF 변환 시작")
        self.btn_start_capture.clicked.connect(self.start_capture)
        control_layout.addWidget(self.btn_start_capture)

        main_layout.addLayout(preview_layout, 3)
        main_layout.addLayout(control_layout, 2)
        self.setLayout(main_layout)

    def get_position(self, label):
        time.sleep(5)
        x, y = pyautogui.position()
        self.label_info.setText(f"{label} 좌표 설정 완료: ({x}, {y})")
        
        if label == "좌상단":
            self.x1, self.y1 = x, y
        elif label == "우하단":
            self.x2, self.y2 = x, y
        elif label == "페이지 넘김 버튼":
            self.next_page_x, self.next_page_y = x, y

    def show_preview(self, image_path):
        image = QImage(image_path).scaled(400, 500, Qt.AspectRatioMode.KeepAspectRatio)
        pixmap = QPixmap.fromImage(image)
        self.scene.clear()
        item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(item)

    def preview_capture(self):
        if None in [self.x1, self.y1, self.x2, self.y2]:
            self.label_info.setText("⚠️ 좌표 설정을 먼저 완료하세요!")
            return

        screenshot = pyautogui.screenshot(region=(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
        preview_filename = "crop/preview.png"
        screenshot.save(preview_filename)
        self.show_preview(preview_filename)
        self.label_info.setText("✅ 미리보기 완료!")

    def start_capture(self):
        if None in [self.x1, self.y1, self.x2, self.y2, self.next_page_x, self.next_page_y]:
            self.label_info.setText("⚠️ 모든 좌표를 설정하세요!")
            return

        if not (self.x1 < self.x2 and self.y1 < self.y2):
            self.label_info.setText("⚠️ 좌표 설정 오류: 올바른 범위를 지정하세요!")
            return

        try:
            self.page_count = int(self.page_count_input.text())
        except ValueError:
            self.label_info.setText("⚠️ 유효한 페이지 수를 입력하세요!")
            return

        os.makedirs("crop", exist_ok=True)
        os.makedirs("pdf", exist_ok=True)
        pdf_path = f"pdf/{self.pdf_name}.pdf"
        
        image_list = []
        
        for i in tqdm(range(self.page_count), desc="📸 캡처 진행 중", unit="page"):
            page_num = i + 1
            
            if i > 0:
                pyautogui.click(self.next_page_x, self.next_page_y)
                time.sleep(1.5)  # 페이지 넘김 후 대기
            
            self.label_info.setText(f"📷 {page_num}페이지 캡처 중...")
            screenshot = pyautogui.screenshot(region=(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
            cropped_filename = f"crop/page_{page_num}.png"
            screenshot.save(cropped_filename)
            
            self.show_preview(cropped_filename)
            self.label_info.setText(f"✅ {page_num}페이지 캡처 완료!")
            
            image_list.append(cropped_filename)
        
        self.label_info.setText("📄 PDF 변환 중...")
        for _ in tqdm(image_list, desc="📄 PDF 변환 진행 중", unit="page"):
            pass  # tqdm GUI 표시용
        
        self.images_to_pdf(image_list, pdf_path)
        self.label_info.setText(f"🎉 PDF 저장 완료! {pdf_path}")

    def images_to_pdf(self, image_list, output_pdf):
        c = canvas.Canvas(output_pdf, pagesize=letter)
        for img_path in image_list:
            c.drawImage(img_path, 50, 50, width=500, height=700, preserveAspectRatio=True)
            c.showPage()
        c.save()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EbookCaptureApp()
    ex.show()
    sys.exit(app.exec())
