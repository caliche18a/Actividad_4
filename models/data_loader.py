from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

import pandas as pd

from config import (
    CAUSES_FILE,
    CAUSES_SHEET,
    DIVIPOLA_FILE,
    DIVIPOLA_SHEET,
    GEOJSON_FILE,
    MORTALITY_FILE,
    MORTALITY_SHEET,
)
from models.age_groups import assign_age_group


SEX_LABELS = {
    1: "Hombres",
    2: "Mujeres",
    3: "Indeterminado",
}

MONTH_LABELS = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}


def _normalize_department_code(series: pd.Series) -> pd.Series:
    return series.astype("Int64").astype(str).str.zfill(2)


def _normalize_municipality_code(series: pd.Series) -> pd.Series:
    return series.astype("Int64").astype(str).str.zfill(5)


@lru_cache(maxsize=1)
def load_geojson() -> dict[str, Any]:
    with open(GEOJSON_FILE, encoding="utf-8") as geojson_file:
        return json.load(geojson_file)


@lru_cache(maxsize=1)
def load_divipola() -> pd.DataFrame:
    divipola = pd.read_excel(DIVIPOLA_FILE, sheet_name=DIVIPOLA_SHEET)
    divipola = divipola[
        ["COD_DANE", "COD_DEPARTAMENTO", "DEPARTAMENTO", "COD_MUNICIPIO", "MUNICIPIO"]
    ].copy()
    divipola["DPTO"] = _normalize_department_code(divipola["COD_DEPARTAMENTO"])
    divipola["COD_DANE_STR"] = _normalize_municipality_code(divipola["COD_DANE"])
    divipola["DEPARTAMENTO"] = divipola["DEPARTAMENTO"].astype(str).str.strip()
    divipola["MUNICIPIO"] = divipola["MUNICIPIO"].astype(str).str.strip()
    return divipola.drop_duplicates("COD_DANE_STR")


@lru_cache(maxsize=1)
def load_causes() -> pd.DataFrame:
    causes = pd.read_excel(CAUSES_FILE, sheet_name=CAUSES_SHEET, header=8)
    code3_col = causes.columns[2]
    name3_col = causes.columns[3]
    code4_col = causes.columns[4]
    name4_col = causes.columns[5]

    three_digit = causes[[code3_col, name3_col]].copy()
    three_digit.columns = ["COD_MUERTE", "CAUSA"]
    four_digit = causes[[code4_col, name4_col]].copy()
    four_digit.columns = ["COD_MUERTE", "CAUSA"]

    catalog = pd.concat([four_digit, three_digit], ignore_index=True)
    catalog["COD_MUERTE"] = catalog["COD_MUERTE"].astype(str).str.upper().str.strip()
    catalog["CAUSA"] = catalog["CAUSA"].astype(str).str.strip()
    catalog = catalog[catalog["COD_MUERTE"].ne("NAN")]
    return catalog.drop_duplicates("COD_MUERTE")


@lru_cache(maxsize=1)
def load_deaths() -> pd.DataFrame:
    deaths = pd.read_excel(MORTALITY_FILE, sheet_name=MORTALITY_SHEET)
    deaths = deaths.copy()

    deaths["DPTO"] = _normalize_department_code(deaths["COD_DEPARTAMENTO"])
    deaths["COD_DANE_STR"] = _normalize_municipality_code(deaths["COD_DANE"])
    deaths["COD_MUERTE"] = deaths["COD_MUERTE"].astype(str).str.upper().str.strip()
    deaths["SEXO_LABEL"] = deaths["SEXO"].map(SEX_LABELS).fillna("Sin informacion")
    deaths["MES_LABEL"] = deaths["MES"].map(MONTH_LABELS)
    deaths["GRUPO_EDAD_CATEGORIA"] = deaths["GRUPO_EDAD1"].apply(assign_age_group)

    divipola = load_divipola()[["COD_DANE_STR", "DEPARTAMENTO", "MUNICIPIO"]]
    deaths = deaths.merge(divipola, how="left", on="COD_DANE_STR")
    deaths["DEPARTAMENTO"] = deaths["DEPARTAMENTO"].fillna("Sin departamento")
    deaths["MUNICIPIO"] = deaths["MUNICIPIO"].fillna("Sin municipio")
    deaths["CIUDAD"] = deaths["MUNICIPIO"] + " (" + deaths["DEPARTAMENTO"] + ")"
    return deaths


@lru_cache(maxsize=1)
def load_reference_data() -> dict[str, Any]:
    divipola = load_divipola()
    departments = (
        divipola[["DPTO", "DEPARTAMENTO"]]
        .drop_duplicates()
        .sort_values("DEPARTAMENTO")
        .reset_index(drop=True)
    )
    return {
        "departments": departments,
        "sexes": list(SEX_LABELS.values()),
        "months": MONTH_LABELS,
        "causes": load_causes(),
    }
