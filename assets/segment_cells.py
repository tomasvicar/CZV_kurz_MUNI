import glob
import os
import re

import matplotlib.pyplot as plt
import numpy as np
import tifffile
from scipy import ndimage as ndi
from skimage import exposure, feature, filters, measure, morphology, segmentation

DATA_DIR = "data_celltypes"
OUT_DIR = "results"
MIN_CELL_AREA = 200

os.makedirs(OUT_DIR, exist_ok=True)


def segment(img):
    # Normalize per-image to 0..1 for stable thresholding across conditions.
    lo, hi = np.percentile(img, (1, 99.5))
    norm = np.clip((img - lo) / (hi - lo + 1e-8), 0, 1)

    # Rolling-ball-style background subtraction using a large Gaussian.
    background = filters.gaussian(norm, sigma=40, preserve_range=True)
    flat = np.clip(norm - background, 0, None)

    smooth = filters.gaussian(flat, sigma=2, preserve_range=True)

    # Triangle threshold is more permissive than Otsu when foreground is sparse
    # and low-contrast (dim PC3 cells), so it catches them too.
    thr = filters.threshold_triangle(smooth)
    fg = smooth > thr
    fg = morphology.remove_small_holes(fg, area_threshold=300)
    fg = morphology.binary_opening(fg, morphology.disk(2))
    fg = morphology.remove_small_objects(fg, min_size=MIN_CELL_AREA)

    # Seed markers at local intensity maxima of a strongly smoothed image —
    # one seed per cell body — then watershed on the inverted smoothed image.
    seed_src = filters.gaussian(flat, sigma=6, preserve_range=True)
    coords = feature.peak_local_max(
        seed_src, min_distance=10, threshold_abs=thr * 0.5, labels=fg
    )
    marker_img = np.zeros(img.shape, dtype=bool)
    if len(coords):
        marker_img[tuple(coords.T)] = True
    markers = measure.label(marker_img)

    labels = segmentation.watershed(-seed_src, markers, mask=fg)
    labels = morphology.remove_small_objects(labels, min_size=MIN_CELL_AREA)
    return labels


def cell_type(path):
    m = re.search(r"_([A-Za-z0-9]+)_img", os.path.basename(path))
    return m.group(1) if m else "unknown"


sizes_by_type = {}
example_saved = {}

for path in sorted(glob.glob(os.path.join(DATA_DIR, "*.tif"))):
    img = tifffile.imread(path)
    labels = segment(img)
    props = measure.regionprops(labels)
    areas = [p.area for p in props]

    ctype = cell_type(path)
    sizes_by_type.setdefault(ctype, []).extend(areas)
    print(f"{os.path.basename(path)} [{ctype}]: {len(areas)} cells")

    if ctype not in example_saved:
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].imshow(img, cmap="gray")
        ax[0].set_title(f"{ctype} — input")
        ax[0].axis("off")
        ax[1].imshow(img, cmap="gray")
        ax[1].imshow(
            np.ma.masked_where(labels == 0, labels),
            cmap="nipy_spectral",
            alpha=0.5,
        )
        ax[1].set_title(f"{ctype} — segmentation ({len(areas)} cells)")
        ax[1].axis("off")
        fig.tight_layout()
        fig.savefig(os.path.join(OUT_DIR, f"qc_{ctype}.png"), dpi=120)
        plt.close(fig)
        example_saved[ctype] = True

types = sorted(sizes_by_type)
fig, ax = plt.subplots(figsize=(6, 5))
ax.boxplot([sizes_by_type[t] for t in types], tick_labels=types, showfliers=True)
ax.set_ylabel("Cell area (pixels)")
ax.set_title("Cell size by type")
fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "boxplot_cell_sizes.png"), dpi=120)
plt.close(fig)

for t in types:
    a = np.array(sizes_by_type[t])
    print(f"{t}: n={len(a)}  median={np.median(a):.0f}  mean={a.mean():.0f}")
