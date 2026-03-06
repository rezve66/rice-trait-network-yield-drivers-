# ============================================================
# HARVEST INDEX RESPONSE SURFACE ANALYSIS
# ============================================================
# Author: Jarvis
# Repository: Rice Trait Network Analysis
#
# Purpose
# -------
# Visualize how two agronomic traits jointly influence
# Harvest Index (HI) using a response surface model.
#
# Methods
# -------
# • Data interpolation (scipy griddata)
# • 3D response surface visualization
# • 2D contour heatmap
#
# Traits analyzed
# ---------------
# X-axis : Straw yield per hill
# Y-axis : Filled grains per panicle
# Z-axis : Harvest index
#
# Outputs
# -------
# HI_ResponseSurface_SYH_FG.png
# HI_ResponseSurface_SYH_FG.pdf
#
# Both exported at publication quality (600 dpi)
# ============================================================

# ============================================================
# 1. Import libraries
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from google.colab import files

# ============================================================
# 2. Upload dataset
# ============================================================

print("Upload dataset (CSV or Excel)")

uploaded = files.upload()

file_name = list(uploaded.keys())[0]

# ============================================================
# 3. Load dataset
# ============================================================

if file_name.endswith(".csv"):
    df = pd.read_csv(file_name)

elif file_name.endswith((".xlsx", ".xls")):
    df = pd.read_excel(file_name)

else:
    raise ValueError("Unsupported file format")

print("Dataset loaded successfully")
print("Available columns:")
print(df.columns)

# ============================================================
# 4. Define variables
# ============================================================

X_COL = "Straw yield per hill"
Y_COL = "Filled grain per panicle"
Z_COL = "Harvest index"

for col in [X_COL, Y_COL, Z_COL]:

    if col not in df.columns:

        raise ValueError(f"Column '{col}' not found in dataset")

x = df[X_COL].values
y = df[Y_COL].values
z = df[Z_COL].values

# ============================================================
# 5. Create interpolation grid
# ============================================================

xi = np.linspace(x.min(), x.max(), 40)
yi = np.linspace(y.min(), y.max(), 40)

X, Y = np.meshgrid(xi, yi)

Z = griddata(

    (x, y),
    z,
    (X, Y),
    method='linear'

)

# ============================================================
# 6. Generate plots
# ============================================================

fig = plt.figure(figsize=(14, 6))

# ------------------------------------------------------------
# 3D Response Surface
# ------------------------------------------------------------

ax1 = fig.add_subplot(121, projection='3d')

surface = ax1.plot_surface(

    X,
    Y,
    Z,

    cmap='viridis',
    edgecolor='none',
    alpha=0.95

)

ax1.set_xlabel("Straw yield per hill (g)")
ax1.set_ylabel("Filled grains per panicle")
ax1.set_zlabel("Harvest index")

ax1.set_title("3D Response Surface of Harvest Index")

fig.colorbar(surface, ax=ax1, shrink=0.6, label="Harvest index")

# ------------------------------------------------------------
# Heatmap / Contour Plot
# ------------------------------------------------------------

ax2 = fig.add_subplot(122)

contour = ax2.contourf(

    X,
    Y,
    Z,

    levels=20,
    cmap="viridis"

)

fig.colorbar(contour, ax=ax2, label="Harvest index")

ax2.set_xlabel("Straw yield per hill (g)")
ax2.set_ylabel("Filled grains per panicle")

ax2.set_title("Heatmap of Harvest Index")

plt.tight_layout()

# ============================================================
# 7. Save high-resolution figures
# ============================================================

plt.savefig(

    "HI_ResponseSurface_SYH_FG.png",

    dpi=600,
    bbox_inches="tight"

)

plt.savefig(

    "HI_ResponseSurface_SYH_FG.pdf",

    bbox_inches="tight"

)

plt.show()

print("Figures saved successfully")
print("✔ HI_ResponseSurface_SYH_FG.png")
print("✔ HI_ResponseSurface_SYH_FG.pdf")
