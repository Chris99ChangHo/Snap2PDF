# 📸 Snap2PDF

**Snap2PDF**는 전자책이나 문서 화면을 자동으로 캡처하고 고해상도 PDF로 변환해주는 도구입니다.  
PyQt 기반 GUI와 OpenCV 업스케일링 기능을 통해 직관적이고 고품질의 결과물을 제공합니다.

---

## 🚀 주요 기능

- ✅ **영역 자동 캡처**: 지정한 영역을 페이지마다 자동 캡처
- ✅ **페이지 넘김 자동화**: 넘김 버튼 좌표를 기반으로 자동 전환
- ✅ **이미지 업스케일링**: OpenCV로 2배 확대 (고해상도 PDF 생성)
- ✅ **PDF 변환**: 캡처 이미지를 하나의 PDF로 저장
- ✅ **실시간 미리보기**: 캡처 과정 중 실시간으로 이미지 확인 가능
- ✅ **진행률 표시**: 캡처 및 변환 상태를 진행 바로 시각화

---

## 📥 다운로드 및 실행 방법

1. [Releases 페이지](https://github.com/Chris99ChangHo/Snap2PDF/releases)에서 **Snap2PDF.exe** 다운로드  
2. 다운로드한 파일을 실행  
3. 좌표 설정 및 캡처 시작  
4. PDF 변환 버튼 클릭

> 💡 Windows 환경에서는 **관리자 권한 실행**을 권장합니다.

---

## 🖱️ 사용 방법 (GUI 가이드)

### ① 캡처 영역 설정
- **[크롭 좌상단 좌표 설정]**, **[크롭 우하단 좌표 설정]** 버튼을 차례로 클릭
- 5초 후 마우스를 원하는 위치에 두면 자동 저장됨
- 설정 완료 메시지가 GUI에 표시됨

### ② 페이지 넘김 버튼 설정
- **[페이지 넘김 버튼 좌표 설정]** 클릭
- 마우스를 페이지 넘김 버튼에 올려놓으면 좌표 저장됨

### ③ 표지 미리보기
- **[표지(0번 페이지) 캡처 미리보기]** 버튼 클릭  
- 지정한 영역이 올바르게 크롭되는지 미리 확인 가능

### ④ 캡처 시작
1. 총 페이지 수 입력 (예: `50`)
2. **[캡처 시작]** 클릭
3. 자동 페이지 넘김 + 캡처 수행 (각 페이지 업스케일됨)
4. 진행률 바와 함께 실시간 미리보기 제공

### ⑤ PDF 변환
- **[PDF 변환]** 클릭 시 `PDF/` 폴더에 PDF 파일 저장됨  
- 파일명은 입력창에서 지정 가능 (`미입력 시 기본값 'output' 사용`)

---

## 🔍 이미지 업스케일링 (OpenCV 사용)

Snap2PDF는 `cv2.INTER_CUBIC` 보간법을 활용해 **이미지를 2배 확대**합니다.  
- 원본 캡처: `cropped/` 폴더에 저장  
- 업스케일 결과: `upscaled/` 폴더에 저장  
- 최종 PDF는 업스케일 이미지 기준으로 생성됩니다

---

## ⚠️ 주의 사항

- 관리자 권한 실행이 필요할 수 있습니다  
- 너무 많은 페이지 캡처 시 메모리 사용량이 증가할 수 있습니다  
- **OCR(텍스트 인식) 기능은 미포함**입니다 (추후 예정)

---

## 💡 향후 업데이트 예정

- OCR(광학 문자 인식) 기능  
- PDF 내 텍스트 검색 기능  
- 키보드 단축키 지원

---

## 📜 라이선스

이 프로젝트는 개인용으로 제작되었습니다.  
상업적 용도 또는 무단 배포는 제한될 수 있습니다.
