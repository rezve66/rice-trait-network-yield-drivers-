# ============================================================
# HARVEST INDEX TRAIT CORRELATION MATRIX
# ============================================================
# Author: Jarvis
# Repository: Rice Trait Network Analysis
#
# Purpose
# -------
# Generate a modern triangular correlation matrix showing
# relationships among key Harvest Index–associated traits.
#
# Visualization layout
# --------------------
# Diagonal        : Trait distributions (histograms)
# Lower triangle  : Scatter plots
# Upper triangle  : Pearson correlations + significance
#
# Traits analyzed
# ----------------
# Harvest Index
# Grain yield per hill
# Straw yield per hill
# Thousand grain weight
# Plant height
# Panicle length
# Filled grains per panicle
#
# Output
# ------
# Figure_Correlation_7_HI_Traits_Modern.png (600 dpi)
#
# ============================================================

# ============================================================
# 1. Install required packages (Colab compatible)
# ============================================================

!pip install pandas numpy matplotlib scipy openpyxl

# ============================================================
# 2. Import libraries
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from google.colab import files

# ============================================================
# 3. Upload dataset
# ============================================================

print("Upload Excel (.xlsx) dataset")

uploaded = files.upload()

file_name = list(uploaded.keys())[0]

df = pd.read_excel(file_name)

print("Dataset loaded:", file_name)
print("Dataset shape:", df.shape)

# ============================================================
# 4. Select HI-associated traits
# ============================================================

traits = [

"Harvest Index",
"GYH",
"SYH",
"TGW",
"PH",
"PL",
"FG"

]

# Check if traits exist
missing = [t for t in traits if t not in df.columns]

if missing:
    raise ValueError(f"Missing required traits: {missing}")

data = df[traits]

print("Traits used in analysis:")
for t in traits:
    print("-", t)

# ============================================================
# 5. Plot configuration
# ============================================================

plt.style.use("ggplot")

n = len(traits)

fig, axes = plt.subplots(
    n,
    n,
    figsize=(2.8*n, 2.8*n)
)

scatter_color = "#2C7FB8"
hist_color = "#7FCDBB"
pos_color = "#1A9850"
neg_color = "#D7301F"

# ============================================================
# 6. Generate matrix plots
# ============================================================

for i in range(n):

    for j in range(n):

        ax = axes[i,j]

        # Diagonal: histogram
        if i == j:

            ax.hist(
                data.iloc[:,i],
                bins=22,
                density=True,
                color=hist_color,
                edgecolor="white"
            )

            ax.set_title(
                traits[i],
                fontsize=15,
                fontweight="bold",
                pad=6
            )

        # Lower triangle: scatter
        elif i > j:

            ax.scatter(
                data.iloc[:,j],
                data.iloc[:,i],
                s=22,
                alpha=0.75,
                color=scatter_color
            )

        # Upper triangle: correlation text
        else:

            r,p = pearsonr(
                data.iloc[:,j],
                data.iloc[:,i]
            )

            stars = "***" if p < 0.001 else \
                    "**" if p < 0.01 else \
                    "*" if p < 0.05 else ""

            ax.text(
                0.5,
                0.58,
                "Corr:",
                ha="center",
                va="center",
                fontsize=13,
                color="gray",
                transform=ax.transAxes
            )

            ax.text(
                0.5,
                0.38,
                f"{r:.2f}{stars}",
                ha="center",
                va="center",
                fontsize=17,
                fontweight="bold",
                color=pos_color if r>=0 else neg_color,
                transform=ax.transAxes
            )

            ax.set_facecolor("#F7F7F7")

            ax.axis("off")

        ax.tick_params(
            left=False,
            bottom=False,
            labelleft=False,
            labelbottom=False
        )

# ============================================================
# 7. Add figure title
# ============================================================

fig.suptitle(

"Phenotypic correlation among seven Harvest Index–associated traits",

fontsize=24,
fontweight="bold",
y=0.995

)

plt.tight_layout(rect=[0,0,1,0.97])

# ============================================================
# 8. Save high-resolution figure
# ============================================================

output_file = "Figure_Correlation_7_HI_Traits_Modern.png"

plt.savefig(
    output_file,
    dpi=600,
    bbox_inches="tight"
)

plt.show()

# ============================================================
# 9. Download output
# ============================================================

files.download(output_file)

print("Figure generated successfully")
print("Saved as:", output_file)
