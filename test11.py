import sys
import os
import pyautogui
import cv2
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QProgressBar)
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
        self.image_list = []

    def initUI(self):
        self.setWindowTitle("E-Book PDF 자동화 도구")
        self.setGeometry(100, 100, 900, 600)

        main_layout = QHBoxLayout()

        # 좌측: 이미지 미리보기
        self.preview_label = QLabel("미리보기")
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setFixedSize(400, 500)

        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_label)
        preview_layout.addWidget(self.graphics_view)

        # 우측: 버튼 및 입력창
        control_layout = QVBoxLayout()

        self.label_info = QLabel("좌표 설정 후 PDF 변환을 실행하세요.")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        self.btn_start_capture = QPushButton("캡처 시작")
        self.btn_start_capture.clicked.connect(self.start_capture)
        control_layout.addWidget(self.btn_start_capture)

        self.btn_start_pdf = QPushButton("PDF 변환")
        self.btn_start_pdf.clicked.connect(self.start_pdf_conversion)
        control_layout.addWidget(self.btn_start_pdf)
        
        self.progress_bar = QProgressBar(self)
        control_layout.addWidget(self.progress_bar)

        main_layout.addLayout(preview_layout, 3)
        main_layout.addLayout(control_layout, 2)
        self.setLayout(main_layout)

    def get_position(self, label):
        time.sleep(5)
        x, y = pyautogui.position()
        self.label_info.setText(f"✅ {label} 좌표 설정 완료: ({x}, {y})")
        
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
        os.makedirs("preview", exist_ok=True)
        preview_filename = "preview/preview.png"
        screenshot.save(preview_filename)
        self.show_preview(preview_filename)
        self.label_info.setText("✅ 미리보기 완료!")

    def upscale_image(self, image_path):
        img = cv2.imread(image_path)
        upscaled = cv2.resize(img, (img.shape[1] * 2, img.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
        upscaled_path = image_path.replace("croped", "upscaled")
        os.makedirs("upscaled", exist_ok=True)
        cv2.imwrite(upscaled_path, upscaled)
        return upscaled_path

    def start_capture(self):
        self.page_count = int(self.page_count_input.text()) if self.page_count_input.text().isdigit() else 0
        if self.page_count <= 0:
            self.label_info.setText("⚠️ 페이지 수를 올바르게 입력하세요!")
            return

        self.label_info.setText("📸 캡처 진행 중...")
        self.image_list.clear()
        os.makedirs("croped", exist_ok=True)
        for i in range(self.page_count):
            if i > 0:
                pyautogui.click(self.next_page_x, self.next_page_y)
                time.sleep(1.5)
            screenshot = pyautogui.screenshot(region=(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
            filename = f"croped/page_{i+1}.png"
            screenshot.save(filename)
            upscaled_filename = self.upscale_image(filename)
            self.image_list.append(upscaled_filename)
            self.show_preview(upscaled_filename)  # 실시간 미리보기 업데이트
            QApplication.processEvents()  # UI 업데이트 반영
            self.progress_bar.setValue(int((i + 1) / self.page_count * 100))
        self.label_info.setText("✅ 캡처 완료!")

    def start_pdf_conversion(self):
        pdf_name = self.pdf_name_input.text().strip() # or "output"
        pdf_path = f"PDF/{pdf_name}.pdf"
        self.images_to_pdf(self.image_list, pdf_path)
        self.label_info.setText("✅ PDF 변환 완료!")

    def images_to_pdf(self, image_list, pdf_path):
        c = canvas.Canvas(pdf_path, pagesize=letter)
        for img_path in image_list:
            c.drawImage(img_path, 50, 50, 500, 700)
            c.showPage()
        c.save()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EbookCaptureApp()
    window.show()
    sys.exit(app.exec())
