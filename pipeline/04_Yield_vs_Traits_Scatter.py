# ============================================================
# PLOS ONE – YIELD vs TRAITS SCATTER ANALYSIS
# ============================================================
# Author: Jarvis
# Repository: Rice Trait Network Analysis
#
# Purpose
# -------
# Generate publication-ready scatter plots showing the
# relationships between grain yield and key agronomic traits.
#
# Features
# --------
# • Pearson correlation (r)
# • Linear regression fit
# • 95% confidence interval
# • Parent vs mutant color coding
# • High-resolution export (600 dpi)
# • Automatic ZIP download of figures
#
# Output
# ------
# Scatter_Yield_vs_Grain_yield_per_hill.png
# Scatter_Yield_vs_Straw_yield_per_hill.png
# Scatter_Yield_vs_Primary_branches_per_panicle.png
# Scatter_Yield_vs_Panicle_length.png
# Scatter_Yield_vs_Secondary_branches_per_panicle.png
# Scatter_Yield_vs_Filled_grains_per_panicle.png
#
# ============================================================

# ============================================================
# 1. Import libraries
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import os
import zipfile
from google.colab import files

# ============================================================
# 2. Upload dataset
# ============================================================

print("Upload dataset (CSV or Excel)")

uploaded = files.upload()

filename = list(uploaded.keys())[0]

if filename.endswith(".xlsx"):
    df = pd.read_excel(filename)
elif filename.endswith(".csv"):
    df = pd.read_csv(filename)
else:
    raise ValueError("Upload CSV or XLSX file")

print("Dataset loaded:", filename)

# ============================================================
# 3. Define parent vs mutant groups
# ============================================================

df["Group"] = np.where(
    df["Genotype"].astype(str).str.lower() == "parent",
    "Parent",
    "Mutants"
)

# ============================================================
# 4. Output directory
# ============================================================

outdir = "Yield_vs_Traits_outputs"
os.makedirs(outdir, exist_ok=True)

# ============================================================
# 5. Traits used for analysis
# ============================================================

traits = [

("Scatter_Yield_vs_Grain_yield_per_hill.png",
 "Grain yield hill-1",
 "Grain yield per hill"),

("Scatter_Yield_vs_Straw_yield_per_hill.png",
 "Straw yield hill-1",
 "Straw yield per hill"),

("Scatter_Yield_vs_Primary_branches_per_panicle.png",
 "Primary branch panicle-1",
 "Primary branches per panicle"),

("Scatter_Yield_vs_Panicle_length.png",
 "Panicle length",
 "Panicle length"),

("Scatter_Yield_vs_Secondary_branches_per_panicle.png",
 "Secondary branch panicle-1",
 "Secondary branches per panicle"),

("Scatter_Yield_vs_Filled_grains_per_panicle.png",
 "Filled grain panicle-1",
 "Filled grains per panicle")

]

yield_col = "Grain yield hill-1"

generated_files = []

# ============================================================
# 6. Generate scatter plots
# ============================================================

for fname, xcol, xlabel in traits:

    sub = df[[xcol, yield_col, "Group"]].dropna()

    x = sub[xcol].astype(float).to_numpy().ravel()
    y = sub[yield_col].astype(float).to_numpy().ravel()

    n = len(x)

    # Pearson correlation
    r = np.corrcoef(x, y)[0,1]

    t_val = r * np.sqrt((n-2) / max(1e-9, (1-r**2)))
    p = 2 * (1 - t.cdf(abs(t_val), df=max(1,n-2)))

    # Linear regression
    slope, intercept = np.polyfit(x,y,1)

    xg = np.linspace(x.min(), x.max(), 300)
    yg = slope * xg + intercept

    # Confidence interval
    yhat = slope*x + intercept
    resid = y - yhat

    s_err = np.sqrt(np.sum(resid**2) / max(1,n-2))

    xbar = np.mean(x)
    sxx = np.sum((x-xbar)**2)

    tcrit = t.ppf(0.975, df=max(1,n-2))

    ci = tcrit * s_err * np.sqrt(1/n + (xg-xbar)**2 / max(1e-9,sxx))

    # -------------------------------------------------------
    # Plot
    # -------------------------------------------------------

    plt.figure(figsize=(6.8,5.4))

    for grp, color in [("Parent","#1f77b4"),("Mutants","#ff7f0e")]:

        d = sub[sub["Group"]==grp]

        plt.scatter(
            d[xcol],
            d[yield_col],
            s=42,
            alpha=0.85,
            color=color,
            label=grp
        )

    plt.plot(xg,yg,color="#1f77b4",linewidth=2.8)

    plt.fill_between(
        xg,
        yg-ci,
        yg+ci,
        color="#9fd3a5",
        alpha=0.45
    )

    plt.xlabel(xlabel,fontsize=11)
    plt.ylabel("Grain yield hill$^{-1}$ (g)",fontsize=11)

    plt.title(
        f"Grain yield vs {xlabel}\n"
        f"Linear fit with 95% CI (r={r:.2f}, p={p:.3g})",
        fontsize=12
    )

    plt.legend(frameon=False)

    plt.tight_layout()

    outpath = os.path.join(outdir,fname)

    plt.savefig(outpath,dpi=600)

    plt.close()

    generated_files.append(outpath)

# ============================================================
# 7. Zip all figures
# ============================================================

zip_name = "Yield_vs_Traits_Figures.zip"

with zipfile.ZipFile(zip_name,"w",zipfile.ZIP_DEFLATED) as z:

    for f in generated_files:

        z.write(f)

# ============================================================
# 8. Download results
# ============================================================

files.download(zip_name)

print("Analysis complete")
print("Figures saved in:", outdir)
