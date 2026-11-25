import sys

import cv2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from page import find_page, flatten_page
from preprocess import make_ink_mask
from strokes import extract_strokes

def save_debug(flat, ink, strokes):
    cv2.imwrite("flat.png", flat)
    cv2.imwrite("ink.png", ink)

    plt.figure(figsize=(10, 6))
    for s in strokes:
        plt.plot(s[:, 0], s[:, 1], "b-", lw=1)
    plt.gca().invert_yaxis()
    plt.gca().set_aspect("equal")
    plt.savefig("strokes_plot.png", dpi=200)
    plt.close()

def run(path, size_mm=(210, 297), px_per_mm=8, debug=True):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Couldn't load {path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    flat = flatten_page(gray, find_page(gray), size_mm, px_per_mm)
    ink = make_ink_mask(flat)
    strokes = extract_strokes(ink)

    if debug:
        save_debug(flat, ink, strokes)
    print(f"{len(strokes)} strokes, {sum(len(s) for s in strokes)} points")
    return strokes

if __name__ == "__main__":
 run(sys.argv[1] if len(sys.argv) > 1 else "test.jpeg")
