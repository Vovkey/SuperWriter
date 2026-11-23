from pickletools import uint8

import cv2
import matplotlib

matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
import numpy as np
from page import find_page, flatte_page
from skimage.morphology import skeletonize

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

fig, axes = plt.subplots(1, 3, figsize=(12,6))
for ax, im, title in zip(axes, [flat, ink, skel_img], ["Flat", "Ink mask", "Skeleton"]):
    ax.imshow(im, cmap="gray")
    ax.set_title(title)
    ax.axis("off")
plt.savefig("skeleton.png", dpi=150)
