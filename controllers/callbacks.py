from __future__ import annotations

from dash import Input, Output

from controllers.dashboard_state import build_dashboard_state


def register_callbacks(app) -> None:
    @app.callback(
        Output("kpi-total", "children"),
        Output("kpi-departments", "children"),
        Output("kpi-cities", "children"),
        Output("kpi-main-cause", "children"),
        Output("department-map", "figure"),
        Output("monthly-line", "figure"),
        Output("violent-cities-bar", "figure"),
        Output("lowest-mortality-pie", "figure"),
        Output("top-causes-table", "data"),
        Output("sex-department-bar", "figure"),
        Output("age-histogram", "figure"),
        Input("department-filter", "value"),
        Input("sex-filter", "value"),
        Input("month-filter", "value"),
    )
    def update_dashboard(departments, sexes, month_range):
        state = build_dashboard_state(departments, sexes, month_range)
        kpis = state["kpis"]
        figures = state["figures"]

        return (
            kpis["total_deaths"],
            kpis["departments"],
            kpis["cities"],
            kpis["main_cause"],
            figures["department-map"],
            figures["monthly-line"],
            figures["violent-cities-bar"],
            figures["lowest-mortality-pie"],
            state["top_causes"],
            figures["sex-department-bar"],
            figures["age-histogram"],
        )
