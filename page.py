import cv2
import numpy as np

def order_corners(pts):
    pts = pts.reshape(4, 2).astype("float32")
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)[:, 0]
    return np.array([
        pts[np.argmin(s)],
        pts[np.argmin(d)],
        pts[np.argmax(s)],
        pts[np.argmax(d)],
    ], dtype = "float32")

def find_page(gray):
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No page found. Is the paper on a darker background?")
    page = max(contours, key=cv2.contourArea)

    peri = cv2.arcLength(page, True)
    approx = cv2.approxPolyDP(page, 0.02 * peri, True)
    if len(approx) != 4:
        approx = cv2.boxPoints(cv2.minAreaRect(page))
    return order_corners(approx)

def flatten_page(img, corners, size_mm=(210, 297), px_per_mm=8):
    w = int(size_mm[0] * px_per_mm)
    h = int(size_mm[1] * px_per_mm)
    dst = np.array([[0, 0], [w - 1, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]],
        dtype="float32")
    M = cv2.getPerspectiveTransform(corners, dst)
    return cv2.warpPerspective(img, M, (w, h))
