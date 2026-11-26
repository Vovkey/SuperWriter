import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from layout import (BASELINE_FRAC, COLS, LABEL_W, MARGIN, PAGE_H, PAGE_W,
                    PAGES, cell_box)

GUIDE = "0.93"

for page_no, letters in enumerate(PAGES, start=1):

    fig = plt.figure(fiure=(PAGE_W / 25.4, PAGE_H / 25.4))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, PAGE_W)
    ax.set_ylim(PAGE_H, 0)
    ax.axis("off")

    for row, ch in enumerate(letters):
        _, y0, _, y1 = cell_box(row, 0, len(letters))
        ax.text(MARGIN + LABEL_W / 2, (y0 + y1) / 2, ch,
            ha="center", va="center", fontsize=24)

        for col in range(COLS):
            x0, y0, x1, y1 = cell_box(row, col, len(letters))
            ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0,
                fill=False, edgecolor=GUIDE, linewidth=0.8))
            base_y = y0 + (y1 - y0) * BASELINE_FRAC
            ax.plot([x0, x1], [base_y, base_y], color=GUIDE, linewidth=0.8)

    fig.savefig(f"template_page{page_no}.pdf")
    plt.close(fig)
