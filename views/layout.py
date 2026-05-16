from __future__ import annotations

from dash import dash_table, dcc, html

from controllers.dashboard_state import build_dashboard_state
from models.data_loader import MONTH_LABELS, load_reference_data


def _department_options() -> list[dict[str, str]]:
    departments = load_reference_data()["departments"]
    return [
        {"label": row["DEPARTAMENTO"], "value": row["DPTO"]}
        for _, row in departments.iterrows()
    ]


def _sex_options() -> list[dict[str, str]]:
    return [{"label": sex, "value": sex} for sex in load_reference_data()["sexes"]]


def _month_marks() -> dict[int, str]:
    return {month: label[:3] for month, label in MONTH_LABELS.items()}


def _kpi_card(title: str, element_id: str, value: str) -> html.Div:
    return html.Div(
        className="kpi-card",
        children=[
            html.P(title, className="kpi-title"),
            html.H3(value, id=element_id, className="kpi-value"),
        ],
    )


def _graph_panel(
    title: str, graph_id: str, figure, class_name: str = ""
) -> html.Div:
    return html.Div(
        className=f"panel {class_name}".strip(),
        children=[
            html.H2(title),
            dcc.Loading(
                dcc.Graph(id=graph_id, figure=figure, config={"displaylogo": False})
            ),
        ],
    )


def build_layout() -> html.Main:
    initial_state = build_dashboard_state()
    kpis = initial_state["kpis"]
    figures = initial_state["figures"]
    return html.Main(
        className="app-shell",
        children=[
            html.Header(
                className="app-header",
                children=[
                    html.Div(
                        children=[
                            html.P("Colombia, 2019", className="eyebrow"),
                            html.H1("Análisis interactivo de mortalidad no fetal"),
                            html.H4("Carlos Enrique Jiménez Avendaño"),
                            html.H4("Gustavo Alberto Guerrero Polanco"),
                            html.H4("Osman Angulo"),
                        ]
                    ),
                    html.Div(
                        className="source-pill",
                        children="Fuente: DANE - Estadísticas vitales",
                    ),
                ],
            ),
            html.Section(
                className="filters-panel",
                children=[
                    html.Div(
                        className="filter-control",
                        children=[
                            html.Label("Departamento"),
                            dcc.Dropdown(
                                id="department-filter",
                                options=_department_options(),
                                multi=True,
                                placeholder="Todos",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-control",
                        children=[
                            html.Label("Sexo"),
                            dcc.Dropdown(
                                id="sex-filter",
                                options=_sex_options(),
                                multi=True,
                                placeholder="Todos",
                            ),
                        ],
                    ),
                    html.Div(
                        className="filter-control filter-control-wide",
                        children=[
                            html.Label("Mes"),
                            dcc.RangeSlider(
                                id="month-filter",
                                min=1,
                                max=12,
                                step=1,
                                value=[1, 12],
                                marks=_month_marks(),
                                allowCross=False,
                            ),
                        ],
                    ),
                ],
            ),
            html.Section(
                className="kpi-grid",
                children=[
                    _kpi_card("Muertes registradas", "kpi-total", kpis["total_deaths"]),
                    _kpi_card("Departamentos", "kpi-departments", kpis["departments"]),
                    _kpi_card("Municipios", "kpi-cities", kpis["cities"]),
                    _kpi_card("Principal causa", "kpi-main-cause", kpis["main_cause"]),
                ],
            ),
            html.Section(
                className="dashboard-grid",
                children=[
                    _graph_panel(
                        "Distribución total por departamento",
                        "department-map",
                        figures["department-map"],
                        "wide",
                    ),
                    _graph_panel("Muertes por mes", "monthly-line", figures["monthly-line"]),
                    _graph_panel(
                        "Cinco ciudades con más homicidios X95",
                        "violent-cities-bar",
                        figures["violent-cities-bar"],
                    ),
                    _graph_panel(
                        "Diez ciudades con menor mortalidad registrada",
                        "lowest-mortality-pie",
                        figures["lowest-mortality-pie"],
                    ),
                    html.Div(
                        className="panel",
                        children=[
                            html.H2("Diez principales causas de muerte"),
                            dash_table.DataTable(
                                id="top-causes-table",
                                columns=[
                                    {"name": "Código", "id": "Código"},
                                    {"name": "Causa de muerte", "id": "Causa de muerte"},
                                    {"name": "Total", "id": "Total", "type": "numeric"},
                                ],
                                data=initial_state["top_causes"],
                                page_size=10,
                                sort_action="native",
                                style_as_list_view=True,
                                style_cell={
                                    "fontFamily": "Inter, Segoe UI, sans-serif",
                                    "fontSize": "13px",
                                    "padding": "10px",
                                    "whiteSpace": "normal",
                                    "height": "auto",
                                    "textAlign": "left",
                                },
                                style_header={
                                    "fontWeight": "700",
                                    "backgroundColor": "#e9eef2",
                                    "border": "0",
                                },
                                style_data={"border": "0", "borderBottom": "1px solid #e5e7eb"},
                                style_cell_conditional=[
                                    {"if": {"column_id": "Código"}, "width": "90px"},
                                    {"if": {"column_id": "Total"}, "width": "100px"},
                                ],
                            ),
                        ],
                    ),
                    _graph_panel(
                        "Muertes por sexo y departamento",
                        "sex-department-bar",
                        figures["sex-department-bar"],
                        "wide",
                    ),
                    _graph_panel(
                        "Histograma por grupo de edad",
                        "age-histogram",
                        figures["age-histogram"],
                        "wide",
                    ),
                ],
            ),
        ],
    )
