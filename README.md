# 🌾 Rice Genotype–Trait Network & Yield Driver Analysis Pipeline

A **reproducible computational framework** for analyzing genotype–trait relationships in rice breeding populations using **quantitative genetics, multivariate statistics, network analysis, and machine learning**.

This repository implements a **complete analytical pipeline** to identify:

* key traits controlling grain yield
* direct interactions among agronomic traits
* hub traits in trait networks
* elite mutant genotypes using multi-trait selection
* yield-driving predictors using machine learning
* optimal trait combinations for breeding improvement

The workflow produces **publication-ready figures and tables (600 dpi)** suitable for journals such as:

**PLOS ONE  
Scientific Reports  
Frontiers in Plant Science  
Field Crops Research**

---

# 📖 Scientific Motivation

Grain yield in rice is a **complex quantitative trait** controlled by multiple interacting morphological, physiological, and genetic components.

Traditional correlation analysis often fails to reveal **true biological relationships among traits** due to:

* indirect trait effects
* multicollinearity
* environmental variation
* genotype × trait interactions

To overcome these limitations, this pipeline integrates **classical plant breeding statistics with modern computational approaches**, including:

• **BLUP-based genetic estimation**  
• **Graphical Lasso partial correlation networks**  
• **machine learning trait importance models**  
• **multi-trait genotype selection indices (MGIDI)**  
• **response surface modeling of harvest index**  
• **principal component analysis (PCA)**  
• **genotype–trait association networks**

This integrated framework allows researchers to identify **direct trait interactions, yield drivers, and elite genotypes for crop improvement**.

---

# 🧠 Methods Implemented

The pipeline combines **classical quantitative genetics with modern statistical learning methods**.

| Method | Purpose |
|------|------|
| Mixed Linear Model (REML) | Estimate BLUP genotype effects |
| Variance Components | Partition genetic and residual variance |
| Broad-sense Heritability | Measure trait inheritance |
| Graphical Lasso | Estimate sparse partial correlation networks |
| Network Centrality | Identify hub traits driving trait interactions |
| Multiple Linear Regression | Detect key yield predictors |
| Partial Least Squares (PLS) | Estimate trait predictive importance |
| Random Forest | Model nonlinear trait effects |
| SHAP Analysis | Explain machine learning predictions |
| MGIDI Index | Multi-trait genotype selection |
| Path Analysis | Estimate direct trait effects on yield |
| PCA | Identify major sources of phenotypic variation |
| Response Surface Modeling | Analyze trait combinations affecting harvest index |
| Chord Diagram Networks | Visualize genotype–trait associations |

---

# 📂 Repository Structure


rice-genotype-trait-analysis
│
├── data
│ └── example_dataset.xlsx
│
├── scripts
│
│ ├── 01_BLUP_Heritability_Network.py
│ ├── 02_Trait_Network_ML_HI.py
│ ├── 03_GeneticParameters_MGIDI_EliteSelection.py
│ ├── 04_Yield_vs_Traits_Scatter.py
│ ├── 05_HI_Correlation_Matrix.py
│ ├── 06_Genotype_Trait_Chord_Diagram.py
│ ├── 07_HI_Response_Surface.py
│ ├── 08_Parent_vs_Mutants_TraitMatrix.py
│ └── 09_TargetTrait_Correlation_PCA.py
│
├── notebooks
│ └── colab_pipeline.ipynb
│
├── outputs
│ ├── tables
│ ├── figures
│ └── networks
│
├── pipeline_colab.py
├── requirements.txt
└── README.md


---

# 📊 Dataset Requirements

The pipeline expects a **CSV or Excel dataset** from a **Randomized Complete Block Design (RCBD)** experiment.

### Required Columns


Genotype
Replication
Trait columns...


---

### Example Dataset Structure

| Genotype | Replication | Plant height | Panicle length | Filled grains | Grain yield |
|--------|--------|--------|--------|--------|--------|
| Parent | 1 | 110 | 26 | 180 | 38 |
| Mutant1 | 1 | 118 | 28 | 195 | 41 |
| Mutant2 | 1 | 105 | 24 | 165 | 35 |

---

### Example Trait List

Typical agronomic traits include:


Days to flowering
Days to maturity
Plant height
Tillers per hill
Effective tillers per hill
Panicle length
Primary branch per panicle
Secondary branch per panicle
Flag leaf length
Filled grain per panicle
Sterile grain per panicle
Grain length
Grain breadth
1000 grain weight
Grain yield per hill
Straw yield per hill
Harvest index



---
## 🧬 Computational Workflow

This project implements an automated computational pipeline for analyzing rice phenotypic traits using statistical genetics, network analysis, and machine learning.  
The workflow integrates classical quantitative genetics with modern data science tools to identify key determinants of agronomic performance.

All analyses are executed in a **Python-based environment using Google Colab**, enabling reproducibility, scalability, and automated figure generation.

---

### 🔬 Workflow Overview

```
📂 Data Import
      ↓
🔎 Automatic Trait Detection
      ↓
🧬 BLUP Estimation & Heritability
      ↓
📈 Correlation Analysis
      ↓
🌐 Graphical Lasso Trait Network
      ↓
📊 Partial Correlation Modeling
      ↓
🤖 Machine Learning Trait Prediction
      ↓
🧬 Genetic Parameter Estimation
      ↓
🏆 MGIDI Multi-Trait Selection
      ↓
📉 Yield–Trait Regression Analysis
      ↓
📊 PCA Multivariate Trait Structure
      ↓
🌐 Interactive Visualization Dashboard
      ↓
📑 Automated Report Generation
```

---

## 🔹 Step 1 — Data Import and Trait Detection
📂 → 📊  

The phenotypic dataset containing genotype, replication, and agronomic trait measurements is imported into the computational environment.  
Numeric trait columns are automatically detected using Python routines to ensure compatibility with datasets containing variable trait sets.

---

## 🔹 Step 2 — BLUP Estimation and Heritability
🧬 → 📉  

Genotypic effects are estimated using **Best Linear Unbiased Prediction (BLUP)** based on a mixed linear model:

```
yᵢⱼ = μ + Rⱼ + Gᵢ + eᵢⱼ
```

Where:

- **μ** = population mean  
- **Rⱼ** = replication effect  
- **Gᵢ** = genotype effect  
- **eᵢⱼ** = residual error  

Variance components are used to compute **broad-sense heritability (H²)**.

---

## 🔹 Step 3 — Trait Correlation and Network Analysis
📈 → 🌐  

Trait relationships are initially evaluated using **Pearson correlation matrices**.

To reveal direct conditional relationships between traits, a **Graphical Lasso model** is used to estimate sparse inverse covariance matrices, generating **partial correlation networks** that highlight key trait interactions.

Network visualization identifies **hub traits** with strong influence on plant performance.

---

## 🔹 Step 4 — Machine Learning Trait Importance
🤖 → 📊  

Machine learning models are applied to quantify the predictive contribution of individual traits.

Algorithms used include:

- Random Forest regression  
- Gradient Boosting regression  
- SHAP feature importance analysis  

These models identify traits that most strongly influence yield or harvest index.

---

## 🔹 Step 5 — Genetic Parameter Estimation
🧬 → 📉  

Classical quantitative genetic parameters are calculated to evaluate variability and selection potential:

- **Genotypic coefficient of variation (GCV)**  
- **Phenotypic coefficient of variation (PCV)**  
- **Broad-sense heritability (H²)**  
- **Genetic advance (GA)**  
- **Genetic advance as percent of mean (GAM)**  

These metrics help determine which traits respond most effectively to selection.

---

## 🔹 Step 6 — Multi-Trait Selection Using MGIDI
🏆 → 🌾  

The **Multi-Trait Genotype–Ideotype Distance Index (MGIDI)** is used to identify elite genotypes with optimal trait combinations.

Genotypes with **lower MGIDI scores** are considered closer to the ideal breeding profile.

---

## 🔹 Step 7 — Yield–Trait Relationship Modeling
📉 → 📈  

Linear regression models are applied to quantify relationships between grain yield and key yield components such as:

- panicle length  
- filled grains per panicle  
- straw yield  

Regression plots with **95% confidence intervals** are generated to visualize trait contributions.

---

## 🔹 Step 8 — Multivariate Trait Structure (PCA)
📊 → 🔬  

Principal Component Analysis (PCA) summarizes multivariate trait variation across genotypes.

PCA biplots simultaneously visualize:

- genotype clustering  
- trait loadings  
- major axes of phenotypic variation.

---

## 🔹 Step 9 — Interactive Visualization and Reporting
🌐 → 📑  

Interactive dashboards built with **Plotly and Holoviews** allow dynamic exploration of genotype–trait relationships.

All outputs—including figures, statistical tables, and analysis summaries—are automatically exported and compiled into downloadable results and PDF reports.

---

## 💻 Computational Environment

The workflow is implemented using open-source Python libraries:

- **pandas** — data processing  
- **NumPy** — numerical computation  
- **statsmodels** — mixed linear models  
- **scikit-learn** — machine learning and PCA  
- **NetworkX** — network analysis  
- **Plotly / Holoviews** — interactive visualization  

All computations were performed in **Google Colab**, enabling automated and reproducible analysis pipelines.

# ⚙️ Installation

Clone the repository.


git clone https://github.com/yourusername/rice-genotype-trait-analysis

cd rice-genotype-trait-analysis


Install dependencies.


pip install -r requirements.txt


---

# 🚀 Running the Pipeline

Run the main analysis script.


python pipeline_colab.py


Upload your dataset when prompted (`.xlsx` or `.csv`).

The pipeline will automatically perform the **complete genotype–trait analysis workflow**.

---

# 📈 Generated Outputs

The pipeline produces **multiple statistical tables and figures automatically**.

### Tables


BLUP_matrix_genotype_x_traits.csv
VarianceComponents_H2BLUP.csv
PartialCorrelation_Glasso.csv
YieldPredictors_LinearModel.csv
RandomForest_importance.csv
MGIDI_scores.csv
HubTraits_degree_centrality.csv
PCA_Loadings_All_Traits_All_PCs.csv


---

### Figures (600 dpi)


PartialCorrelation_heatmap.png
Trait_network.png
Yield_predictor_barplot.png
PLS_predicted_vs_actual.png
RandomForest_importance.png
SHAP_feature_importance.png
MGIDI_Top10.png
Scatter_yield_vs_traits.png
Chord_genotype_trait_network.png
HI_ResponseSurface.png
PCA_Biplot.png


All figures are exported at **high resolution suitable for journal submission**.

---

# 🧑‍🔬 Author

**Md Rezve**

PhD Applicant — Plant Breeding & Quantitative Genetics

Research interests:

• Quantitative genetics  
• Trait network analysis  
• Machine learning in crop improvement  
• Mutation breeding  
• Multi-trait genotype selection  

---

# 📚 Citation

If you use this pipeline, please cite:


Md Rezve (2026)
Rice Genotype–Trait Network and Yield Driver Analysis Pipeline
GitHub Repository


---

# 📜 License

MIT License

---

⭐ If this repository helps your research, please consider **starring the project**.
