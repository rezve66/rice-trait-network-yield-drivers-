# 🌾 Rice Genotype–Trait Network & Yield Driver Analysis Pipeline

A **reproducible computational framework** for analyzing genotype–trait relationships in rice breeding populations using **quantitative genetics, network analysis, and machine learning**.

This repository implements a **complete analytical pipeline** to identify:

* key traits controlling grain yield
* direct interactions among agronomic traits
* hub traits in trait networks
* elite mutant genotypes using multi-trait selection
* trait combinations for breeding improvement

The workflow produces **publication-ready figures and tables** suitable for journals such as **PLOS ONE, Scientific Reports, and Frontiers in Plant Science**.

---

# 📖 Scientific Motivation

Grain yield in rice is a **complex quantitative trait** controlled by multiple interacting morphological and physiological components.

Traditional correlation analysis often fails to reveal **true biological relationships among traits** due to indirect effects and multicollinearity.

To overcome these limitations, this pipeline integrates:

• **BLUP-based genetic estimation**
• **Graphical Lasso partial correlation networks**
• **Machine learning feature importance models**
• **multi-trait genotype selection indices**

This approach allows the identification of **direct trait interactions and key yield-driving components**.

---

# 🔬 Computational Workflow

```text
Field Experiment Data
        │
        ▼
Data Cleaning & Trait Formatting
        │
        ▼
Mixed Linear Model Analysis
(BLUP Estimation)
        │
        ▼
Variance Components
& Heritability
        │
        ▼
BLUP Matrix (Genotype × Traits)
        │
        ▼
Trait Standardization
        │
        ▼
Graphical Lasso
Partial Correlation Analysis
        │
        ▼
Trait Interaction Network
        │
        ▼
Yield Driver Identification
   │          │            │
   ▼          ▼            ▼
PLS Model   RandomForest   SHAP
VIP Scores   Importance    Feature Effects
        │
        ▼
MGIDI Multi-Trait Selection Index
        │
        ▼
Elite Genotype Identification
        │
        ▼
Publication-Ready Figures
```

---

# 🧠 Methods Implemented

The pipeline combines **classical plant breeding statistics with modern machine learning methods**.

| Method                      | Purpose                                 |
| --------------------------- | --------------------------------------- |
| Mixed Linear Model (REML)   | Estimate BLUP genotype effects          |
| Variance Components         | Partition genetic and residual variance |
| Broad-sense Heritability    | Measure trait inheritance               |
| Graphical Lasso             | Estimate partial correlation networks   |
| Network Centrality          | Identify hub traits                     |
| Multiple Linear Regression  | Detect yield predictors                 |
| Partial Least Squares (PLS) | Determine predictive trait importance   |
| Random Forest               | Model nonlinear trait effects           |
| SHAP Analysis               | Explain machine learning predictions    |
| MGIDI Index                 | Multi-trait genotype selection          |
| Path Analysis               | Estimate direct trait effects on yield  |

---

# 📂 Repository Structure

```
rice-genotype-trait-analysis
│
├── data
│   └── example_dataset.xlsx
│
├── scripts
│   ├── 01_data_loading.py
│   ├── 02_blup_heritability.py
│   ├── 03_trait_network.py
│   ├── 04_yield_models.py
│   ├── 05_mgidi_selection.py
│   ├── 06_scatter_relationships.py
│   └── 07_visualizations.py
│
├── notebooks
│   └── colab_pipeline.ipynb
│
├── outputs
│   ├── tables
│   ├── figures
│   └── networks
│
├── pipeline_colab.py
├── requirements.txt
└── README.md
```

---

# 📊 Dataset Requirements

The pipeline expects a **CSV or Excel dataset** from a **Randomized Complete Block Design (RCBD)** experiment.

### Required Columns

```
Genotype
Replication
Trait columns...
```

---

### Example Dataset Structure

| Genotype | Replication | Plant height | Panicle length | Filled grains | Grain yield |
| -------- | ----------- | ------------ | -------------- | ------------- | ----------- |
| Parent   | 1           | 110          | 26             | 180           | 38          |
| Mutant1  | 1           | 118          | 28             | 195           | 41          |
| Mutant2  | 1           | 105          | 24             | 165           | 35          |

---

### Example Trait List

Typical agronomic traits include:

```
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
```

---

# ⚙️ Installation

Clone the repository.

```
git clone https://github.com/yourusername/rice-genotype-trait-analysis
cd rice-genotype-trait-analysis
```

Install dependencies.

```
pip install -r requirements.txt
```

---

# 🚀 Running the Pipeline

Run the main analysis script.

```
python pipeline_colab.py
```

Upload your dataset when prompted (`.xlsx` or `.csv`).

The pipeline will automatically perform the full analysis.

---

# 📈 Generated Outputs

The pipeline produces **multiple tables and figures automatically**.

### Tables

```
BLUP_matrix_genotype_x_traits.csv
VarianceComponents_H2BLUP.csv
PartialCorrelation_Glasso.csv
YieldPredictors_LinearModel.csv
RandomForest_importance.csv
MGIDI_scores.csv
HubTraits_degree_centrality.csv
```

---

### Figures (600 dpi)

```
PartialCorrelation_heatmap.png
Trait_network.png
Yield_predictor_barplot.png
PLS_predicted_vs_actual.png
RandomForest_importance.png
SHAP_feature_importance.png
MGIDI_Top10.png
Scatter_yield_vs_traits.png
```

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

```
Md Rezve (2026)
Rice Genotype–Trait Network and Yield Driver Analysis Pipeline
GitHub Repository
```

---

# 📜 License

MIT License

---

⭐ If this repository helps your research, please consider **starring the project**.
