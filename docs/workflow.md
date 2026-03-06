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
