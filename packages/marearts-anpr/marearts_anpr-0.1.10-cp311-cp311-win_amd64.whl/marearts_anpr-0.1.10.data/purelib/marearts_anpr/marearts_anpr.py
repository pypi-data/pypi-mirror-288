#marearts_anpr.py
import cv2
from PIL import Image
from marearts_anpr import ma_anpr_detector
from marearts_anpr import ma_anpr_ocr
import time 
import numpy as np

def marearts_anpr_from_pil(anpr_d, anpr_r, pil_img):
    # Convert the PIL image to RGB if it's not already
    if pil_img.mode != "RGB":
        pil_img = pil_img.convert(mode="RGB")
    # Convert PIL Image to a NumPy array (compatible with OpenCV functions if needed)
    img = np.array(pil_img)
    return marearts_anpr_from_cv2(anpr_d, anpr_r, img)

def marearts_anpr_from_image_file(anpr_d, anpr_r, image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image from {image_path}")
    print(f"Loaded image shape: {img.shape}, dtype: {img.dtype}")
    return marearts_anpr_from_cv2(anpr_d, anpr_r, img)

def marearts_anpr_from_cv2(anpr_d, anpr_r, img):
    start_time = time.time()
    # eu image
    #marearts anpr detector
    detections = anpr_d.detector(img)
    ltrb_time = time.time() - start_time

    results = []
    ocr_time = 0
    for box_info in detections:
        # Crop image
        l, t, r, b = box_info['box']
        crop_img = img[int(t):int(b), int(l):int(r)]

        if crop_img.size == 0:
            continue

        # Convert to PIL Image
        pil_img = Image.fromarray(crop_img)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert(mode="RGB")

        start_time = time.time()
        #marearts anpr ocr
        ocr_result = anpr_r.predict(pil_img)
        ocr_time += time.time() - start_time

        # Append results
        results.append({
            "ocr": ocr_result[0],
            "ocr_conf": ocr_result[1],
            "ltrb": [int(l), int(t), int(r), int(b)],
            "ltrb_conf": int(box_info['score'] * 100)
        })

    output = { "results": results, "ltrb_proc_sec": round(ltrb_time, 2), "ocr_proc_sec": round(ocr_time, 2)}
    return output


if __name__ == '__main__':

    #################################
    ##initiate marearts anpr
    user_name = "your email"
    serial_key = "your key"
    detector_model_version = "middle" #samll, large
    ocr_model_version = "eu" #"kr"

    #marearts anpr detector inference
    anpr_d = ma_anpr_detector(detector_model_version, user_name, serial_key, conf_thres=0.3, iou_thres=0.5)
    #marearts anpr ocr inference
    anpr_r = ma_anpr_ocr(ocr_model_version, user_name, serial_key)
    #################################

    #################################
    #Routine Task 1 - predict from file
    image_path = './sample_images/eu_test1.jpg'
    output = marearts_anpr_from_image_file(anpr_d, anpr_r, image_path)
    print(output)

    #Routine Task 2 - predict from cv2
    img = cv2.imread(image_path)
    output = marearts_anpr_from_cv2(anpr_d, anpr_r, img)
    print(output)

    #Routine Task 2 - predict from pillow
    pil_img = Image.open(image_path)
    output = marearts_anpr_from_pil(anpr_d, anpr_r, pil_img)
    print(output)
    #################################