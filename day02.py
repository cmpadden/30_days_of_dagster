"""

dagster dev -f day02.py

"""

import dagster as dg


@dg.asset(
    automation_condition=dg.AutomationCondition.on_cron(
        "0 * * * *"
    )  # https://crontab.guru/#0_*_*_*_*
)
def a(): ...


@dg.asset(deps=[a], automation_condition=dg.AutomationCondition.eager())
def b(): ...


@dg.asset(deps=[b], automation_condition=dg.AutomationCondition.eager())
def c(): ...


defs = dg.Definitions(assets=[a, b, c])
