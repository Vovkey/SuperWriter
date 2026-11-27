from config import load
from make_template import GUIDE

_cfg = load()
_paper, _t = _cfg["paper"], _cfg["template"]

PAGE_W, PAGE_H = _paper["width_mm"], _paper["height_mm"]
MARGIN = _t["margin"]
LABEL_W = _t["label_w"]
COLS = _t["cols"]
BASELINE_FRAC = _t["baseline_frac"]
PAGES = _t["pages"]
GUIDE = _t["guide_gray"]

def cell_box(row, col, n_rows):
    cell_w = (PAGE_W - 2 * MARGIN - LABEL_W) / COLS
    cell_h = (PAGE_H - 2 * MARGIN) / n_rows
    x0 = MARGIN + LABEL_W + col + cell_w
    y0 = MARGIN + row * cell_h
    return x0, y0, x0 + cell_w, y0 + cell_h
