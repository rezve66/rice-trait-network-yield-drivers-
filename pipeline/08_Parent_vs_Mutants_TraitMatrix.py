# ============================================================
# PARENT vs HIGH / LOW YIELD MUTANTS TRAIT MATRIX
# ============================================================
# Author: Jarvis
# Repository: Rice Trait Network Analysis
#
# Purpose
# -------
# Compare parent genotype with high-yield and low-yield mutants
# using a multi-trait correlation and density matrix.
#
# Visualization layout
# --------------------
# Diagonal        : Kernel density distributions
# Lower triangle  : Scatter plots
# Upper triangle  : Correlation statistics
#
# Groups
# ------
# Parent
# High-yield mutants
# Low-yield mutants
# Other mutants
#
# Output
# ------
# parent_high_low_corrmatrix_abbr_legend_top_600dpi.png
#
# ============================================================

# ============================================================
# 1. Install required package (Colab compatible)
# ============================================================

!pip -q install openpyxl

# ============================================================
# 2. Import libraries
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import matplotlib.lines as mlines

from google.colab import files

# ============================================================
# 3. Upload dataset
# ============================================================

print("Upload Excel dataset")

uploaded = files.upload()

excel_file = list(uploaded.keys())[0]

df = pd.read_excel(excel_file)

print("Dataset loaded:", excel_file)

# ============================================================
# 4. USER SETTINGS
# ============================================================

yield_col = "Grain yield per hill"

TOP_N = 4
BOTTOM_N = 4

PARENT_NAME = "Parent"

traits_map = {

"Harvest index":"HI",
"Straw yield per hill":"SYH",
"Panicle length":"PL",
"Tillers per hill":"TH",
"Primary branch per panicle":"PBP",
"Secondary branch per panicle":"SBP",
"Grain length-breadth ratio":"GLGB"

}

group_colors = {

"Parent":"black",
"High-yield":"#00A6D6",
"Low-yield":"#F05A64",
"Mid":"#9e9e9e"

}

# ============================================================
# 5. Validate dataset
# ============================================================

required_cols = ["Genotype", yield_col] + list(traits_map.keys())

missing = [c for c in required_cols if c not in df.columns]

if missing:

    raise ValueError(f"Missing required columns: {missing}")

traits = [t for t in traits_map.keys() if t in df.columns]

sub = df[["Genotype"] + traits].copy()

# ============================================================
# 6. Identify mutant groups
# ============================================================

means = df.groupby("Genotype")[yield_col].mean().sort_values(ascending=False)

if PARENT_NAME not in means.index:

    raise ValueError(f"Parent genotype '{PARENT_NAME}' not found")

mut_means = means.drop(PARENT_NAME)

top_mutants = mut_means.head(TOP_N).index.tolist()
bottom_mutants = mut_means.tail(BOTTOM_N).index.tolist()

def group_label(g):

    if g == PARENT_NAME:
        return "Parent"

    elif g in top_mutants:
        return "High-yield"

    elif g in bottom_mutants:
        return "Low-yield"

    else:
        return "Mid"

sub["Group"] = sub["Genotype"].map(group_label)

print("Top mutants:", top_mutants)
print("Bottom mutants:", bottom_mutants)

# ============================================================
# 7. Helper functions
# ============================================================

def corr_p(x, y):

    x = np.asarray(x)
    y = np.asarray(y)

    mask = ~(np.isnan(x) | np.isnan(y))

    if mask.sum() < 3:
        return np.nan, np.nan

    r, p = st.pearsonr(x[mask], y[mask])

    return r, p

def stars(p):

    if np.isnan(p): return ""
    if p < 0.001: return "***"
    if p < 0.01: return "**"
    if p < 0.05: return "*"
    return ""

# ============================================================
# 8. Create matrix plot
# ============================================================

k = len(traits)

fig, axes = plt.subplots(k, k, figsize=(16,14))

plt.subplots_adjust(wspace=0.07, hspace=0.07, top=0.85)

for i, ytrait in enumerate(traits):

    for j, xtrait in enumerate(traits):

        ax = axes[i,j]

        ax.set_facecolor("#f6f6f6")

        ax.grid(True, linewidth=0.25, alpha=0.5)

        # Diagonal (density)
        if i == j:

            for g in ["High-yield","Low-yield","Parent"]:

                vals = sub.loc[sub["Group"]==g, ytrait].dropna().values

                if len(vals) < 2:
                    continue

                mn = np.nanmin(sub[ytrait])
                mx = np.nanmax(sub[ytrait])

                xs = np.linspace(mn,mx,200)

                kde = st.gaussian_kde(vals)

                ax.fill_between(xs, kde(xs), alpha=0.45, color=group_colors[g])

            ax.set_yticks([])

        # Lower triangle (scatter)
        elif i > j:

            for g in ["Mid","Low-yield","High-yield","Parent"]:

                d = sub[sub["Group"]==g]

                ax.scatter(

                    d[xtrait],
                    d[ytrait],

                    s=20 if g!="Parent" else 38,

                    alpha=0.9,

                    c=group_colors[g],

                    edgecolors="none"

                )

        # Upper triangle (correlation)
        else:

            r_all, p_all = corr_p(sub[xtrait], sub[ytrait])

            r_high, p_high = corr_p(
                sub.loc[sub["Group"]=="High-yield",xtrait],
                sub.loc[sub["Group"]=="High-yield",ytrait]
            )

            r_low, p_low = corr_p(
                sub.loc[sub["Group"]=="Low-yield",xtrait],
                sub.loc[sub["Group"]=="Low-yield",ytrait]
            )

            ax.text(
                0.5,0.72,
                f"Corr: {r_all:.3f}{stars(p_all)}",
                ha="center",
                transform=ax.transAxes,
                fontsize=10,
                color="#404040",
                fontweight="bold"
            )

            ax.text(
                0.5,0.48,
                f"High: {r_high:.3f}{stars(p_high)}",
                ha="center",
                transform=ax.transAxes,
                fontsize=10,
                color=group_colors["High-yield"]
            )

            ax.text(
                0.5,0.24,
                f"Low : {r_low:.3f}{stars(p_low)}",
                ha="center",
                transform=ax.transAxes,
                fontsize=10,
                color=group_colors["Low-yield"]
            )

            ax.set_xticks([])
            ax.set_yticks([])

        if i < k-1:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel(traits_map[xtrait], rotation=45, fontsize=11, fontweight="bold")

        if j > 0:
            ax.set_yticklabels([])
        else:
            ax.set_ylabel(traits_map[ytrait], fontsize=11, fontweight="bold")

# ============================================================
# 9. Title
# ============================================================

fig.suptitle(
"Parent reference vs High- and Low-yield Mutants",
fontsize=16
)

# ============================================================
# 10. Legend
# ============================================================

handles = [

mlines.Line2D([],[],color=group_colors["Parent"],marker='o',linestyle='None',label="Parent"),

mlines.Line2D([],[],color=group_colors["High-yield"],marker='o',linestyle='None',label=f"High-yield mutants (Top {TOP_N})"),

mlines.Line2D([],[],color=group_colors["Low-yield"],marker='o',linestyle='None',label=f"Low-yield mutants (Bottom {BOTTOM_N})"),

mlines.Line2D([],[],color=group_colors["Mid"],marker='o',linestyle='None',label="Other mutants")

]

fig.legend(
handles=handles,
loc="upper center",
bbox_to_anchor=(0.5,0.92),
ncol=4,
frameon=True
)

# ============================================================
# 11. Save figure
# ============================================================

out_png = "parent_high_low_corrmatrix_abbr_legend_top_600dpi.png"

plt.savefig(out_png, dpi=600, bbox_inches="tight")

plt.show()

files.download(out_png)

print("Figure saved:", out_png)
