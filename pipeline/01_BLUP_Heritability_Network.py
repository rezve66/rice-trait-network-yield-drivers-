# ============================================================
# BLUP HERITABILITY + TRAIT NETWORK + YIELD DRIVERS
# ============================================================
# Author: Jarvis
# Repository: Rice Trait Network Analysis
#
# Purpose
# --------
# Estimate genetic parameters and trait relationships:
#
# 1. BLUP estimation using mixed linear model (REML)
# 2. Variance components (σg² and σe²)
# 3. BLUP-based heritability (H2_BLUP)
# 4. Partial correlation network using Graphical Lasso
# 5. Trait interaction network
# 6. Yield predictors using multiple regression
#
# Output
# -------
# Table2_VarianceComponents_H2BLUP.csv
# BLUP_matrix_genotype_x_traits.csv
# Standardized_BLUP_Z.csv
# PartialCorrelation_Glasso.csv
# HubTraits_degree_centrality.csv
#
# Figures
# -------
# Fig2a_PartialCorrelation_Glasso.png
# Fig2b_TraitNetwork.png
# Fig2c_YieldPredictors_LinearModel.png
#
# All figures saved at 600 dpi.
# ============================================================

# ============================================================
# 1. Install required libraries (Colab compatible)
# ============================================================

!pip -q install statsmodels scikit-learn networkx openpyxl

# ============================================================
# 2. Import libraries
# ============================================================

import os
import re
import shutil
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.formula.api as smf
from sklearn.preprocessing import StandardScaler
from sklearn.covariance import GraphicalLassoCV
from sklearn.linear_model import LinearRegression

import networkx as nx
from google.colab import files

warnings.filterwarnings("ignore")

# ============================================================
# 3. Output directory
# ============================================================

OUTDIR = "BLUP_Network_YieldDrivers_outputs"
os.makedirs(OUTDIR, exist_ok=True)

THRESHOLD_PC = 0.20
RANDOM_SEED = 42

# ============================================================
# 4. Trait abbreviations (for plotting)
# ============================================================

abbr = {

 'Days to flowering':'DF',
 'Days to maturity':'DM',
 'Plant height':'PH',
 'Tillers per hill':'TH',
 'Effective tillers per hill':'ETH',
 'Panicle length':'PL',
 'Primary branch per panicle':'PBP',
 'Secondary branch per panicle':'SBP',
 'Flag leaf length':'FLL',
 'Filled grain per panicle':'FG',
 'Sterile grain per panicle':'SG',
 'Grain length':'GL',
 'Grain breadth':'GB',
 'Grain length-breadth ratio':'GLGB',
 '1000 grain weight':'TGW',
 'Grain yield per hill':'GYH',
 'Straw yield per hill':'SYH',
 'Harvest index':'HI'
}

def safe_abbr(trait):
    return abbr.get(trait, re.sub(r"[^A-Za-z0-9]+", "", trait)[:6])

# ============================================================
# 5. Upload dataset
# ============================================================

print("Upload Excel dataset with columns: Genotype | Replication | traits")

uploaded = files.upload()

infile = list(uploaded.keys())[0]
print("Uploaded:", infile)

df = pd.read_excel(infile)

df.columns = [c.strip() for c in df.columns]
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

assert "Genotype" in df.columns
assert "Replication" in df.columns

df["Genotype"] = df["Genotype"].astype(str)
df["Replication"] = df["Replication"].astype(str)

traits = [c for c in df.columns if c not in ["Genotype","Replication"]]

print("Traits detected:", len(traits))

# ============================================================
# 6. BLUP estimation (mixed linear model)
# ============================================================

genotypes = sorted(df["Genotype"].unique())
reps = sorted(df["Replication"].unique())
r = len(reps)

blup = pd.DataFrame(index=genotypes, columns=traits)

vc_rows = []

for t in traits:

    formula = f'Q("{t}") ~ C(Replication)'

    md = smf.mixedlm(formula, df, groups=df["Genotype"])

    try:
        m = md.fit(reml=True, method="lbfgs")
    except:
        m = md.fit(reml=True, method="powell")

    mu = float(m.fe_params.iloc[0])
    reffs = m.random_effects

    for g in genotypes:

        u = float(np.asarray(reffs.get(g,[0]))[0])
        blup.loc[g,t] = mu + u

    sigma_g2 = float(m.cov_re.iloc[0,0])
    sigma_e2 = float(m.scale)

    H2 = sigma_g2 / (sigma_g2 + sigma_e2/r)

    vc_rows.append({

        "Trait":t,
        "Trait_abbr":safe_abbr(t),
        "sigma_g2":sigma_g2,
        "sigma_e2":sigma_e2,
        "replications_r":r,
        "H2_BLUP":H2
    })

vc_df = pd.DataFrame(vc_rows).sort_values("H2_BLUP",ascending=False)

blup.to_csv(os.path.join(OUTDIR,"BLUP_matrix_genotype_x_traits.csv"))

vc_df.to_csv(os.path.join(OUTDIR,"Table2_VarianceComponents_H2BLUP.csv"),index=False)

print("BLUP estimation completed")

# ============================================================
# 7. Standardize BLUP matrix
# ============================================================

Z = pd.DataFrame(
    StandardScaler().fit_transform(blup.values),
    columns=traits,
    index=blup.index
)

Z.to_csv(os.path.join(OUTDIR,"Standardized_BLUP_Z.csv"))

# ============================================================
# 8. Graphical Lasso partial correlations
# ============================================================

gl = GraphicalLassoCV()

gl.fit(Z.values)

P = gl.precision_

d = np.sqrt(np.diag(P))

pcorr = -P / np.outer(d,d)

np.fill_diagonal(pcorr,1)

pcorr_df = pd.DataFrame(pcorr,index=traits,columns=traits)

pcorr_df.to_csv(os.path.join(OUTDIR,"PartialCorrelation_Glasso.csv"))

# ============================================================
# 9. Figure 2a — Partial correlation heatmap
# ============================================================

fig, ax = plt.subplots(figsize=(10,9))

im = ax.imshow(pcorr_df,cmap="coolwarm",vmin=-1,vmax=1)

labs = [safe_abbr(t) for t in traits]

ax.set_xticks(range(len(labs)))
ax.set_yticks(range(len(labs)))

ax.set_xticklabels(labs,rotation=45,ha="right")
ax.set_yticklabels(labs)

ax.set_title(
"Figure 2a. BLUP-based Partial Correlations (Graphical Lasso)",
fontweight="bold"
)

plt.colorbar(im,ax=ax)

plt.tight_layout()

fig.savefig(
os.path.join(OUTDIR,"Fig2a_PartialCorrelation_Glasso.png"),
dpi=600
)

plt.close()

# ============================================================
# 10. Trait interaction network
# ============================================================

G = nx.Graph()

for i in range(len(traits)):

    for j in range(i+1,len(traits)):

        w = pcorr_df.iloc[i,j]

        if abs(w) >= THRESHOLD_PC:

            G.add_edge(traits[i],traits[j],weight=w,abs_weight=abs(w))

degree = nx.degree_centrality(G)

hub_df = pd.DataFrame({

"Trait":list(degree.keys()),
"Trait_abbr":[safe_abbr(t) for t in degree.keys()],
"DegreeCentrality":list(degree.values())

}).sort_values("DegreeCentrality",ascending=False)

hub_df.to_csv(os.path.join(OUTDIR,"HubTraits_degree_centrality.csv"),index=False)

# ============================================================
# 11. Figure 2b — Network
# ============================================================

fig, ax = plt.subplots(figsize=(11,9))

pos = nx.spring_layout(G,seed=RANDOM_SEED)

cent = np.array([degree.get(n,0) for n in G.nodes()])

nodes = nx.draw_networkx_nodes(
G,pos,
node_size=700 + 3500*cent,
node_color=cent,
cmap="viridis",
ax=ax
)

pos_edges = [(u,v) for u,v,d in G.edges(data=True) if d["weight"]>0]
neg_edges = [(u,v) for u,v,d in G.edges(data=True) if d["weight"]<0]

nx.draw_networkx_edges(G,pos,edgelist=pos_edges,ax=ax)

nx.draw_networkx_edges(G,pos,edgelist=neg_edges,style="dashed",ax=ax)

for node,(x,y) in pos.items():

    ax.text(x,y,safe_abbr(node),
    ha="center",
    va="center",
    fontweight="bold")

plt.colorbar(nodes,ax=ax)

ax.axis("off")

plt.tight_layout()

fig.savefig(
os.path.join(OUTDIR,"Fig2b_TraitNetwork.png"),
dpi=600
)

plt.close()

# ============================================================
# 12. Yield predictors (Multiple regression)
# ============================================================

yield_trait = "Grain yield per hill"

assert yield_trait in Z.columns

X = Z.drop(columns=[yield_trait])
y = Z[yield_trait]

lin = LinearRegression().fit(X,y)

importance = pd.Series(np.abs(lin.coef_),index=X.columns).sort_values()

imp_df = pd.DataFrame({

"Trait":importance.index,
"Trait_abbr":[safe_abbr(t) for t in importance.index],
"AbsStdCoeff":importance.values

}).sort_values("AbsStdCoeff",ascending=False)

imp_df.to_csv(
os.path.join(OUTDIR,"YieldPredictors_LinearModel.csv"),
index=False
)

# ============================================================
# 13. Figure 2c — Yield predictors
# ============================================================

fig, ax = plt.subplots(figsize=(9,6))

ax.barh(
imp_df.sort_values("AbsStdCoeff")["Trait_abbr"],
imp_df.sort_values("AbsStdCoeff")["AbsStdCoeff"],
edgecolor="black"
)

ax.set_title(
"Figure 2c. Key Predictors of Grain Yield",
fontweight="bold"
)

ax.set_xlabel("Absolute standardized regression coefficient")

plt.tight_layout()

fig.savefig(
os.path.join(OUTDIR,"Fig2c_YieldPredictors_LinearModel.png"),
dpi=600
)

plt.close()

# ============================================================
# 14. Zip outputs
# ============================================================

zipfile = shutil.make_archive(OUTDIR,"zip",OUTDIR)

files.download(zipfile)

print("Pipeline completed successfully")
print("Outputs saved in:",OUTDIR)
