from __future__ import annotations

from models.analytics import (
    deaths_by_age_group,
    deaths_by_department,
    deaths_by_month,
    deaths_by_sex_department,
    filter_deaths,
    kpi_summary,
    lowest_mortality_cities,
    top_causes,
    violent_cities,
)
from models.data_loader import load_deaths, load_geojson, load_reference_data
from views.figures import (
    age_histogram_figure,
    department_map_figure,
    lowest_mortality_pie_figure,
    monthly_line_figure,
    sex_department_bar_figure,
    violent_cities_bar_figure,
)


def build_dashboard_state(
    departments: list[str] | None = None,
    sexes: list[str] | None = None,
    month_range: list[int] | tuple[int, int] | None = None,
) -> dict:
    deaths = load_deaths()
    reference = load_reference_data()
    causes = reference["causes"]
    department_reference = reference["departments"]
    filtered = filter_deaths(deaths, departments, sexes, month_range)

    return {
        "kpis": kpi_summary(filtered, causes),
        "figures": {
            "department-map": department_map_figure(
                deaths_by_department(filtered, department_reference), load_geojson()
            ),
            "monthly-line": monthly_line_figure(deaths_by_month(filtered)),
            "violent-cities-bar": violent_cities_bar_figure(violent_cities(filtered)),
            "lowest-mortality-pie": lowest_mortality_pie_figure(
                lowest_mortality_cities(filtered)
            ),
            "sex-department-bar": sex_department_bar_figure(
                deaths_by_sex_department(filtered, department_reference)
            ),
            "age-histogram": age_histogram_figure(deaths_by_age_group(filtered)),
        },
        "top_causes": top_causes(filtered, causes).to_dict("records"),
    }
