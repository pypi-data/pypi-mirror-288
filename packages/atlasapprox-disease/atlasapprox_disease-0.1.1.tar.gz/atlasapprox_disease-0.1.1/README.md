# atlasapprox-disease

`atlasapprox-disease` is a Python package for accessing approximated versions of cellxgene's disease cell atlas data. This package enables efficient query of large-scale single-cell datasets with reduced memory and computational requirements.

### Installation

You can install the package from PyPI:

```bash
pip install atlasapprox-disease
```
**Please note**: You must have Python >=3.10 to use the high-level API.

### Quick start
**Example 1: To query `differential cell type abundance` of the `flu` disease**

```bash
# import and create an API object
from atlasapprox_disease import API
api = API()

# make API call
df_cell_type_abundance = api.diff_celltype_abundance(disease_keyword="flu")

# display the result
print(df_cell_type_aundance)
```
Output:

![Differential cell type abundance](diff_cell_type_abun.png)


For more detailed tutorials and examples, please visit the API tutorials site ([API tutorials site](https://github.com/YingX97/disease_approximation_API/tree/main/api_tutorials)
).

**Example 2: To query the top 5 `differentially expressed genes` of the `flu` disease**

```bash
df_gene_exp = api.api.diff_gene_expression(disease_keyword="flu", cell_type_keyword="blood", top_n=5)

print(df_gene_exp)
```

Output:

![Differential gene expression](diff_gene_exp.png)



For more detailed tutorials and examples, please visit the [API tutorials site](https://github.com/YingX97/disease_approximation_API/tree/main/api_tutorials).