# ============================================================
# GENETIC PARAMETERS + MGIDI + ELITE MUTANT SELECTION
# ============================================================
# Author: Jarvis
# Repository: Rice Trait Network Analysis
#
# Purpose
# -------
# Perform classical quantitative genetics analysis for
# mutant rice populations and identify elite genotypes
# using the MGIDI multi-trait selection index.
#
# Methods
# -------
# 1. Genetic parameters (GCV, PCV, H², GA, GAM)
# 2. Genotype mean estimation
# 3. MGIDI multi-trait index
# 4. Elite mutant identification
# 5. Selection response estimation
# 6. Path coefficient analysis
# 7. Trait heatmap visualization
# 8. MGIDI ranking plot
#
# Outputs
# -------
# Genetic_parameters_shortform.csv
# MGIDI_scores.csv
# Top10_Elite_Mutants.csv
# Selection_response_GYH.csv
# Path_direct_effects_GYH.csv
#
# Figures
# -------
# Heatmap_Top10_GYH.png
# MGIDI_Top10.png
#
# ============================================================

# ============================================================
# 1. Import libraries
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FactorAnalysis
from sklearn.linear_model import LinearRegression
from scipy.cluster.hierarchy import linkage, leaves_list
import os
from google.colab import files

# ============================================================
# 2. Upload dataset
# ============================================================

print("Upload dataset (CSV or Excel)")

uploaded = files.upload()

file_name = list(uploaded.keys())[0]

if file_name.endswith(".csv"):
    df = pd.read_csv(file_name)
else:
    df = pd.read_excel(file_name)

print("Dataset loaded:", file_name)

# ============================================================
# 3. Output directory
# ============================================================

OUTPUT_DIR = "GeneticParameters_MGIDI_outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# 4. Trait renaming (full → short)
# ============================================================

TRAIT_MAP = {

"Days to flowering": "DF",
"Days to maturity": "DM",
"Plant height": "PH",
"Tillers hill-1": "TH",
"Effective tillers hill-1": "ETH",
"Panicle length": "PL",
"Primary branches panicle-1": "PBP",
"Secondary branches panicle-1": "SBP",
"Flag leaf length": "FLL",
"Filled grains panicle-1": "FG",
"Sterile grains panicle-1": "SGP",
"Grain length": "GL",
"Grain breadth": "GB",
"1000-grain weight": "TGW",
"Grain yield hill-1": "GYH",
"Straw yield hill-1": "SYH",
"Harvest index": "HI"

}

df = df.rename(columns={k: v for k, v in TRAIT_MAP.items() if k in df.columns})

# ============================================================
# 5. Derived trait (grain shape ratio)
# ============================================================

if "GL" in df.columns and "GB" in df.columns:

    df["GL/GB"] = df["GL"] / df["GB"]

    print("Derived trait GL/GB created")

# ============================================================
# 6. Define traits dynamically
# ============================================================

TRAITS = [c for c in df.columns if c not in ["Genotype","Replication"]]

print("Traits used:", sorted(TRAITS))

# ============================================================
# 7. Genotype means
# ============================================================

gmeans = df.groupby("Genotype")[TRAITS].mean()

# ============================================================
# 8. Genetic parameter calculation
# ============================================================

def genetic_params(trait):

    r = df["Replication"].nunique()
    g = df["Genotype"].nunique()

    grand = df[trait].mean()

    SST = ((df[trait] - grand)**2).sum()

    SSg = r * ((df.groupby("Genotype")[trait].mean() - grand)**2).sum()

    SSr = g * ((df.groupby("Replication")[trait].mean() - grand)**2).sum()

    SSe = SST - SSg - SSr

    MSg = SSg / (g-1)

    MSe = SSe / ((g-1)*(r-1))

    GV = max((MSg - MSe)/r, 0)

    PV = GV + MSe

    mean = df[trait].mean()

    GCV = np.sqrt(GV)/mean*100 if mean!=0 else np.nan

    PCV = np.sqrt(PV)/mean*100 if mean!=0 else np.nan

    H2 = GV/PV if PV>0 else np.nan

    GA = 2.06*np.sqrt(PV)*H2 if PV>0 else np.nan

    GAM = GA/mean*100 if mean!=0 else np.nan

    return [mean,GCV,PCV,H2,GA,GAM]

genetic_table = pd.DataFrame(

{t: genetic_params(t) for t in TRAITS},

index=["Mean","GCV","PCV","H2","GA","GAM"]

).T

genetic_table.to_csv(

f"{OUTPUT_DIR}/Genetic_parameters_shortform.csv"

)

print("Genetic parameter table saved")

# ============================================================
# 9. MGIDI multi-trait index
# ============================================================

LOWER_BETTER = {"DF","DM","PH","SGP"}

X = gmeans.copy()

for t in X.columns:

    if t in LOWER_BETTER:

        X[t] = -X[t]

Z = StandardScaler().fit_transform(X)

n_factors = min(5, Z.shape[1])

fa = FactorAnalysis(

n_components=n_factors,

random_state=0

)

F = fa.fit_transform(Z)

ideotype = F.max(axis=0)

mgidi = np.sqrt(((F - ideotype)**2).sum(axis=1))

mgidi = pd.Series(mgidi,index=gmeans.index).sort_values()

mgidi.to_csv(

f"{OUTPUT_DIR}/MGIDI_scores.csv"

)

print("MGIDI index calculated")

# ============================================================
# 10. Top elite mutants
# ============================================================

if "GYH" in gmeans.columns:

    top10 = gmeans["GYH"].sort_values(

        ascending=False

    ).head(10)

    elite_table = pd.DataFrame({

    "Rank":range(1,len(top10)+1),

    "Genotype":top10.index,

    "GYH":top10.values,

    "MGIDI":mgidi[top10.index].values

    })

    elite_table.to_csv(

        f"{OUTPUT_DIR}/Top10_Elite_Mutants.csv",

        index=False

    )

    print("Top elite mutants identified")

# ============================================================
# 11. Selection response
# ============================================================

if "GYH" in gmeans.columns:

    mean_pop = gmeans["GYH"].mean()

    n_sel = max(int(np.ceil(0.05*len(gmeans))),1)

    mean_sel = gmeans["GYH"].sort_values(

        ascending=False

    ).head(n_sel).mean()

    SD = mean_sel - mean_pop

    H2_yield = genetic_table.loc["GYH","H2"]

    R = SD * H2_yield

    pd.DataFrame({

    "Population_mean":[mean_pop],

    "Selected_mean":[mean_sel],

    "Selection_differential":[SD],

    "Heritability":[H2_yield],

    "Expected_response":[R]

    }).to_csv(

        f"{OUTPUT_DIR}/Selection_response_GYH.csv",

        index=False

    )

# ============================================================
# 12. Path coefficient analysis
# ============================================================

TARGET = "GYH"

PREDICTORS = ["ETH","PL","FG","TGW","PH"]

PREDICTORS = [p for p in PREDICTORS if p in gmeans.columns]

if TARGET in gmeans.columns and len(PREDICTORS) >= 2:

    Xp = StandardScaler().fit_transform(

        gmeans[PREDICTORS]

    )

    Yp = StandardScaler().fit_transform(

        gmeans[TARGET].values.reshape(-1,1)

    ).ravel()

    model = LinearRegression().fit(Xp,Yp)

    path_df = pd.DataFrame({

    "Trait":PREDICTORS,

    "Direct_effect_beta":model.coef_

    }).sort_values("Direct_effect_beta",ascending=False)

    path_df.to_csv(

        f"{OUTPUT_DIR}/Path_direct_effects_GYH.csv",

        index=False

    )

# ============================================================
# 13. Trait heatmap for elite genotypes
# ============================================================

if "GYH" in gmeans.columns:

    highlight = list(top10.index)

    H = gmeans.loc[highlight, TRAITS]

    Hz = (H - H.mean()) / H.std()

    order = leaves_list(

        linkage(Hz.T, method="average")

    )

    plt.figure(figsize=(12,5))

    plt.imshow(

        Hz.iloc[:,order],

        aspect="auto",

        cmap="viridis"

    )

    plt.yticks(

        range(len(highlight)),

        highlight

    )

    plt.xticks(

        range(len(order)),

        Hz.columns[order],

        rotation=90

    )

    plt.colorbar(label="Z-score")

    plt.title(

        "Trait heatmap (Top 10 elite mutants)"

    )

    plt.tight_layout()

    plt.savefig(

        f"{OUTPUT_DIR}/Heatmap_Top10_GYH.png",

        dpi=600

    )

    plt.close()

# ============================================================
# 14. MGIDI ranking plot
# ============================================================

plt.figure(figsize=(7,5))

top10_mgidi = mgidi.head(10).iloc[::-1]

plt.barh(

    top10_mgidi.index,

    top10_mgidi.values,

    color=plt.cm.viridis(

        np.linspace(0.2,0.9,len(top10_mgidi))

    )

)

plt.xlabel("MGIDI score (lower = better)")

plt.title("Top elite mutants based on MGIDI")

plt.tight_layout()

plt.savefig(

    f"{OUTPUT_DIR}/MGIDI_Top10.png",

    dpi=600

)

plt.close()

print("Pipeline completed successfully")
print("Outputs saved in:", OUTPUT_DIR)
