# ===============================================================
# TRAIT NETWORK + MACHINE LEARNING ANALYSIS
# ===============================================================
# Author: Md Rezve
# Repository: Rice Trait Network Analysis
#
# Purpose
# -------
# Analyze trait relationships and identify predictors of
# Harvest Index (HI) using statistical and machine learning tools.
#
# Methods implemented
# -------------------
# 1. Trait correlation matrix
# 2. Hierarchical clustermap
# 3. Trait interaction networks
# 4. Partial Least Squares regression (PLS)
# 5. Variable Importance in Projection (VIP)
# 6. Random Forest feature importance
# 7. Gradient Boosting + SHAP interpretation
# 8. Z-score genotype heatmap
#
# Target trait
# ------------
# HARVEST_INDEX
#
# Outputs
# -------
# trait_clustermap.png
# trait_network.png
# strong_trait_network.png
# pls_hi_predicted_vs_actual.png
# zscore_heatmap.png
# rf_feature_importance.png
# shap_feature_importance.png
#
# ===============================================================

# ===============================================================
# 1. Install required packages (Colab compatible)
# ===============================================================

!pip install pandas numpy seaborn matplotlib networkx scikit-learn shap openpyxl

# ===============================================================
# 2. Import libraries
# ===============================================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import r2_score

import shap

from google.colab import files

# ===============================================================
# 3. Upload dataset
# ===============================================================

print("Upload Excel dataset")

uploaded = files.upload()

file_name = list(uploaded.keys())[0]

df = pd.read_excel(file_name)

# ===============================================================
# 4. Clean column names
# ===============================================================

df.columns = df.columns.str.strip()
df.columns = df.columns.str.replace('\s+', '_', regex=True)
df.columns = df.columns.str.upper()

print("Columns detected:")
print(df.columns)

# ===============================================================
# 5. Define dataset structure
# ===============================================================

GENOTYPE_COL = 'GENOTYPE'
TARGET_COL = 'HARVEST_INDEX'

if TARGET_COL not in df.columns:
    raise ValueError(f"{TARGET_COL} not found in dataset")

df = df.dropna()

trait_cols = [c for c in df.columns if c not in [GENOTYPE_COL, TARGET_COL]]

X = df[trait_cols]
y = df[TARGET_COL]

print("Number of predictor traits:", len(trait_cols))

# ===============================================================
# 6. Create output directory
# ===============================================================

output_folder = "TraitNetwork_ML_outputs"
os.makedirs(output_folder, exist_ok=True)

# ===============================================================
# 7. Correlation clustermap
# ===============================================================

corr = X.corr()

sns.clustermap(
    corr,
    cmap="vlag",
    annot=True,
    linewidths=0.5,
    figsize=(12,10)
)

plt.title("Trait Correlation Clustermap")

plt.savefig(
    f"{output_folder}/trait_clustermap.png",
    dpi=600
)

plt.show()

# ===============================================================
# 8. Trait interaction network (|r| > 0.6)
# ===============================================================

G = nx.Graph()

for t in trait_cols:
    G.add_node(t)

for i in trait_cols:
    for j in trait_cols:

        if i != j and abs(corr.loc[i, j]) > 0.6:

            G.add_edge(i, j, weight=corr.loc[i, j])

plt.figure(figsize=(10,10))

pos = nx.spring_layout(G, seed=42)

weights = [abs(G[u][v]['weight']) * 5 for u, v in G.edges()]

nx.draw(
    G,
    pos,
    with_labels=True,
    width=weights,
    node_color='skyblue',
    edge_color='gray',
    node_size=1500
)

plt.title("Trait Network (|r| > 0.6)")

plt.savefig(
    f"{output_folder}/trait_network.png",
    dpi=600
)

plt.show()

# ===============================================================
# 9. PLS regression
# ===============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

pls = PLSRegression(
    n_components=min(5, len(trait_cols))
)

pls.fit(X_scaled, y)

y_pred = cross_val_predict(pls, X_scaled, y, cv=5)

print("PLS R²:", r2_score(y, y_pred))

# ===============================================================
# 10. VIP score calculation
# ===============================================================

def calculate_vip(pls_model):

    t = pls_model.x_scores_
    w = pls_model.x_weights_
    q = pls_model.y_loadings_

    p, h = w.shape

    vip = np.zeros((p,))

    s = np.sum((t**2) @ (q**2).T, axis=0)

    total_s = np.sum(s)

    for i in range(p):

        vip[i] = np.sqrt(
            p * np.sum((w[i,:]**2) * s) / total_s
        )

    return vip

vip_scores = calculate_vip(pls)

vip_df = pd.DataFrame({

    'Trait': trait_cols,
    'VIP': vip_scores

}).sort_values('VIP', ascending=False)

print("VIP Scores")

print(vip_df)

# ===============================================================
# 11. PLS predicted vs observed plot
# ===============================================================

plt.figure(figsize=(6,6))

sns.scatterplot(
    x=y,
    y=y_pred
)

plt.plot(
    [y.min(), y.max()],
    [y.min(), y.max()],
    'r--'
)

plt.xlabel("Observed Harvest Index")
plt.ylabel("Predicted Harvest Index")

plt.title("PLS: Predicted vs Observed")

plt.savefig(
    f"{output_folder}/pls_hi_predicted_vs_actual.png",
    dpi=600
)

plt.show()

# ===============================================================
# 12. Z-score genotype heatmap
# ===============================================================

Xz = pd.DataFrame(

    StandardScaler().fit_transform(X),

    columns=trait_cols,
    index=df[GENOTYPE_COL]

)

plt.figure(figsize=(14,6))

sns.heatmap(
    Xz,
    cmap="coolwarm",
    annot=False
)

plt.title("Z-Score Heatmap of Traits per Genotype")

plt.savefig(
    f"{output_folder}/zscore_heatmap.png",
    dpi=600
)

plt.show()

# ===============================================================
# 13. Strong correlation network (|r| > 0.7)
# ===============================================================

G2 = nx.Graph()

for i in trait_cols:

    for j in trait_cols:

        if i != j and abs(corr.loc[i, j]) > 0.7:

            color = 'green' if corr.loc[i, j] > 0 else 'red'

            G2.add_edge(
                i,
                j,
                weight=abs(corr.loc[i, j]),
                color=color
            )

plt.figure(figsize=(10,10))

pos = nx.spring_layout(G2, seed=42)

colors = [G2[u][v]['color'] for u, v in G2.edges()]

weights = [G2[u][v]['weight'] * 5 for u, v in G2.edges()]

nx.draw(
    G2,
    pos,
    with_labels=True,
    edge_color=colors,
    width=weights,
    node_color='lightblue',
    node_size=1500
)

plt.title("Strong Trait Correlation Network (|r| > 0.7)")

plt.savefig(
    f"{output_folder}/strong_trait_network.png",
    dpi=600
)

plt.show()

# ===============================================================
# 14. Random Forest feature importance
# ===============================================================

rf = RandomForestRegressor(

    n_estimators=300,
    max_depth=5,
    random_state=42

)

rf.fit(X, y)

rf_imp = pd.DataFrame({

    'Trait': trait_cols,
    'Importance': rf.feature_importances_

}).sort_values('Importance', ascending=False)

plt.figure(figsize=(8,6))

sns.barplot(
    data=rf_imp,
    x='Importance',
    y='Trait'
)

plt.title("Random Forest Feature Importance (HI)")

plt.savefig(
    f"{output_folder}/rf_feature_importance.png",
    dpi=600
)

plt.show()

# ===============================================================
# 15. Gradient Boosting + SHAP interpretation
# ===============================================================

gb = GradientBoostingRegressor(

    n_estimators=300,
    max_depth=3,
    random_state=42

)

gb.fit(X, y)

explainer = shap.Explainer(gb, X)

shap_values = explainer(X)

shap.plots.bar(shap_values, show=False)

plt.savefig(
    f"{output_folder}/shap_feature_importance.png",
    dpi=600
)

plt.show()

print("Analysis complete")

print("All outputs saved in:", output_folder)
