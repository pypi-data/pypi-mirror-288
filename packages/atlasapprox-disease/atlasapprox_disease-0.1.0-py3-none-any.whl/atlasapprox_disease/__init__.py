import os
from typing import List, Optional
from atlasapprox_disease.utils import (
    _fetch_metadata,
    _fetch_differential_celltype_abundance,
    _fetch_differential_gene_expression,
)

__all__ = (
    "api_version",
    "BadRequestError",
    "API",
)

api_version = "v1"

baseurl = os.getenv(
    "ATLASAPPROX_DISEASE_BASEURL",
    "https://disease-approximation-p523xiwksa-ts.a.run.app/",
)
baseurl = baseurl.rstrip("/") + "/"

class API:
    """Main object used to access the disease atlas approximation API.
    
    
    """

    def get_metadata(self, disease_keyword: str):
        """Fetch metadata for a given disease keyword.

        Parameters
        ----------
        disease_keyword : str
            The keyword of the disease.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the metadata results. Each row contains the following columns:
            - unique_id (str): Unique identifier for the record.
            - disease (str): The disease name.
            - cell_type_number (int): Number of types of cells in this record.
            - dataset_id (str): Identifier for the dataset.
            - collection_name (str): Name of the collection the dataset belongs to.
            - unit (str): Unit of measurement.
            - log_transformed (bool): Indicates if the data is log-transformed.
            - has_normal_baseline (bool): Indicates if the dataset has a normal baseline.
        """
        return _fetch_metadata(baseurl, disease_keyword)
    
    def diff_celltype_abundance(self, disease_keyword: Optional[str] = None, unique_ids: Optional[List[str]] = None):
        """Fetch differential cell type abundance for a given keyword or unique IDs (from this get metadata method).

        Parameters
        ----------
        disease_keyword : Optional[str]
            The keyword of the disease.
        unique_ids : Optional[List[str]]
            A list of unique IDs.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the differential cell type abundance results.
        """
        return _fetch_differential_celltype_abundance(baseurl, disease_keyword, unique_ids)

    def diff_gene_expression(self, disease_keyword: Optional[str] = None, unique_ids: Optional[List[str]] = None, cell_type_keyword: Optional[str] = None, top_n: Optional[int] = None):
        """Fetch differential gene expression for a given keyword, unique IDs, cell type, and top N genes.

        Parameters
        ----------
        disease_keyword : Optional[str]
            The keyword of the disease.
        unique_ids : Optional[List[str]]
            A list of unique IDs.
        cell_type : Optional[str]
            The type of cell.
        top_n : Optional[int]
            The number of top genes to return. This will return both the top upregulated and top downregulated genes.
            
        Returns
        -------
        pd.DataFrame
            A DataFrame with the differential gene expression results.
        """
        return _fetch_differential_gene_expression(baseurl, disease_keyword, unique_ids, cell_type_keyword, top_n)
