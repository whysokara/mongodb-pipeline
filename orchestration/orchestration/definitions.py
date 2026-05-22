from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import dbttransform_dbt_assets
from .project import dbttransform_project
from .schedules import schedules

defs = Definitions(
    assets=[dbttransform_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=dbttransform_project),
    },
)