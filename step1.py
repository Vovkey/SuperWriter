
import cv2
import matplotlib
from scipy.interpolate import splev, splprep
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

bg = cv2.GaussianBlur(flat, (0, 0), 30 )
norm = cv2.divide(flat, bg, scale=255)
_, ink = cv2.threshold(norm, 210, 255, cv2.THRESH_BINARY_INV)
ink = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

"""
ink = cv2.adaptiveThreshold(
    blur, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    31, 10,
)
"""

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

covered = set(p for s in strokes for p in s)
all_skel = set(map(tuple, np.argwhere(sk)))
missing = all_skel-covered
print("Skeleton pixels", len(all_skel))
print("Covered", len(covered))
print("Missed", len(missing))

canvas = np.zeros((*skeleton.shape, 3), np.uint8)
for stroke in strokes:
    col = [int(v) for v in np.random.randint(80, 256, 3)]
    for y, x in stroke:
        canvas[y, x] = col
for y, x in missing:
    canvas[y, x] = (0, 0, 255)
cv2.imwrite("strokes.png", cv2.dilate(canvas, np.ones((3, 3), np.uint8)))

def smooth_resample(stroke, spacing=3.0, smoothing=1.0):
    pts = np.array([(x, y) for y, x in stroke], dtype=float)
    keep = np.r_[True, np.any(np.diff(pts, axis=0) != 0, axis=1)]
    pts = pts[keep]
    if len(pts) < 4:
        return pts

    tck, _ = splprep([pts[:, 0], pts[:, 1]], s=smoothing * len(pts), k=3)

    length = np.sum(np.hypot(*np.diff(pts, axis=0).T))
    n = max (int(length / spacing), 2)
    u = np.linspace(0, 1, n)
    x, y = splev(u, tck)
    return np.column_stack([x, y])

def simplify(stroke, epsilon=1.0):
    pts = np.array([(x, y) for y, x in stroke], dtype=np.float32).reshape(-1, 1, 2)
    approx = cv2.approxPolyDP(pts, epsilon, False)
    return approx.reshape(-1, 2)

plt.figure(figsize=(10, 6))
for s in strokes:
    if len(s) < 4:
        continue
    a = simplify(s, 2.0)
    b= smooth_resample(s)
    plt.plot(a[:, 0], a[:, 1], "r-", lw=1)
    plt.plot(b[:, 0], b[:, 1], "b-", lw=1)
plt.gca().invert_yaxis()
plt.gca().set_aspect("equal")
plt.savefig("compare.png", dpi=200)

cv2.imwrite("ink.png", ink)
