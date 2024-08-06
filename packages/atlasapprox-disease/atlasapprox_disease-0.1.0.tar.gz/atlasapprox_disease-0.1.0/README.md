# Atlasapprox-Diseases

atlasapprox-diseases is a Python package for accessing disease cell atlas approximations.

### Installation

You can install the package from PyPI:

```bash
pip install atlasapprox-disease
```
### Usage
#####  Example 1: 
**To look at differential cell type abundance of a disease of interet**

```bash
from atlasapprox_diseases import API

api = API()
result = api.diff_celltype_abundance(disease_keyword="flu")
print(result)
```
**Expected Output**
```json
[
    {
        "disease": "influenza",
        "dataset_id": "de2c780c-1747-40bd-9ccf-9588ec186cee",
        "cell_type": "blood cell",
        "normal_count": 309,
        "disease_count": 216,
        "total_count": 525,
        "normal_pct": 58.857142857142854,
        "disease_pct": 41.14285714285714,
        "delta_fraction": -17.714285714285715
    },
    {
        ...
        "cell_type": "erythrocyte",
        "normal_count": 184,
        "disease_count": 309,
        ...
    } ...
```
#####  Example 2: 
**To look at top N differentially expressed genes of a disease of interet**

```bash

result = api.api.diff_gene_expression(disease_keyword="immunodeficency")
print(result)
```

**Expected output**

```json
[
    {
        "disease": "common variable immunodeficiency",
        "dataset_id": "a5d95a42-0137-496f-8a60-101e17f263c8",
        "condition": "common variable immunodeficiency",
        "cell_type": "naive B cell",
        "regulation": "up",
        "feature_name": "ENSG00000044574",
        "expr_normal": 0.676017701625824,
        "expr_disease": 4.170171737670898,
        "frac_normal": 0.09770114719867706,
        "frac_disease": 0.21674877405166626,
        "log2_fc": 1.6251747608184814,
        "delta_change": 3.4941539764404297
    },
    {
        ...
        "feature_name": "ENSG00000168734",
        ...
    },
```

