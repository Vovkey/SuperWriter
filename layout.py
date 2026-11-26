PAGE_W, PAGE_H = 210, 297
MARGIN = 15
LABEL_W = 15
COLS = 3
BASELINE_FRAC = 0.7
PAGES = ["abcdefghijklm", "nopqrstuvwxyz"]

def cell_box(row, col, n_rows):
    cell_w = (PAGE_W - 2 * MARGIN - LABEL_W) / COLS
    cell_h = (PAGE_H - 2 * MARGIN) / n_rows
    x0 = MARGIN + LABEL_W + col + cell_w
    y0 = MARGIN + row * cell_h
    return x0, y0, x0 + cell_w, y0 + cell_h
