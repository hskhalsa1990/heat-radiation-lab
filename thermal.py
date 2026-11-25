"""Thermal image helpers shared by the dashboard and the PDF report."""
import numpy as np
from scipy import ndimage

def to_temperature(arr, t_min, t_max):
    """Greyscale array (any range) -> temperature grid in K, linearly mapped to [t_min, t_max]."""
    a = np.asarray(arr, float)
    if a.ndim == 3: a = a[..., :3].mean(axis=2)
    a = (a - a.min()) / max(a.max() - a.min(), 1e-12)
    return t_min + a * (t_max - t_min)

def detect_hotspots(T, k_sigma=3.0, smooth=1.0, min_pixels=5):
    """Return (mask, labels, spots). spots = list of dicts with x, y, peak_K, area_px."""
    img = ndimage.gaussian_filter(np.asarray(T, float), smooth)
    mask = img > img.mean() + k_sigma * img.std()
    lab, n = ndimage.label(mask); spots = []
    for k in range(1, n + 1):
        sel = lab == k
        if sel.sum() < min_pixels: mask[sel] = False; continue
        cy, cx = ndimage.center_of_mass(sel)
        spots.append(dict(x=round(cx), y=round(cy), peak_K=round(float(img[sel].max()), 1), area_px=int(sel.sum())))
    return mask, lab, sorted(spots, key=lambda s: -s["peak_K"])
