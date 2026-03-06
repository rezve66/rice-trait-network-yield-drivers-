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

# 🔬 Computational Workflow

┌──────────────────────┐
│ 🌾 Field Experiment  │
│ Genotype × Traits    │
│ RCBD dataset         │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│ 📊 BLUP Estimation   │
│ Mixed Linear Model   │
│ Variance Components  │
│ Heritability         │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────────────┐
│ 🕸 Trait Interaction Network │
│ Graphical Lasso              │
│ Partial Correlations         │
│ Hub Trait Detection          │
└─────────┬────────────────────┘
          │
          ▼
┌──────────────────────────────┐
│ 🤖 Machine Learning Models   │
│ PLS Regression               │
│ Random Forest                │
│ SHAP Feature Importance      │
└─────────┬────────────────────┘
          │
          ▼
┌──────────────────────────────┐
│ 🎯 Yield Driver Detection    │
│ Trait Importance Ranking     │
│ Direct Trait Effects         │
└─────────┬────────────────────┘
          │
          ▼
┌──────────────────────────────┐
│ 🌿 Multi-Trait Selection     │
│ MGIDI Index                  │
│ Elite Mutant Identification  │
└─────────┬────────────────────┘
          │
          ▼
┌──────────────────────────────┐
│ 📈 Advanced Trait Analysis   │
│ PCA                          │
│ Response Surface Modeling    │
│ Genotype–Trait Chord Network │
└─────────┬────────────────────┘
          │
          ▼
┌──────────────────────────────┐
│ 📄 Publication-Ready Outputs │
│ Tables & Figures (600 dpi)   │
│ Trait Networks               │
│ ML Importance Plots          │
└──────────────────────────────┘
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
