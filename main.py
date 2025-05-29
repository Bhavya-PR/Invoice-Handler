from utils import preprocess
import cv2

images = preprocess.convert_pdf_to_images("input")
for i, img in enumerate(images):
    cv2.imwrite(f"output/page_{i+1}.png", img)
