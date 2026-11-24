import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangles

PAGE_W, PAGE_H = 210, 297
MARGIN = 15
LABEL_W = 15
COLS = 2
LETTERS = "abcdefghijklm"
ROWS = len(LETTERS)

cell_w = (PAGE_W -2 * MARGIN - LABEL_W) / COLS
Cell_h = (PAGE_H -2 * MARGIN) / ROWS
