from __future__ import annotations

import pandas as pd

from models.age_groups import AGE_GROUP_ORDER
from models.data_loader import MONTH_LABELS


def filter_deaths(
    deaths: pd.DataFrame,
    departments: list[str] | None,
    sexes: list[str] | None,
    month_range: list[int] | tuple[int, int] | None,
) -> pd.DataFrame:
    filtered = deaths
    if departments:
        filtered = filtered[filtered["DPTO"].isin(departments)]
    if sexes:
        filtered = filtered[filtered["SEXO_LABEL"].isin(sexes)]
    if month_range:
        start_month, end_month = int(month_range[0]), int(month_range[1])
        filtered = filtered[filtered["MES"].between(start_month, end_month)]
    return filtered.copy()


def kpi_summary(deaths: pd.DataFrame, causes: pd.DataFrame) -> dict[str, str]:
    if deaths.empty:
        return {
            "total_deaths": "0",
            "departments": "0",
            "cities": "0",
            "main_cause": "Sin datos",
        }

    top_cause_code = deaths["COD_MUERTE"].value_counts().idxmax()
    cause_name = causes.set_index("COD_MUERTE")["CAUSA"].to_dict().get(
        top_cause_code, "No encontrada"
    )
    return {
        "total_deaths": f"{len(deaths):,}".replace(",", "."),
        "departments": f"{deaths['DPTO'].nunique():,}".replace(",", "."),
        "cities": f"{deaths['COD_DANE_STR'].nunique():,}".replace(",", "."),
        "main_cause": f"{top_cause_code} - {cause_name}",
    }


def deaths_by_department(deaths: pd.DataFrame, departments: pd.DataFrame) -> pd.DataFrame:
    totals = (
        deaths.groupby("DPTO", as_index=False)
        .size()
        .rename(columns={"size": "TOTAL"})
    )
    summary = departments.merge(totals, how="left", on="DPTO").fillna({"TOTAL": 0})
    summary["TOTAL"] = summary["TOTAL"].astype(int)
    return summary.sort_values("TOTAL", ascending=False)


def deaths_by_month(deaths: pd.DataFrame) -> pd.DataFrame:
    totals = deaths.groupby("MES", as_index=False).size().rename(columns={"size": "TOTAL"})
    calendar = pd.DataFrame({"MES": list(MONTH_LABELS.keys())})
    summary = calendar.merge(totals, how="left", on="MES").fillna({"TOTAL": 0})
    summary["MES_LABEL"] = summary["MES"].map(MONTH_LABELS)
    summary["TOTAL"] = summary["TOTAL"].astype(int)
    return summary


def violent_cities(deaths: pd.DataFrame, limit: int = 5) -> pd.DataFrame:
    x95 = deaths[
        deaths["COD_MUERTE"].str.startswith("X95")
        & deaths["MANERA_MUERTE"].astype(str).str.upper().eq("HOMICIDIO")
    ]
    return (
        x95.groupby(["CIUDAD", "MUNICIPIO", "DEPARTAMENTO"], as_index=False)
        .size()
        .rename(columns={"size": "TOTAL"})
        .sort_values("TOTAL", ascending=False)
        .head(limit)
    )


def lowest_mortality_cities(deaths: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    if deaths.empty:
        return pd.DataFrame(columns=["CIUDAD", "MUNICIPIO", "DEPARTAMENTO", "TOTAL"])

    return (
        deaths.groupby(["CIUDAD", "MUNICIPIO", "DEPARTAMENTO"], as_index=False)
        .size()
        .rename(columns={"size": "TOTAL"})
        .sort_values(["TOTAL", "CIUDAD"], ascending=[True, True])
        .head(limit)
    )


def top_causes(deaths: pd.DataFrame, causes: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    totals = (
        deaths.groupby("COD_MUERTE", as_index=False)
        .size()
        .rename(columns={"size": "TOTAL"})
        .sort_values("TOTAL", ascending=False)
        .head(limit)
    )
    summary = totals.merge(causes, how="left", on="COD_MUERTE")
    summary["CAUSA"] = summary["CAUSA"].fillna("No encontrada en el catalogo")
    summary = summary[["COD_MUERTE", "CAUSA", "TOTAL"]]
    summary.columns = ["Código", "Causa de muerte", "Total"]
    return summary


def deaths_by_sex_department(
    deaths: pd.DataFrame, departments: pd.DataFrame
) -> pd.DataFrame:
    totals = (
        deaths.groupby(["DPTO", "SEXO_LABEL"], as_index=False)
        .size()
        .rename(columns={"size": "TOTAL"})
    )
    summary = totals.merge(departments, how="left", on="DPTO")
    return summary.sort_values(["DEPARTAMENTO", "SEXO_LABEL"])


def deaths_by_age_group(deaths: pd.DataFrame) -> pd.DataFrame:
    totals = (
        deaths.groupby("GRUPO_EDAD_CATEGORIA", as_index=False)
        .size()
        .rename(columns={"size": "TOTAL"})
    )
    categories = pd.DataFrame({"GRUPO_EDAD_CATEGORIA": AGE_GROUP_ORDER})
    summary = categories.merge(totals, how="left", on="GRUPO_EDAD_CATEGORIA")
    summary["TOTAL"] = summary["TOTAL"].fillna(0).astype(int)
    return summary
