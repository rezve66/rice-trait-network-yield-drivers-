{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Rice Trait Genetic Analysis Pipeline\n",
    "\n",
    "## BLUP • Trait Networks • Machine Learning • MGIDI Selection\n",
    "\n",
    "Author: Jarvis\n",
    "\n",
    "---\n",
    "\n",
    "This notebook performs a complete quantitative genetics and machine learning analysis for rice mutant populations.\n",
    "\n",
    "The pipeline includes:\n",
    "\n",
    "1. BLUP estimation\n",
    "2. Heritability calculation\n",
    "3. Trait interaction networks\n",
    "4. Machine learning trait prediction\n",
    "5. MGIDI multi-trait selection index\n",
    "6. Elite genotype identification\n",
    "\n",
    "---\n",
    "\n",
    "## Input Data Format\n",
    "\n",
    "Dataset must contain columns:\n",
    "\n",
    "- Genotype\n",
    "- Replication\n",
    "- Traits\n",
    "\n",
    "Example traits:\n",
    "\n",
    "- Days to flowering\n",
    "- Days to maturity\n",
    "- Plant height\n",
    "- Tillers per hill\n",
    "- Panicle length\n",
    "- Filled grain per panicle\n",
    "- Grain yield per hill\n",
    "- Straw yield per hill\n",
    "- Harvest index\n",
    "\n",
    "---"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 1 — Install Required Libraries\n",
    "\n",
    "This installs all required packages for the analysis."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "!pip install pandas numpy seaborn matplotlib networkx scikit-learn statsmodels shap openpyxl"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 2 — Import Libraries"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import networkx as nx\n",
    "import statsmodels.formula.api as smf\n",
    "\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.covariance import GraphicalLassoCV\n",
    "from sklearn.linear_model import LinearRegression\n",
    "from sklearn.cross_decomposition import PLSRegression\n",
    "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n",
    "\n",
    "import shap\n",
    "import os"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 3 — Upload Dataset"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from google.colab import files\n",
    "\n",
    "uploaded = files.upload()\n",
    "file_name = list(uploaded.keys())[0]\n",
    "\n",
    "df = pd.read_excel(file_name)\n",
    "\n",
    "print(df.head())"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 4 — BLUP Estimation\n",
    "\n",
    "BLUP (Best Linear Unbiased Prediction) estimates genotype effects while accounting for replication effects."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "traits = [c for c in df.columns if c not in ['Genotype','Replication']]\n",
    "\n",
    "genotypes = sorted(df['Genotype'].unique())\n",
    "\n",
    "blup = pd.DataFrame(index=genotypes, columns=traits)\n",
    "\n",
    "for t in traits:\n",
    "\n",
    "    model = smf.mixedlm(\n",
    "        f'Q(\"{t}\") ~ C(Replication)',\n",
    "        df,\n",
    "        groups=df['Genotype']\n",
    "    )\n",
    "\n",
    "    result = model.fit()\n",
    "\n",
    "    mu = result.fe_params[0]\n",
    "\n",
    "    reffs = result.random_effects\n",
    "\n",
    "    for g in genotypes:\n",
    "        u = float(np.asarray(reffs.get(g,[0]))[0])\n",
    "        blup.loc[g,t] = mu + u\n",
    "\n",
    "blup.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 5 — Partial Correlation Network\n",
    "\n",
    "Graphical Lasso estimates sparse partial correlations between traits."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "Z = StandardScaler().fit_transform(blup)\n",
    "\n",
    "gl = GraphicalLassoCV()\n",
    "gl.fit(Z)\n",
    "\n",
    "P = gl.precision_\n",
    "\n",
    "d = np.sqrt(np.diag(P))\n",
    "\n",
    "pcorr = -P / np.outer(d,d)\n",
    "\n",
    "np.fill_diagonal(pcorr,1)\n",
    "\n",
    "pcorr_df = pd.DataFrame(pcorr, index=traits, columns=traits)\n",
    "\n",
    "sns.heatmap(pcorr_df, cmap='coolwarm')\n",
    "\n",
    "plt.title('Partial Correlation Heatmap')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 6 — Machine Learning Trait Prediction"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "target = 'Harvest index'\n",
    "\n",
    "X = blup.drop(columns=[target])\n",
    "y = blup[target]\n",
    "\n",
    "rf = RandomForestRegressor(n_estimators=300)\n",
    "rf.fit(X,y)\n",
    "\n",
    "importance = pd.Series(rf.feature_importances_, index=X.columns)\n",
    "\n",
    "importance.sort_values().plot.barh()\n",
    "\n",
    "plt.title('Random Forest Feature Importance')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 7 — MGIDI Multi-Trait Selection Index\n",
    "\n",
    "MGIDI identifies superior genotypes considering multiple traits simultaneously."
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "from sklearn.decomposition import FactorAnalysis\n",
    "\n",
    "X = blup.copy()\n",
    "\n",
    "Z = StandardScaler().fit_transform(X)\n",
    "\n",
    "fa = FactorAnalysis(n_components=5)\n",
    "\n",
    "F = fa.fit_transform(Z)\n",
    "\n",
    "ideotype = F.max(axis=0)\n",
    "\n",
    "mgidi = np.sqrt(((F-ideotype)**2).sum(axis=1))\n",
    "\n",
    "mgidi = pd.Series(mgidi,index=blup.index)\n",
    "\n",
    "mgidi.sort_values().head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Step 8 — Identify Elite Mutants"
   ]
  },
  {
   "cell_type": "code",
   "metadata": {},
   "source": [
    "elite = mgidi.sort_values().head(10)\n",
    "\n",
    "elite"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Analysis Completed\n",
    "\n",
    "Outputs include:\n",
    "\n",
    "- BLUP matrix\n",
    "- Trait networks\n",
    "- Machine learning predictors\n",
    "- MGIDI elite mutants\n",
    "\n",
    "These results can be used for breeding selection and trait improvement."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
