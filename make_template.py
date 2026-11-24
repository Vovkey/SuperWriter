import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

PAGE_W, PAGE_H = 210, 297
MARGIN = 15
LABEL_W = 15
COLS = 2
LETTERS = "abcdefghijklm"
ROWS = len(LETTERS)

cell_w = (PAGE_W -2 * MARGIN - LABEL_W) / COLS
cell_h = (PAGE_H -2 * MARGIN) / ROWS

fig = plt.figure(figsize=(PAGE_W / 25.4, PAGE_H / 25.4))
ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, PAGE_W)
ax.set_ylim(PAGE_H, 0)
ax.axis("off")


for row, ch in enumerate(LETTERS):
    y = MARGIN + row * cell_h

    ax.text(MARGIN + LABEL_W / 2, y + cell_h / 2, ch,
        ha="center", va="center", fontsize=24)

    for col in range(COLS):
        x = MARGIN + LABEL_W + col * cell_w

        ax.add_patch(Rectangle((x, y), cell_w, cell_h,
            fill=False, edgecolor="0.85", linewidth=0.8))

        base_y = y + cell_h*0.7
        ax.plot([x, x + cell_w], [base_y, base_y], color="0.85", linewidth=0.8)

fig.savefig("template_page1.pdf")   # change to _page2 when LETTERS = "nopqrstuvwxyz"
