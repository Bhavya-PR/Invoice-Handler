import os
import cv2

def crop_seal_signature(image, ocr_data, output_folder="output", page_num=1):
    candidates = [d for d in ocr_data if 'seal' in d['text'].lower() or 'sign' in d['text'].lower()]
    if candidates:
        for idx, cand in enumerate(candidates):
            x, y, w, h = cand['left'], cand['top'], cand['width'], cand['height']
            crop = image[y:y+h+50, x:x+w+100]
            filename = f"seal_signature_page_{page_num}_{idx+1}.png"
            cv2.imwrite(os.path.join(output_folder, filename), crop)
            print(f"Saved cropped seal/signature: {filename}")
    else:
        print(f"No seal or signature detected on page {page_num}")
