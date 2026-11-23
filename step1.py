from asyncio.streams import start_server

import cv2
import matplotlib
from scipy.ndimage import convolve

matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
import numpy as np
from skimage.morphology import skeletonize

from page import find_page, flatte_page

img = cv2.imread("test.jpeg")
if img is None:
    raise FileNotFoundError("Couldn't load the image -check the path")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
flat = flatte_page(gray, find_page(gray))[20:-20, 20:-20]

blur = cv2.GaussianBlur(flat, (5, 5), 0)

_, otsu = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

ink = cv2.adaptiveThreshold(
    blur, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31, 10,
)


adaptive = cv2.adaptiveThreshold(
    blur, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31, 10,
)

skeleton = skeletonize(ink > 0)
skel_img = (skeleton * 255).astype(np.uint8)
sk = skeleton.astype(np.uint8)

kernel = np.ones((3, 3), dtype=np.uint8)
kernel[1, 1] = 0

neighbors = convolve(sk, kernel, mode="constant") * sk

endpoints = np.argwhere(neighbors == 1)
junctions = np.argwhere(neighbors >= 3)

print("Endpoints:", len(endpoints))
print("Junction pixels:", len(junctions))

def get_neighbors(sk, r, c):
    h, w = sk.shape
    result = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and sk[nr, nc]:
                result.append((nr, nc))
    return result

def trace(sk, endpoints):
    visited = set()
    strokes = []

    for start in endpoints:
        start = tuple(start)
        if start in visited:
            continue

        path = [start]
        visited.add(start)
        current = start

        while True:
            nbrs = get_neighbors(sk, *current)
            nbrs = [p for p in nbrs if p not in visited]
            if not nbrs:
                break
            current = nbrs[0]
            path.append(current)
            visited.add(current)

        strokes.append(path)
    return strokes

fig, axes = plt.subplots(1, 3, figsize=(12,6))
for ax, im, title in zip(axes, [flat, ink, skel_img], ["Flat", "Ink mask", "Skeleton"]):
    ax.imshow(im, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.savefig("skeleton.png", dpi=150)

strokes = trace(sk, endpoints)
print("Number of Strokes:", len(strokes))
print("Lengths:", [len(s) for s in strokes])

canvas = np.zeros((*skeleton.shape, 3), np.uint8)
for stroke in strokes:
    col = [int(v) for v in np.random.randint(80, 256, 3)]
    for y, x in stroke:
        canvas[y, x] = col
cv2.imwrite("strokes.png", cv2.dilate(canvas, np.ones((3, 3), np.uint8)))
