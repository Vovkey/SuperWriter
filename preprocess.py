import cv2
import numpy as np

def make_ink_mask(flat, blur_sigma=40, threshold=210, close=True):
    bg = cv2.GaussianBlur(flat, (0, 0), blur_sigma)
    norm = cv2.divide(flat, bg, scale=255)
    _, ink = cv2.threshold(norm, threshold, 255, cv2.THRESH_BINARY_INV)
    if close:
        ink = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    return ink
