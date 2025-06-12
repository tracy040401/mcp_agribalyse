from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from mcp.server.fastmcp.tools import Tool
from mcp.server.fastmcp.resources import Resource

import requests
from typing import Optional, List

# Initialisation du serveur MCP
mcp = FastMCP("Agribalyse")

BASE_URL = "https://data.ademe.fr/data-fair/api/v1/datasets/agribalyse-31-synthese"

# ---------------------------
# -------- RESOURCES --------
# ---------------------------
@mcp.resource("agribalyse://api-docs")
def agribalyse_api_docs() -> dict:
    """Retrieve the full OpenAPI specification of the Agribalyse API."""
    response = requests.get(f"{BASE_URL}/api-docs.json")
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code}

@mcp.resource("agribalyse://files")
def agribalyse_data_files() -> dict:
    """List data files available through the ADEME API."""
    response = requests.get(f"{BASE_URL}/data-files")
    return response.json()

@mcp.resource("agribalyse://fields")
def agribalyse_field_list() -> list:
    """List of allowed textual fields for queries (used for validation or suggestions)."""
    return [
        "Code_AGB", "Groupe_d'aliment", "Sous-groupe_d'aliment",
        "Nom_du_Produit_en_Français", "LCI_Name", "code_saison",
        "Livraison", "Approche_emballage_", "Préparation"
    ]


@mcp.resource("agribalyse://columns/sortables")
def agribalyse_sortable_fields() -> list:
    """Fields that can be used for sorting query results."""
    return [
        "Code_AGB", "Code_CIQUAL", "Groupe_d'aliment", "Sous-groupe_d'aliment",
        "Nom_du_Produit_en_Français", "LCI_Name", "code_saison", "code_avion",
        "Livraison", "Approche_emballage_", "Préparation", "DQR", "Score_unique_EF",
        "Changement_climatique", "Appauvrissement_de_la_couche_d'ozone",
        "Rayonnements_ionisants", "Formation_photochimique_d'ozone", "Particules_fines",
        "Effets_toxicologiques_sur_la_santé_humaine___substances_non-cancérogènes",
        "Effets_toxicologiques_sur_la_santé_humaine___substances_cancérogènes",
        "Acidification_terrestre_et_eaux_douces", "Eutrophisation_eaux_douces",
        "Eutrophisation_marine", "Eutrophisation_terrestre",
        "Écotoxicité_pour_écosystèmes_aquatiques_d'eau_douce",
        "Utilisation_du_sol", "Épuisement_des_ressources_eau",
        "Épuisement_des_ressources_énergétiques", "Épuisement_des_ressources_minéraux",
        "Changement_climatique_-_émissions_biogéniques",
        "Changement_climatique_-_émissions_fossiles",
        "Changement_climatique_-_émissions_liées_au_changement_d'affectation_des_sols",
        "_id", "_i", "_rand"
    ]

@mcp.resource("agribalyse://metrics/fields")
def agribalyse_metric_fields() -> list:
    """Numeric columns eligible for metric calculations."""
    return [
        "DQR", "Score_unique_EF", "Changement_climatique",
        "Appauvrissement_de_la_couche_d'ozone", "Rayonnements_ionisants",
        "Formation_photochimique_d'ozone", "Particules_fines",
        "Effets_toxicologiques_sur_la_santé_humaine___substances_non-cancérogènes",
        "Effets_toxicologiques_sur_la_santé_humaine___substances_cancérogènes",
        "Acidification_terrestre_et_eaux_douces", "Eutrophisation_eaux_douces",
        "Eutrophisation_marine", "Eutrophisation_terrestre",
        "Écotoxicité_pour_écosystèmes_aquatiques_d'eau_douce",
        "Utilisation_du_sol", "Épuisement_des_ressources_eau",
        "Épuisement_des_ressources_énergétiques", "Épuisement_des_ressources_minéraux",
        "Changement_climatique_-_émissions_biogéniques",
        "Changement_climatique_-_émissions_fossiles",
        "Changement_climatique_-_émissions_liées_au_changement_d'affectation_des_sols"
    ]

@mcp.resource("agribalyse://metrics/types")
def agribalyse_metric_types() -> list:
    """List of available metric types for numerical fields."""
    return [
        "avg", "sum", "min", "max", "stats", "value_count",
        "percentiles", "cardinality"
    ]

@mcp.resource("agribalyse://fields/descriptions")
def agribalyse_field_descriptions() -> dict:
    """Descriptions of fields from the Agribalyse 3.1 dataset."""
    return {
        "Code_AGB": "Unique internal identifier for Agribalyse.",
        "Code_CIQUAL": "Identifier for the related CIQUAL record.",
        "Groupe_d'aliment": "General food category.",
        "Sous-groupe_d'aliment": "More specific sub-category of food group.",
        "Nom_du_Produit_en_Français": "Common product name in French.",
        "LCI_Name": "Name in the Life Cycle Inventory database.",
        "code_saison": "Seasonal status: 1=in season, 0=off season, 2=mixed.",
        "code_avion": "Boolean indicating if product was air-transported.",
        "Livraison": "Delivery mode (Frozen, Ambient, etc.).",
        "Approche_emballage_": "Modeling approach for packaging (PACK AGB or PACK PROXY).",
        "Préparation": "Cooking or preparation method (e.g., oven, pan).",
        "DQR": "Data Quality Rating: from 1 (excellent) to 5 (poor).",
        "Score_unique_EF": "Single environmental score in milli-points/kg.",
        "Changement_climatique": "Climate change impact in CO₂-eq/kg.",
        "Appauvrissement_de_la_couche_d'ozone": "Ozone depletion in kg CFC-11 eq.",
        "Rayonnements_ionisants": "Ionizing radiation in kBq U-235 eq.",
        "Formation_photochimique_d'ozone": "Photochemical ozone formation in kg NMVOC eq.",
        "Particules_fines": "Fine particulate impact in disease incidence/kg.",
        "Effets_toxicologiques_sur_la_santé_humaine___substances_non-cancérogènes": "Non-carcinogenic toxicity (CTUh/kg).",
        "Effets_toxicologiques_sur_la_santé_humaine___substances_cancérogènes": "Carcinogenic toxicity (CTUh/kg).",
        "Acidification_terrestre_et_eaux_douces": "Acidification in mol H+ eq./kg.",
        "Eutrophisation_eaux_douces": "Freshwater eutrophication in kg P eq./kg.",
        "Eutrophisation_marine": "Marine eutrophication in kg N eq./kg.",
        "Eutrophisation_terrestre": "Terrestrial eutrophication in mol N eq./kg.",
        "Écotoxicité_pour_écosystèmes_aquatiques_d'eau_douce": "Freshwater ecotoxicity (CTUe/kg).",
        "Utilisation_du_sol": "Land use expressed in Points.",
        "Épuisement_des_ressources_eau": "Water depletion in m³ deprivation eq./kg.",
        "Épuisement_des_ressources_énergétiques": "Energy depletion in MJ/kg.",
        "Épuisement_des_ressources_minéraux": "Mineral depletion in kg Sb eq./kg.",
        "Changement_climatique_-_émissions_biogéniques": "Biogenic CO₂ emissions.",
        "Changement_climatique_-_émissions_fossiles": "Fossil CO₂ emissions.",
        "Changement_climatique_-_émissions_liées_au_changement_d'affectation_des_sols": "Land use change-related emissions.",
        "_id": "Unique internal line ID.",
        "_i": "Row index in the dataset.",
        "_rand": "Random value assigned to the row (for sampling)."
    }
 
# -------------------------
# --------- TOOLS ---------
# -------------------------
@mcp.tool()
def read_lines(
    page: int = 1,
    size: int = 10,
    sort: Optional[str] = None,
    select: Optional[List[str]] = None,
    q: Optional[str] = None,
    q_fields: Optional[List[str]] = None,
    qs: Optional[str] = None
) -> dict:
    """
    Retrieve data lines from the Agribalyse dataset via the ADEME public API.

    Arguments:
    - page: Page number to retrieve (default: 1).
    - size: Number of results to return per page (max: 10,000).
    - sort: Sorting criteria as a comma-separated string  (prefix field with '-' for descending order).
        Allowed fields for sorting:
        - Code_AGB, Code_CIQUAL, Groupe_d'aliment, Sous-groupe_d'aliment,
        - Nom_du_Produit_en_Français, LCI_Name, code_saison, code_avion,
        - Livraison, Approche_emballage_, Préparation, DQR, Score_unique_EF,
        - Changement_climatique, Appauvrissement_de_la_couche_d'ozone,
        - Rayonnements_ionisants, Formation_photochimique_d'ozone, Particules_fines,
        - Effets_toxicologiques_sur_la_santé_humaine___substances_non-cancérogènes,
        - Effets_toxicologiques_sur_la_santé_humaine___substances_cancérogènes,
        - Acidification_terrestre_et_eaux_douces, Eutrophisation_eaux_douces,
        - Eutrophisation_marine, Eutrophisation_terrestre,
        - Écotoxicité_pour_écosystèmes_aquatiques_d'eau_douce,
        - Utilisation_du_sol, Épuisement_des_ressources_eau,
        - Épuisement_des_ressources_énergétiques, Épuisement_des_ressources_minéraux,
        - Changement_climatique_-_émissions_biogéniques,
        - Changement_climatique_-_émissions_fossiles,
        - Changement_climatique_-_émissions_liées_au_changement_d'affectation_des_sols,
        - _id, _i, _rand

    - select: List of columns to include in the result. Same list as for `sort` (voir ci-dessus).
    - q: Simple text search query applied across selected fields.
        - Example: "pomme" will match any row containing 'pomme'.
    - q_fields: List of fields to restrict simple text search. Allowed fields:
        - Code_AGB, Groupe_d'aliment, Sous-groupe_d'aliment,
        - Nom_du_Produit_en_Français, LCI_Name, code_saison,
        - Livraison, Approche_emballage_, Préparation
    - qs: Advanced query string using Elasticsearch-style query DSL for complex filtering.

    Returns:
    - Dictionary containing the paginated dataset rows matching the query parameters.
    """
    params = {
        "page": page,
        "size": size
    }
    if sort:
        params["sort"] = sort
    if select:
        params["select"] = ",".join(select)
    if q:
        params["q"] = q
    if q_fields:
        params["q_fields"] = ",".join(q_fields)
    if qs:
        params["qs"] = qs

    url = f"{BASE_URL}/lines"
    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code}

@mcp.tool()
def get_values(
    field: str,
    size: int = 10,
    sort: str = "asc",
    q: Optional[str] = None,
    q_mode: str = "simple",
    q_fields: Optional[List[str]] = None,
    qs: Optional[str] = None
) -> dict:
    """
    Get distinct values of a given field in the Agribalyse dataset.

    Arguments:
    - field: Field name to get distinct values from. Allowed fields:
        - Code_AGB, Groupe_d'aliment, Sous-groupe_d'aliment,
        - Nom_du_Produit_en_Français, LCI_Name, code_saison,
        - Livraison, Approche_emballage_, Préparation

    - size: Number of values to return (1-1000, default: 10).
    - sort: Sort order: "asc" for ascending, "desc" for descending.
    - q: Simple text search query to filter values.
    - q_mode: Search mode. Allowed values:
        - simple, complete
    - q_fields: List of fields to apply text search to. Allowed fields:
        - Code_AGB, Groupe_d'aliment, Sous-groupe_d'aliment,
        - Nom_du_Produit_en_Français, LCI_Name, code_saison,
        - Livraison, Approche_emballage_, Préparation
    - qs: Advanced query string using Elasticsearch-style query DSL for complex filtering.

    Returns:
    - JSON object with distinct values and their counts.
    """
    allowed_fields = [
        "Code_AGB", "Groupe_d'aliment", "Sous-groupe_d'aliment",
        "Nom_du_Produit_en_Français", "LCI_Name", "code_saison",
        "Livraison", "Approche_emballage_", "Préparation"
    ]
    if field not in allowed_fields:
        return {"error": f"The field '{field}' is not valid."}

    url = f"{BASE_URL}/values/{field}"
    params = {
        "size": size,
        "sort": sort,
        "q_mode": q_mode
    }
    if q:
        params["q"] = q
    if q_fields:
        params["q_fields"] = ",".join(q_fields)
    if qs:
        params["qs"] = qs

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code}

@mcp.tool()
def get_metric_agg(
    metric: str,
    field: str,
    percents: Optional[str] = None,
    q: Optional[str] = None,
    q_mode: str = "simple",
    q_fields: Optional[List[str]] = None,
    qs: Optional[str] = None
) -> dict:
    """
    Calculate a metric on a numeric column of the Agribalyse dataset.

    Arguments:
    - metric: Aggregation type. Allowed values:
        - avg, sum, min, max, stats, value_count, percentiles, cardinality
    - field: Target column for aggregation. Allowed fields:
        - DQR, Score_unique_EF, Changement_climatique,
        - Appauvrissement_de_la_couche_d'ozone, Rayonnements_ionisants,
        - Formation_photochimique_d'ozone, Particules_fines,
        - Effets_toxicologiques_sur_la_santé_humaine___substances_non-cancérogènes,
        - Effets_toxicologiques_sur_la_santé_humaine___substances_cancérogènes,
        - Acidification_terrestre_et_eaux_douces, Eutrophisation_eaux_douces,
        - Eutrophisation_marine, Eutrophisation_terrestre,
        - Écotoxicité_pour_écosystèmes_aquatiques_d'eau_douce,
        - Utilisation_du_sol, Épuisement_des_ressources_eau,
        - Épuisement_des_ressources_énergétiques, Épuisement_des_ressources_minéraux,
        - Changement_climatique_-_émissions_biogéniques,
        - Changement_climatique_-_émissions_fossiles,
        - Changement_climatique_-_émissions_liées_au_changement_d'affectation_des_sols

    - percents: List of percentiles (comma-separated) required if metric = percentiles.
    - q: Simple text search query.
    - q_mode: Search mode. Allowed values:
        - simple, complete
    - q_fields: Fields for simple search. Allowed fields:
        - Code_AGB, Groupe_d'aliment, Sous-groupe_d'aliment,
        - Nom_du_Produit_en_Français, LCI_Name, code_saison,
        - Livraison, Approche_emballage_, Préparation
    - qs: Advanced query string using Elasticsearch-style query DSL.

    Returns:
    - JSON result of the metric computation.
    """
    valid_metrics = [
        "avg", "sum", "min", "max", "stats", "value_count", "percentiles", "cardinality"
    ]
    if metric not in valid_metrics:
        return {"error": f"Metric '{metric}' is not supported."}

    url = f"{BASE_URL}/metric_agg"
    params = {
        "metric": metric,
        "field": field,
        "q_mode": q_mode
    }
    if percents:
        params["percents"] = percents
    if q:
        params["q"] = q
    if q_fields:
        params["q_fields"] = ",".join(q_fields)
    if qs:
        params["qs"] = qs

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code}

@mcp.tool()
def get_simple_metrics_agg(
    metrics: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    q: Optional[str] = None,
    q_mode: str = "simple",
    q_fields: Optional[List[str]] = None,
    qs: Optional[str] = None
) -> dict:
    """
    Calculate multiple metrics on multiple numeric columns of the Agribalyse dataset.

    Arguments:
    - metrics: List of metrics to compute. Allowed values:
        - avg, sum, min, max, stats, value_count, percentiles, cardinality
    - fields: Target columns for aggregation. Allowed fields:
        - DQR, Score_unique_EF, Changement_climatique,
        - Appauvrissement_de_la_couche_d'ozone, Rayonnements_ionisants,
        - Formation_photochimique_d'ozone, Particules_fines,
        - Effets_toxicologiques_sur_la_santé_humaine___substances_non-cancérogènes,
        - Effets_toxicologiques_sur_la_santé_humaine___substances_cancérogènes,
        - Acidification_terrestre_et_eaux_douces, Eutrophisation_eaux_douces,
        - Eutrophisation_marine, Eutrophisation_terrestre,
        - Écotoxicité_pour_écosystèmes_aquatiques_d'eau_douce,
        - Utilisation_du_sol, Épuisement_des_ressources_eau,
        - Épuisement_des_ressources_énergétiques, Épuisement_des_ressources_minéraux,
        - Changement_climatique_-_émissions_biogéniques,
        - Changement_climatique_-_émissions_fossiles,
        - Changement_climatique_-_émissions_liées_au_changement_d'affectation_des_sols

    - q: Simple text search query.
    - q_mode: Search mode. Allowed values:
        - simple, complete
    - q_fields: Fields for simple search. Allowed fields:
        - Code_AGB, Groupe_d'aliment, Sous-groupe_d'aliment,
        - Nom_du_Produit_en_Français, LCI_Name, code_saison,
        - Livraison, Approche_emballage_, Préparation
    - qs: Advanced query string using Elasticsearch-style query DSL.

    Returns:
    - Dictionary with aggregated results.
    """
    url = f"{BASE_URL}/simple_metrics_agg"
    params = {"q_mode": q_mode}

    if metrics:
        params["metrics"] = ",".join(metrics)
    if fields:
        params["fields"] = ",".join(fields)
    if q:
        params["q"] = q
    if q_fields:
        params["q_fields"] = ",".join(q_fields)
    if qs:
        params["qs"] = qs

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code}

@mcp.tool()
def get_words_agg(
    field: str,
    analysis: str = "lang",
    q: Optional[str] = None,
    q_mode: str = "simple",
    q_fields: Optional[List[str]] = None,
    qs: Optional[str] = None
) -> dict:
    """
    Retrieve most significant word tokens from a textual field.

    Arguments:
    - field: Target column. Allowed fields:
        - Code_AGB, Groupe_d'aliment, Sous-groupe_d'aliment,
        - Nom_du_Produit_en_Français, LCI_Name, code_saison,
        - Livraison, Approche_emballage_, Préparation
    - analysis: Tokenization analysis mode. Allowed values:
        - lang, standard
    - q: Simple text search query.
    - q_mode: Search mode. Allowed values:
        - simple, complete
    - q_fields: Fields for simple search. Allowed fields:
        - Code_AGB, Groupe_d'aliment, Sous-groupe_d'aliment,
        - Nom_du_Produit_en_Français, LCI_Name, code_saison,
        - Livraison, Approche_emballage_, Préparation
    - qs: Advanced query string using Elasticsearch-style query DSL.

    Returns:
    - JSON result with frequent word tokens.
    """
    valid_fields = [
        "Code_AGB", "Groupe_d'aliment", "Sous-groupe_d'aliment",
        "Nom_du_Produit_en_Français", "LCI_Name", "code_saison",
        "Livraison", "Approche_emballage_", "Préparation"
    ]
    if field not in valid_fields:
        return {"error": f"Invalid field: '{field}'"}

    url = f"{BASE_URL}/words_agg"
    params = {
        "field": field,
        "analysis": analysis,
        "q_mode": q_mode
    }

    if q:
        params["q"] = q
    if q_fields:
        params["q_fields"] = ",".join(q_fields)
    if qs:
        params["qs"] = qs

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code}

@mcp.tool()
def read_schema(
    mimeType: str = "application/json",
    type: Optional[List[str]] = None,
    format: Optional[List[str]] = None,
    capability: Optional[str] = None,
    enum: Optional[str] = None,
    calculated: Optional[str] = None
) -> dict:
    """
    Retrieve the full schema of the Agribalyse dataset columns.

    Arguments:
    - mimeType: Expected mime type of response (default: application/json).
    - type: Optional filter for field types.
    - format: Optional filter for field formats.
    - capability: Optional capability filter.
    - enum: Optional enumeration filter.
    - calculated: Optional calculated field filter.

    Returns:
    - Full schema description of dataset fields.
    """
    url = f"{BASE_URL}/schema"
    params = {"mimeType": mimeType}
    if type:
        params["type"] = ",".join(type)
    if format:
        params["format"] = ",".join(format)
    if capability:
        params["capability"] = capability
    if enum:
        params["enum"] = enum
    if calculated:
        params["calculated"] = calculated

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code}

@mcp.tool()
def read_safe_schema(
    mimeType: str = "application/json",
    type: Optional[List[str]] = None,
    format: Optional[List[str]] = None,
    capability: Optional[str] = None,
    enum: Optional[str] = None,
    calculated: Optional[str] = None
) -> dict:
    """
    Retrieve a safe (reduced) schema version excluding sensitive or costly columns.

    Arguments:
    - mimeType: Expected mime type of response (default: application/json).
    - type: Optional filter for field types.
    - format: Optional filter for field formats.
    - capability: Optional capability filter.
    - enum: Optional enumeration filter.
    - calculated: Optional calculated field filter.

    Returns:
    - Safe schema description of dataset fields.
    """
    url = f"{BASE_URL}/safe-schema"
    params = {"mimeType": mimeType}
    if type:
        params["type"] = ",".join(type)
    if format:
        params["format"] = ",".join(format)
    if capability:
        params["capability"] = capability
    if enum:
        params["enum"] = enum
    if calculated:
        params["calculated"] = calculated

    response = requests.get(url, params=params)

    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        return {"error": str(e), "status_code": response.status_code}

# -------------------------
# -------- PROMPTS --------
# -------------------------
   
@mcp.prompt()
def search_product(nom: str) -> str:
    return f"Can you give me the environmental impact information for the product named: {nom}?"

@mcp.prompt()
def ask_stat(field: str, metric: str) -> str:
    return f"What is the {metric} value of the indicator {field} in the Agribalyse dataset?"

@mcp.prompt()
def compare_products(prod1: str, prod2: str, indicator: str) -> str:
    return (
        f"Compare the environmental impacts of **{prod1}** and **{prod2}** "
        f"based on the following indicator: {indicator}."
    )

@mcp.prompt()
def list_field_values(field: str) -> str:
    return f"What are the possible values for the field {field} in the Agribalyse dataset?"

@mcp.prompt()
def custom_query_prompt() -> list[base.Message]:
    return [
        base.UserMessage("I would like to query lines from the Agribalyse dataset."),
        base.AssistantMessage("Which filters would you like to apply (product, group, season...)?"),
    ]

@mcp.prompt()
def sample_prompt() -> str:
    return "Show me a sample of lines from the Agribalyse dataset so I can understand its structure."

@mcp.prompt()
def explain_indicator(field: str) -> str:
    return f"Explain the environmental indicator {field} used in the Agribalyse dataset."

if __name__ == "__main__":
    mcp.run(transport='sse')
