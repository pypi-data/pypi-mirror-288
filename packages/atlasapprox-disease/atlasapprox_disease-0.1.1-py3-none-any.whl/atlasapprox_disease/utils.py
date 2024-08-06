import requests, json
import pandas as pd
from atlasapprox_disease.exceptions import BadRequestError

def _fetch_metadata(baseurl, disease_keyword):
    
    url = f"{baseurl}metadata"
    params = {"disease_keyword": disease_keyword}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise BadRequestError(f"Error fetching metadata: {response.text}")
    
    return pd.DataFrame(response.json())

def _fetch_differential_celltype_abundance(baseurl, disease_keyword, unique_ids):

    url = f"{baseurl}differential_cell_type_abundance"
    params = {}

    if disease_keyword:
        params["disease_keyword"] = disease_keyword
    elif unique_ids:
        params["unique_ids"] = ','.join(unique_ids)
    else:
        raise BadRequestError("Either disease_keyword or unique_ids must be provided")

    response = requests.post(url, params=params)
    if response.status_code != 200:
        raise BadRequestError(f"Error fetching differential cell type abundance: {response.text}")

    return pd.DataFrame(response.json())



def _fetch_differential_gene_expression(baseurl, disease_keyword, unique_ids, cell_type_keyword, top_n):
    
    url = f"{baseurl}differential_gene_expression"
    
    params = {
        "disease_keyword": disease_keyword if disease_keyword else '',
        "unique_ids": ",".join(unique_ids) if unique_ids else '',
        "cell_type_keyword": cell_type_keyword if cell_type_keyword else '',
        "top_n": top_n
    }

    response = requests.post(url, params=params)
    
    if response.status_code != 200:
        raise BadRequestError(f"Error fetching differential gene expression: {response.text}")
    
    return pd.DataFrame(response.json())