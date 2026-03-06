# ============================================================
# GENOTYPE–TRAIT CHORD DIAGRAM (INTERACTIVE VISUALIZATION)
# ============================================================
# Author: Jarvis
# Repository: Rice Trait Network Analysis
#
# Purpose
# -------
# Create an interactive circular chord diagram that
# visualizes associations between genotypes and traits.
#
# Features
# --------
# • Trait value normalization
# • Interactive hover tooltips
# • Weighted edges based on trait values
# • Color-coded nodes
# • Circular network layout
#
# Libraries
# ---------
# Holoviews
# Bokeh
#
# Output
# ------
# Interactive chord diagram rendered in notebook
#
# ============================================================

# ============================================================
# 1. Install required packages
# ============================================================

!pip install pandas numpy holoviews bokeh openpyxl

# ============================================================
# 2. Import libraries
# ============================================================

import pandas as pd
import numpy as np
import holoviews as hv

from bokeh.palettes import Category20
from bokeh.io import output_notebook
from google.colab import files

hv.extension('bokeh')
output_notebook()

# ============================================================
# 3. Upload dataset
# ============================================================

print("Upload Excel dataset (rows = genotypes, columns = traits)")

uploaded = files.upload()

file_name = list(uploaded.keys())[0]

print("File uploaded:", file_name)

df = pd.read_excel(file_name)

# ============================================================
# 4. Ensure genotype column
# ============================================================

if df.columns[0].lower() != "genotype":

    df.rename(
        columns={df.columns[0]: "Genotype"},
        inplace=True
    )

print("Columns detected:")
print(df.columns)

# ============================================================
# 5. Convert dataset to long format
# ============================================================

long_df = df.melt(
    id_vars="Genotype",
    var_name="Trait",
    value_name="Value"
)

# ============================================================
# 6. Normalize trait values (safe normalization)
# ============================================================

def safe_normalize(x):

    if x.max() != x.min():

        return (x - x.min()) / (x.max() - x.min())

    else:

        return 0

long_df["Value"] = long_df.groupby("Trait")["Value"].transform(safe_normalize)

# ============================================================
# 7. Clean dataset
# ============================================================

long_df = long_df.replace(
    [np.inf, -np.inf],
    np.nan
).dropna()

long_df = long_df[long_df["Value"] > 0]

# ============================================================
# 8. Create edge list
# ============================================================

edges = pd.DataFrame({

"source": long_df["Genotype"],
"target": long_df["Trait"],
"value": long_df["Value"]

})

# ============================================================
# 9. Create node list
# ============================================================

genotypes = df["Genotype"].unique().tolist()

traits = [c for c in df.columns if c != "Genotype"]

nodes = pd.DataFrame({

"index": genotypes + traits

})

# ============================================================
# 10. Assign colors
# ============================================================

palette = Category20[
    max(3, min(20, len(nodes)))
]

nodes["color"] = (
    palette * (len(nodes) // len(palette) + 1)
)[:len(nodes)]

# ============================================================
# 11. Build chord diagram
# ============================================================

chord = hv.Chord(

(edges, hv.Dataset(nodes, 'index'))

).opts(

hv.opts.Chord(

cmap=palette,

edge_color=hv.dim('source'),

edge_line_width=hv.dim('value') * 8,

edge_alpha=0.7,

node_color='color',

node_size=18,

labels='index',

label_text_font_size='12pt',

label_text_font_style='bold',

width=1100,

height=1100,

title="Genotype–Trait Association Chord Diagram",

tools=['hover'],

show_title=True,

fontscale=1.3

)

)

# ============================================================
# 12. Display diagram
# ============================================================

chord
