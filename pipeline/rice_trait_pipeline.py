"""
Rice Trait Network and Yield Driver Analysis Pipeline

Author: Md Rezve
Year: 2026

This pipeline performs:

1. BLUP estimation using mixed models
2. Variance component analysis
3. Broad-sense heritability estimation
4. Graphical Lasso partial correlation network
5. Trait interaction network visualization
6. Yield predictor modeling
7. Random forest feature importance
8. SHAP explainable machine learning
9. MGIDI multi-trait selection index
10. Publication-ready figure generation
"""
# ============================================================
# GENOTYPE–TRAIT MULTI-ANALYSIS PIPELINE
# ============================================================
# Author: Jarvis
# Target journals: PLOS ONE / Scientific Reports
# Platform: Google Colab / Python
# ============================================================

# ============================================================
# 1. INSTALL DEPENDENCIES
# ============================================================

!pip install statsmodels scikit-learn networkx shap seaborn openpyxl

# ============================================================
# 2. IMPORT LIBRARIES
# ============================================================

import os
import warnings
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

from sklearn.preprocessing import StandardScaler
from sklearn.covariance import GraphicalLassoCV
from sklearn.linear_model import LinearRegression
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import r2_score
from sklearn.decomposition import FactorAnalysis

import shap
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

# ============================================================
# 3. UPLOAD DATASET
# ============================================================

from google.colab import files
uploaded = files.upload()

file_name = list(uploaded.keys())[0]

if file_name.endswith(".xlsx"):
    df = pd.read_excel(file_name)
else:
    df = pd.read_csv(file_name)

df.columns = df.columns.str.strip()

print("Dataset shape:", df.shape)

# ============================================================
# 4. BASIC DATA STRUCTURE
# ============================================================

GENOTYPE_COL = "Genotype"
REPLICATION_COL = "Replication"
YIELD_TRAIT = "Grain yield per hill"

traits = [c for c in df.columns if c not in [GENOTYPE_COL, REPLICATION_COL]]

genotypes = df[GENOTYPE_COL].unique()
replications = df[REPLICATION_COL].unique()

print("Traits detected:", len(traits))

# ============================================================
# 5. OUTPUT DIRECTORY
# ============================================================

OUTDIR = "analysis_outputs"
os.makedirs(OUTDIR, exist_ok=True)

# ============================================================
# 6. BLUP ESTIMATION
# ============================================================

print("Running BLUP estimation...")

blup = pd.DataFrame(index=genotypes, columns=traits)

for trait in traits:

    formula = f'Q("{trait}") ~ C({REPLICATION_COL})'

    md = smf.mixedlm(
        formula,
        df,
        groups=df[GENOTYPE_COL]
    )

    m = md.fit()

    mu = m.fe_params[0]

    for g in genotypes:

        u = float(np.asarray(m.random_effects.get(g, [0]))[0])

        blup.loc[g, trait] = mu + u

blup.to_csv(f"{OUTDIR}/BLUP_matrix.csv")

print("BLUP matrix saved")

# ============================================================
# 7. STANDARDIZATION
# ============================================================

scaler = StandardScaler()

Z = pd.DataFrame(
    scaler.fit_transform(blup),
    columns=blup.columns,
    index=blup.index
)

# ============================================================
# 8. GRAPHICAL LASSO PARTIAL CORRELATION
# ============================================================

print("Estimating partial correlation network...")

gl = GraphicalLassoCV()
gl.fit(Z.values)

P = gl.precision_

d = np.sqrt(np.diag(P))

pcorr = -P / np.outer(d, d)

np.fill_diagonal(pcorr, 1)

pcorr_df = pd.DataFrame(
    pcorr,
    index=traits,
    columns=traits
)

pcorr_df.to_csv(f"{OUTDIR}/partial_correlation_matrix.csv")

# ============================================================
# 9. PARTIAL CORRELATION HEATMAP
# ============================================================

plt.figure(figsize=(10,9))

sns.heatmap(
    pcorr_df,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

plt.title("BLUP-based Partial Correlation Network")

plt.savefig(
    f"{OUTDIR}/partial_corr_heatmap.png",
    dpi=600
)

plt.close()

# ============================================================
# 10. TRAIT NETWORK
# ============================================================

G = nx.Graph()

for i in range(len(traits)):
    for j in range(i+1,len(traits)):

        r = pcorr_df.iloc[i,j]

        if abs(r) >= 0.20:
            G.add_edge(
                traits[i],
                traits[j],
                weight=r
            )

pos = nx.spring_layout(G,seed=42)

plt.figure(figsize=(10,9))

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="skyblue",
    node_size=2000
)

plt.title("Trait Interaction Network")

plt.savefig(
    f"{OUTDIR}/trait_network.png",
    dpi=600
)

plt.close()

# ============================================================
# 11. YIELD DRIVER MODEL
# ============================================================

print("Estimating yield predictors...")

X = Z.drop(columns=[YIELD_TRAIT])

y = Z[YIELD_TRAIT]

model = LinearRegression()

model.fit(X,y)

importance = pd.Series(
    np.abs(model.coef_),
    index=X.columns
).sort_values(ascending=False)

importance.to_csv(
    f"{OUTDIR}/yield_predictors.csv"
)

# ============================================================
# 12. PLS REGRESSION
# ============================================================

pls = PLSRegression(n_components=5)

X_scaled = scaler.fit_transform(X)

y_pred = cross_val_predict(
    pls,
    X_scaled,
    y,
    cv=5
)

print("PLS R2:", r2_score(y,y_pred))

# ============================================================
# 13. RANDOM FOREST IMPORTANCE
# ============================================================

rf = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

rf.fit(X,y)

rf_imp = pd.Series(
    rf.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

rf_imp.to_csv(
    f"{OUTDIR}/rf_importance.csv"
)

# ============================================================
# 14. SHAP ANALYSIS
# ============================================================

gb = GradientBoostingRegressor()

gb.fit(X,y)

explainer = shap.Explainer(gb,X)

shap_values = explainer(X)

shap.plots.bar(shap_values)

plt.savefig(
    f"{OUTDIR}/shap_importance.png",
    dpi=600
)

plt.close()

# ============================================================
# 15. MGIDI MULTI-TRAIT INDEX
# ============================================================

print("Computing MGIDI index...")

gmeans = df.groupby(GENOTYPE_COL)[traits].mean()

Zg = StandardScaler().fit_transform(gmeans)

fa = FactorAnalysis(
    n_components=min(5,len(traits))
)

F = fa.fit_transform(Zg)

ideotype = F.max(axis=0)

mgidi = np.sqrt(
    ((F - ideotype)**2).sum(axis=1)
)

mgidi = pd.Series(
    mgidi,
    index=gmeans.index
).sort_values()

mgidi.to_csv(
    f"{OUTDIR}/MGIDI_scores.csv"
)

# ============================================================
# 16. PIPELINE FINISHED
# ============================================================

print("Analysis completed successfully")

print("Results saved to:", OUTDIR)
