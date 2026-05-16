from __future__ import annotations

import pandas as pd
import plotly.graph_objs as go

from models.age_groups import AGE_GROUP_LABELS


COLORWAY = ["#1f6f8b", "#d1495b", "#edae49", "#2a9d8f", "#5d5fef", "#8f5d46"]
BG = "#f6f8fb"
PANEL = "#ffffff"
TEXT = "#1f2933"
GRID = "#d9e2ec"


def _base_layout(
    fig: go.Figure,
    title: str,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
) -> go.Figure:
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left"},
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font={"family": "Inter, Segoe UI, sans-serif", "color": TEXT},
        colorway=COLORWAY,
        margin={"l": 44, "r": 24, "t": 64, "b": 52},
        legend={"orientation": "h", "y": -0.18},
    )
    fig.update_xaxes(title=xaxis_title, showgrid=False, zeroline=False)
    fig.update_yaxes(title=yaxis_title, gridcolor=GRID, zeroline=False)
    return fig


def _empty_figure(title: str, message: str = "No hay datos para la selección") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        showarrow=False,
        font={"size": 15, "color": "#52616f"},
        xref="paper",
        yref="paper",
    )
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _base_layout(fig, title)


def department_map_figure(data: pd.DataFrame, geojson: dict) -> go.Figure:
    if data.empty:
        return _empty_figure("Muertes por departamento")

    fig = go.Figure(
        go.Choropleth(
            geojson=geojson,
            locations=data["DPTO"],
            z=data["TOTAL"],
            featureidkey="properties.DPTO",
            colorscale=[
                [0.0, "#edf2f7"],
                [0.25, "#b8d8d8"],
                [0.5, "#73a9ad"],
                [0.75, "#2d728f"],
                [1.0, "#12355b"],
            ],
            marker_line_width=0.6,
            marker_line_color="#ffffff",
            text=data["DEPARTAMENTO"],
            customdata=data[["TOTAL"]],
            hovertemplate="<b>%{text}</b><br>Muertes: %{customdata[0]:,}<extra></extra>",
            colorbar={"title": "Muertes", "thickness": 14},
        )
    )
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        showcountries=False,
        showcoastlines=False,
        showland=False,
    )
    fig.update_layout(
        title={"text": "Distribución geográfica de muertes", "x": 0.02, "xanchor": "left"},
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font={"family": "Inter, Segoe UI, sans-serif", "color": TEXT},
        margin={"l": 8, "r": 8, "t": 58, "b": 8},
        height=540,
    )
    return fig


def monthly_line_figure(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure(
        go.Scatter(
            x=data["MES_LABEL"],
            y=data["TOTAL"],
            mode="lines+markers",
            line={"width": 3, "color": COLORWAY[0]},
            marker={"size": 8},
            hovertemplate="<b>%{x}</b><br>Muertes: %{y:,}<extra></extra>",
        )
    )
    return _base_layout(fig, "Total de muertes por mes", "Mes", "Muertes")


def violent_cities_bar_figure(data: pd.DataFrame) -> go.Figure:
    title = "Top 5 ciudades por homicidios X95"
    if data.empty:
        return _empty_figure(title)

    data = data.sort_values("TOTAL")
    fig = go.Figure(
        go.Bar(
            x=data["TOTAL"],
            y=data["CIUDAD"],
            orientation="h",
            marker={"color": COLORWAY[1]},
            text=data["TOTAL"],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Homicidios X95: %{x:,}<extra></extra>",
        )
    )
    fig = _base_layout(fig, title, "Homicidios X95", "Ciudad")
    fig.update_xaxes(range=[0, int(data["TOTAL"].max() * 1.18)])
    return fig


def lowest_mortality_pie_figure(data: pd.DataFrame) -> go.Figure:
    title = "Ciudades con menor mortalidad registrada"
    if data.empty:
        return _empty_figure(title)

    fig = go.Figure(
        go.Pie(
            labels=data["CIUDAD"],
            values=data["TOTAL"],
            hole=0.36,
            sort=False,
            textinfo="label+value",
            hovertemplate="<b>%{label}</b><br>Muertes: %{value:,}<extra></extra>",
        )
    )
    fig.update_traces(marker={"line": {"color": "#ffffff", "width": 1}})
    return _base_layout(fig, title)


def sex_department_bar_figure(data: pd.DataFrame) -> go.Figure:
    title = "Muertes por sexo en cada departamento"
    if data.empty:
        return _empty_figure(title)

    fig = go.Figure()
    order = (
        data.groupby("DEPARTAMENTO", as_index=False)["TOTAL"]
        .sum()
        .sort_values("TOTAL", ascending=True)["DEPARTAMENTO"]
    )
    for sex, color in zip(sorted(data["SEXO_LABEL"].unique()), COLORWAY):
        subset = data[data["SEXO_LABEL"] == sex]
        fig.add_trace(
            go.Bar(
                x=subset["TOTAL"],
                y=subset["DEPARTAMENTO"],
                name=sex,
                orientation="h",
                marker={"color": color},
                hovertemplate="<b>%{y}</b><br>%{fullData.name}: %{x:,}<extra></extra>",
            )
        )
    fig.update_layout(barmode="stack", height=780)
    fig.update_yaxes(categoryorder="array", categoryarray=order)
    return _base_layout(fig, title, "Muertes", "Departamento")


def age_histogram_figure(data: pd.DataFrame) -> go.Figure:
    title = "Distribución de muertes por ciclo de vida"
    if data.empty:
        return _empty_figure(title)

    hover_ranges = data["GRUPO_EDAD_CATEGORIA"].map(AGE_GROUP_LABELS)
    fig = go.Figure(
        go.Bar(
            x=data["GRUPO_EDAD_CATEGORIA"],
            y=data["TOTAL"],
            marker={"color": COLORWAY[3]},
            customdata=hover_ranges,
            hovertemplate="<b>%{x}</b><br>Rango: %{customdata}<br>Muertes: %{y:,}<extra></extra>",
        )
    )
    fig.update_xaxes(tickangle=-25)
    return _base_layout(fig, title, "Grupo de edad", "Muertes")
