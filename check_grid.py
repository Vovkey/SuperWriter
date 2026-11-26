import sys
import cv2

from layout import PAGES, COLS, cell_box
from page import find_page, flatten_page

PX_PER_MM = 8

path = sys.argv[1]
page_no = int(sys.argv[2])

img = cv2.imread(path)
if img is None:
    raise FileNotFoundError(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
flat = flatten_page(gray, find_page(gray), px_per_mm=PX_PER_MM)

vis =cv2.cvtColor(flat, cv2.COLOR_GRAY2BGR)
letters = PAGES[page_no - 1]
for row in range(len(letters)):
    for col in range(COLS):
        x0, y0, x1, y1 = cell_box(row, col, len(letters))
        cv2.rectangle(vis,
            (int(x0 * PX_PER_MM), int(y0 * PX_PER_MM)),
            (int(x1 * PX_PER_MM), int(y1 * PX_PER_MM)),
            (0, 0, 255), 3)

cv2.imwrite("grid_check.png", vis)
print("Wrote grid_check.png")
