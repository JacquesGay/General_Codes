#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# User Settings
# -------------------------------------------------------------------
cut = -2  # number of frames to trim from the end (set None to disable)

home = os.getcwd()

# Collect directories: each key maps to a sorted list of subdirectories
dirs = {
    d: sorted(
        [
            sub
            for sub in os.listdir(os.path.join(home, d))
            if os.path.isdir(os.path.join(home, d, sub))
        ]
    )
    for d in os.listdir(home)
    if os.path.isdir(os.path.join(home, d))
}

# COLVAR columns (example header for reference):
# #! FIELDS time CV1 dtyr-ha dlig-ha CV2 dglu-hb dlig-hb c1-c2 CV3
# Choose which two CV columns to plot:
row_labels = ["CV1", "c1-c2"]
id1, id2 = 1, 7  # zero-based indices

# -------------------------------------------------------------------
# Figure layout: rows = groups, cols = 2 (CV1, CV2)
# -------------------------------------------------------------------
panel_order = list(dirs.keys())
n_groups = len(panel_order)
ncols = 2

fig, axes = plt.subplots(
    n_groups, ncols,
    figsize=(12, max(3, 3 * n_groups)),
    tight_layout=True,
    sharex=True
)

# Normalize axes indexing to 2D array
if n_groups == 1:
    axes = np.atleast_2d(axes)

# Colors: use max group length to size the colormap
max_items = max((len(dirs[g]) for g in panel_order), default=1)
cmap = plt.get_cmap('rainbow')
colors = cmap(np.linspace(0, 1, max_items))

for row_idx, group in enumerate(panel_order):
    subdirs = dirs[group]
    ax_left = axes[row_idx, 0]
    ax_right = axes[row_idx, 1]

    for i, sub in enumerate(subdirs):
        file_path = os.path.join(home, group, sub, 'COLVAR')
        if not os.path.exists(file_path):
            continue

        try:
            # Read and optionally trim end
            data = np.genfromtxt(file_path, comments="#", dtype=float)
            if data.ndim == 1:
                data = np.atleast_2d(data)

            time = data[:, 0][:cut] if cut else data[:, 0]
            cv1 = data[:, id1][:cut] if cut else data[:, id1]
            cv2 = data[:, id2][:cut] if cut else data[:, id2]

            # Plot CV1
            if i == 0 or i == len(subdirs) - 1:
                ax_left.plot(time, cv1, color=colors[i], linewidth=0.8, label=f"{group}/{sub}")
            else:
                ax_left.plot(time, cv1, color=colors[i], linewidth=0.8)

            # Plot CV2
            if i == 0 or i == len(subdirs) - 1:
                ax_right.plot(time, cv2, color=colors[i], linewidth=0.8, label=f"{group}/{sub}")
            else:
                ax_right.plot(time, cv2, color=colors[i], linewidth=0.8)

        except Exception:
            pass

    # Titles and labels per row
    ax_left.set_title(row_labels[0])
    ax_right.set_title(row_labels[1])
    ax_left.set_ylabel(f"{group.upper()}")
    ax_left.legend(frameon=False, fontsize=8, loc="best")
    ax_right.legend(frameon=False, fontsize=8, loc="best")

# Common X label
for c in range(ncols):
    axes[-1, c].set_xlabel("Time")

# Optional overarching Y label
fig.supylabel("Collective Variables")

plt.show()
