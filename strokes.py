import numpy as np
from scipy.interpolate import splev, splprep
from scipy.ndimage import convolve
from skimage.morphology import skeletonize


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
            nbrs = [p for p in get_neighbors(sk, *current) if p not in visited]
            if not nbrs:
                break
            current = nbrs[0]
            path.append(current)
            visited.add(current)
        strokes.append(path)
    return strokes

def smooth_resample(stroke, spacing=3.0, smoothing=1.0):
    pts = np.array([(x, y) for y, x in stroke], dtype=float)
    keep = np.r_[True, np.any(np.diff(pts, axis=0) != 0, axis=1)]
    pts = pts[keep]
    if len(pts) < 4:
        return pts
    tck, _ = splprep([pts[:, 0], pts[:, 1]], s=smoothing * len(pts), k=3)
    length = np.sum(np.hypot(*np.diff(pts, axis=0).T))
    n = max(int(length / spacing), 2)
    x, y = splev(np.linspace(0, 1, n), tck)
    return np.column_stack([x, y])

def extract_strokes(ink, spacing=3.0, smoothing=1.0, min_len=4):
    sk = skeletonize(ink > 0).astype(np.uint8)

    kernel = np.ones((3, 3), dtype=np.uint8)
    kernel[1, 1] = 0
    neighbors = convolve(sk, kernel, mode="constant") * sk
    endpoints = np.argwhere(neighbors == 1)

    raw = trace(sk, endpoints)
    return [smooth_resample(s, spacing, smoothing) for s in raw if len(s) >= min_len]
