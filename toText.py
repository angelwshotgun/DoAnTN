import os
from pdf2image import convert_from_path
import cv2
import pytesseract
from PIL import Image

def pdf_to_text(pdf_path, output_folder):
    # Tạo thư mục đầu ra nếu chưa tồn tại
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Chuyển đổi PDF thành danh sách các hình ảnh
    pages = convert_from_path(pdf_path)

    text_output = ""

    for i, page in enumerate(pages):
        # Lưu hình ảnh tạm thời
        image_path = os.path.join(output_folder, f'page_{i+1}.jpg')
        page.save(image_path, 'JPEG')

        # Đọc hình ảnh bằng OpenCV
        image = cv2.imread(image_path)

        # Tiền xử lý hình ảnh
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(gray)
        thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Thực hiện OCR
        text = pytesseract.image_to_string(thresh, lang='vie')
        text_output += text + "\n\n"

        # Xóa file hình ảnh tạm thời
        os.remove(image_path)

    # Lưu văn bản đầu ra
    with open(os.path.join(output_folder, 'output.txt'), 'w', encoding='utf-8') as f:
        f.write(text_output)

    return text_output

# Sử dụng hàm
pdf_path = "C:\\Users\\z\\Documents\\vu\\python\\DoAn\\datasets\\pdf\\264QD-TCKT_0001.pdf"
output_folder = "C:\\Users\\z\\Documents\\vu\\python\\DoAn\\datasets\\output"

extracted_text = pdf_to_text(pdf_path, output_folder)