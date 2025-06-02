import pytest
from server.server import *



# ---- Tests DATA ----

# -------------------------------
# read_lines()
# -------------------------------

def test_read_lines_default():
    result = read_lines()
    assert "results" in result
    assert isinstance(result["results"], list)


def test_read_lines_size_limit():
    result = read_lines(page=1, size=3)
    assert isinstance(result["results"], list)
    assert len(result["results"]) <= 3


def test_read_lines_large_page():
    result = read_lines(page=10, size=5)
    assert "results" in result
    assert isinstance(result["results"], list)


def test_read_lines_sort_ascending():
    result = read_lines(sort="Nom_du_Produit_en_Français")
    assert "results" in result


def test_read_lines_sort_descending():
    result = read_lines(sort="-Nom_du_Produit_en_Français")
    assert "results" in result


def test_read_lines_select_columns():
    selected_columns = ["Nom_du_Produit_en_Français", "Score_unique_EF"]
    result = read_lines(select=selected_columns, size=2)
    assert "results" in result
    for row in result["results"]:
        assert all(col in row for col in selected_columns)


def test_read_lines_with_query():
    result = read_lines(q="pomme", size=5)
    assert "results" in result
    assert isinstance(result["results"], list)


def test_read_lines_with_q_mode_complete():
    result = read_lines(q="pomme", size=3)
    assert "results" in result


def test_read_lines_with_q_fields():
    result = read_lines(q="pomme", q_fields=["Nom_du_Produit_en_Français"])
    assert "results" in result


def test_read_lines_with_qs_advanced():
    result = read_lines(qs='Nom_du_Produit_en_Français:"pomme" AND code_saison:"1"')
    assert "results" in result


def test_read_lines_format_json():
    result = read_lines()
    assert isinstance(result, dict)
    assert "results" in result


def test_read_lines_select_all_columns():
    result = read_lines(select=["_id"], size=1)
    assert "results" in result
    for row in result["results"]:
        assert "_id" in row


def test_read_lines_invalid_sort_does_not_crash():
    result = read_lines(sort="non_existing_column", size=1)
    assert isinstance(result, dict)


def test_read_lines_max_size_limit():
    result = read_lines(size=10000)
    assert "results" in result
    assert len(result["results"]) <= 10000

# -------------------------------
# get_values()
# -------------------------------

def test_get_values_default():
    result = get_values(field="Groupe_d'aliment")
    assert isinstance(result, list)
    assert len(result) <= 10

def test_get_values_sort_desc():
    result = get_values(field="Nom_du_Produit_en_Français", sort="desc")
    assert isinstance(result, list)

def test_get_values_with_query():
    result = get_values(field="Nom_du_Produit_en_Français", q="pomme")
    assert isinstance(result, list)

def test_get_values_with_q_fields():
    result = get_values(field="Nom_du_Produit_en_Français", q="pomme", q_fields=["Nom_du_Produit_en_Français"])
    assert isinstance(result, list)

def test_get_values_with_qs():
    result = get_values(field="Nom_du_Produit_en_Français", qs='Nom_du_Produit_en_Français:"pomme"')
    assert isinstance(result, list)

def test_get_values_invalid_field():
    result = get_values(field="Invalide")
    assert "error" in result

# -------------------------------
# get_metric_agg()
# -------------------------------

def test_get_metric_agg_avg():
    result = get_metric_agg(metric="avg", field="Score_unique_EF")
    assert isinstance(result, dict)
    assert "metric" in result

def test_get_metric_agg_percentiles():
    result = get_metric_agg(metric="percentiles", field="Score_unique_EF", percents="25,50,75")
    assert isinstance(result, dict)
    assert "metric" in result
    assert isinstance(result["metric"], list)
    assert all("key" in p and "value" in p for p in result["metric"])

def test_get_metric_agg_q_fields():
    result = get_metric_agg(metric="avg", field="Score_unique_EF", q="pomme", q_fields=["Nom_du_Produit_en_Français"])
    assert isinstance(result, dict)

def test_get_metric_agg_qs():
    result = get_metric_agg(metric="sum", field="DQR", qs='Nom_du_Produit_en_Français:"pomme"')
    assert isinstance(result, dict)

def test_get_metric_agg_invalid_metric():
    result = get_metric_agg(metric="invalid", field="DQR")
    assert "error" in result

# -------------------------------
# get_simple_metrics_agg()
# -------------------------------

def test_get_simple_metrics_agg_basic():
    result = get_simple_metrics_agg(metrics=["min", "max"], fields=["Score_unique_EF"])
    assert isinstance(result, dict)
    assert "metrics" in result
    assert "Score_unique_EF" in result["metrics"]
    assert all(k in result["metrics"]["Score_unique_EF"] for k in ["min", "max"])

def test_get_simple_metrics_agg_with_query():
    result = get_simple_metrics_agg(metrics=["avg"], fields=["Score_unique_EF"], q="pomme")
    assert isinstance(result, dict)

def test_get_simple_metrics_agg_qs():
    result = get_simple_metrics_agg(metrics=["stats"], fields=["Score_unique_EF"], qs='Nom_du_Produit_en_Français:"pomme"')
    assert isinstance(result, dict)

def test_get_simple_metrics_agg_q_fields():
    result = get_simple_metrics_agg(metrics=["avg"], fields=["Score_unique_EF"], q="pomme", q_fields=["Nom_du_Produit_en_Français"])
    assert isinstance(result, dict)

# -------------------------------
# get_words_agg()
# -------------------------------

def test_get_words_agg_default():
    result = get_words_agg(field="Nom_du_Produit_en_Français", analysis="standard")
    assert isinstance(result, dict)
    assert "metric" in result or "tokens" in result or "buckets" in result or "terms" in result or isinstance(result.get("error"), str)


def test_get_words_agg_standard_analysis():
    result = get_words_agg(field="Nom_du_Produit_en_Français", analysis="standard")
    assert isinstance(result, dict)

def test_get_words_agg_with_query():
    result = get_words_agg(field="Nom_du_Produit_en_Français", q="pomme")
    assert isinstance(result, dict)

def test_get_words_agg_with_q_fields():
    result = get_words_agg(field="Nom_du_Produit_en_Français", q="pomme", q_fields=["Nom_du_Produit_en_Français"])
    assert isinstance(result, dict)

def test_get_words_agg_with_qs():
    result = get_words_agg(field="Nom_du_Produit_en_Français", qs='Nom_du_Produit_en_Français:"pomme"')
    assert isinstance(result, dict)

def test_get_words_agg_invalid_field():
    result = get_words_agg(field="Invalide")
    assert "error" in result


# ---- Tests METADATA ----

def test_read_schema():
    result = read_schema()
    assert isinstance(result, list)
    assert all("key" in col and "label" in col for col in result)


def test_read_schema():
    result = read_schema()
    assert isinstance(result, list)
    assert all(any(k in col for k in ["key", "label", "x-originalName"]) for col in result)


def test_read_api_docs():
    result = read_api_docs()
    assert isinstance(result, dict)
    assert "openapi" in result or "paths" in result