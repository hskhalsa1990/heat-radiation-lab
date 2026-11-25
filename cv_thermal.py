"""Computer vision: synthetic thermal image, hot-spot detection."""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage
from radiation import net_flux

import sys
def load_real(path, t_min, t_max):
    """Real thermal image: greyscale PNG/JPG mapped linearly to [t_min, t_max] K, or a .csv/.npy temperature grid."""
    if path.endswith(".npy"): return np.load(path).astype(float)
    if path.endswith(".csv"): return np.loadtxt(path, delimiter=",")
    g = plt.imread(path).astype(float)
    g = g.mean(axis=2) if g.ndim == 3 else g
    g = g / g.max()
    return t_min + g * (t_max - t_min)

if len(sys.argv) >= 4:      # python3 cv_thermal.py image.png 290 420
    img = ndimage.gaussian_filter(load_real(sys.argv[1], float(sys.argv[2]), float(sys.argv[3])), 1)
else:                       # synthetic demo
    rng = np.random.default_rng(1)
    y, x = np.mgrid[0:200, 0:200]
    img = 300 + rng.normal(0, 1.5, (200, 200))
    for cx, cy, s, a in [(50, 60, 10, 220), (140, 120, 14, 330), (150, 40, 7, 150)]:
        img += a * np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * s**2))
    img = ndimage.gaussian_filter(img, 1)
mask = img > img.mean() + 3 * img.std()
lab, n = ndimage.label(mask)
print("Hot spots found:", n)
fig, ax = plt.subplots(1, 3, figsize=(13, 4))
for i, (a, t, c) in enumerate([(img, "Thermal image (K)", "inferno"), (mask, "Hot-spot mask", "gray"),
                               (net_flux(.9, img, 300) / 1e3, "Radiated flux (kW/m2)", "magma")]):
    im = ax[i].imshow(a, cmap=c); ax[i].set_title(t); ax[i].axis("off"); fig.colorbar(im, ax=ax[i], shrink=.7)
for k in range(1, n + 1):
    cy, cx = ndimage.center_of_mass(mask, lab, k)
    print(f" spot {k}: ({cx:.0f},{cy:.0f}) peak {img[lab==k].max():.0f} K")
fig.tight_layout(); fig.savefig("fig_cv_thermal.png", dpi=120)
