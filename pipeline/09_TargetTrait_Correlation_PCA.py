# ============================================================
# TARGET TRAIT CORRELATION + PCA ANALYSIS
# ============================================================
# Author: Jarvis
# Repository: Rice Trait Network Analysis
#
# Purpose
# -------
# Perform correlation analysis and PCA relative to a
# user-selected target trait.
#
# Features
# --------
# • Select any trait as TARGET_TRAIT
# • Correlation ranking vs target trait
# • PCA on remaining traits
# • PCA biplot visualization
# • Export loadings and eigenvalues
# • High-resolution figures (600 dpi)
#
# Outputs
# -------
# Correlation_vs_TargetTrait.png
# Correlation_Heatmap.png
# PCA_Biplot.png
#
# Tables
# ------
# TargetTrait_Correlation_Results.xlsx
# PCA_Scores.xlsx
# PCA_Loadings_All_Traits_All_PCs.xlsx
# PCA_Eigenvalues_Explained_Cumulative.xlsx
#
# ============================================================

# ============================================================
# 1. Install required library
# ============================================================

!pip install adjustText --quiet

# ============================================================
# 2. Import libraries
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from adjustText import adjust_text
from google.colab import files

# ============================================================
# 3. Plot settings
# ============================================================

sns.set(style="whitegrid", font_scale=1.2)

plt.rcParams.update({

'savefig.dpi':600,
'figure.dpi':150,
'font.size':11

})

# ============================================================
# 4. Upload dataset
# ============================================================

print("Upload dataset (Excel)")

uploaded = files.upload()

filename = list(uploaded.keys())[0]

df = pd.read_excel(filename)

print("Dataset loaded")

display(df.head())

# ============================================================
# 5. USER INPUT — SELECT TARGET TRAIT
# ============================================================

TARGET_TRAIT = "Harvest index"   # ← change this to any trait

if TARGET_TRAIT not in df.columns:

    raise ValueError(
        f"{TARGET_TRAIT} not found in dataset"
    )

print("Target trait selected:", TARGET_TRAIT)

# ============================================================
# 6. Identify numeric traits
# ============================================================

num_cols = df.select_dtypes(include=[np.number]).columns.tolist()

traits = [c for c in num_cols if c != TARGET_TRAIT]

# ============================================================
# 7. Correlation vs target trait
# ============================================================

corr_results = []

for trait in traits:

    r,p = stats.pearsonr(df[trait], df[TARGET_TRAIT])

    corr_results.append({

    'Trait':trait,
    'r':r,
    'p_value':p

    })

corr_df = pd.DataFrame(corr_results)

corr_df = corr_df.sort_values("r",ascending=False)

print("Correlation results")

display(corr_df)

# ============================================================
# 8. Create results folder
# ============================================================

os.makedirs("Results",exist_ok=True)

# ============================================================
# 9. Correlation bar plot
# ============================================================

plt.figure(figsize=(10,6))

sns.barplot(

data=corr_df,
x='r',
y='Trait',
palette='vlag',
orient='h',
edgecolor='black'

)

plt.axvline(0,color='gray',linestyle='--')

plt.title(
f"Correlation of Traits with {TARGET_TRAIT}",
fontsize=14,
weight='bold'
)

plt.xlabel("Pearson Correlation (r)")

plt.tight_layout()

plt.savefig(
"Results/Correlation_vs_TargetTrait.png",
dpi=600,
bbox_inches='tight'
)

plt.show()

# ============================================================
# 10. Correlation heatmap
# ============================================================

plt.figure(figsize=(12,8))

sns.heatmap(

df[num_cols].corr(),
annot=True,
cmap="coolwarm",
fmt=".2f",
cbar_kws={"shrink":0.8}

)

plt.title(
"Correlation Matrix of Numeric Traits",
fontsize=14,
weight='bold'
)

plt.tight_layout()

plt.savefig(
"Results/Correlation_Heatmap.png",
dpi=600,
bbox_inches='tight'
)

plt.show()

# ============================================================
# 11. PCA analysis
# ============================================================

X = df[traits].dropna()

genotypes = df.iloc[:,0]

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

pca_full = PCA()

pca_full.fit(X_scaled)

# PCA scores
pca_scores = pca_full.transform(X_scaled)[:,:2]

pca_df = pd.DataFrame({

'Genotype':genotypes,
'PC1':pca_scores[:,0],
'PC2':pca_scores[:,1],
TARGET_TRAIT:df[TARGET_TRAIT]

})

# ============================================================
# 12. PCA loadings
# ============================================================

loadings_all = pd.DataFrame(

pca_full.components_.T,
index=traits,
columns=[f"PC{i+1}" for i in range(pca_full.n_components_)]

)

print("PCA Loadings")

display(loadings_all)

# ============================================================
# 13. Eigenvalues + variance
# ============================================================

eigenvalues = pca_full.explained_variance_

explained_var = pca_full.explained_variance_ratio_

cumulative_var = np.cumsum(explained_var)

pca_variance_table = pd.DataFrame({

"PC":[f"PC{i+1}" for i in range(len(eigenvalues))],
"Eigenvalue":eigenvalues,
"Explained Variance (%)":explained_var*100,
"Cumulative Variance (%)":cumulative_var*100

})

print("PCA variance explained")

display(pca_variance_table)

# ============================================================
# 14. PCA biplot
# ============================================================

plt.figure(figsize=(10,8))

scatter = plt.scatter(

pca_df['PC1'],
pca_df['PC2'],
c=pca_df[TARGET_TRAIT],
cmap='RdYlGn_r',
s=120,
edgecolor='black'

)

texts = []

for _,row in pca_df.iterrows():

    texts.append(

    plt.text(
        row['PC1']+0.05,
        row['PC2']+0.05,
        row['Genotype'],
        fontsize=10,
        fontweight='bold'
    ))

arrow_scale = 3.0

for trait in traits:

    plt.arrow(

    0,
    0,
    loadings_all.loc[trait,'PC1']*arrow_scale,
    loadings_all.loc[trait,'PC2']*arrow_scale,

    color='steelblue',
    alpha=0.7,
    head_width=0.05,
    linewidth=2

    )

    texts.append(

    plt.text(

    loadings_all.loc[trait,'PC1']*arrow_scale*1.15,
    loadings_all.loc[trait,'PC2']*arrow_scale*1.15,
    trait,
    color='blue',
    fontsize=10,
    weight='bold'

    ))

adjust_text(texts)

plt.axhline(0,color='gray')
plt.axvline(0,color='gray')

plt.xlabel(
f"PC1 ({explained_var[0]*100:.1f}% variance)"
)

plt.ylabel(
f"PC2 ({explained_var[1]*100:.1f}% variance)"
)

plt.title(
"PCA Biplot — Genotypes & Trait Loadings",
fontsize=15,
weight='bold'
)

cbar = plt.colorbar(scatter)

cbar.set_label(TARGET_TRAIT)

plt.grid(True,linestyle='--',alpha=0.5)

plt.tight_layout()

plt.savefig(
"Results/PCA_Biplot.png",
dpi=600,
bbox_inches='tight'
)

plt.show()

# ============================================================
# 15. Save tables
# ============================================================

corr_df.to_excel(
"Results/TargetTrait_Correlation_Results.xlsx",
index=False
)

pca_df.to_excel(
"Results/PCA_Scores.xlsx",
index=False
)

loadings_all.to_excel(
"Results/PCA_Loadings_All_Traits_All_PCs.xlsx"
)

pca_variance_table.to_excel(
"Results/PCA_Eigenvalues_Explained_Cumulative.xlsx",
index=False
)

# ============================================================
# 16. Zip results
# ============================================================

print("Files generated in Results folder")

!zip -r Results.zip Results > /dev/null

files.download("Results.zip")

print("Analysis completed successfully")
