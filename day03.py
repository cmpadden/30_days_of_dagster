"""Day 3

DESCRIPTION

    Run asset A every minute, asset C every 10 minutes, and asset B only when it needs to be run by C.

USAGE

    dagster dev -f day03.py

"""

import dagster as dg


@dg.asset(
    automation_condition=dg.AutomationCondition.on_cron("* * * * *")
)  # every minute
def a(): ...


@dg.asset(
    deps=[a], automation_condition=dg.AutomationCondition.on_cron("*/10 * * * *")
)  # every 10 minutes
def b(): ...


@dg.asset(
    deps=[b], automation_condition=dg.AutomationCondition.eager()
)  # `eager` runs whenever the upstream asset has been updated
def c(): ...


defs = dg.Definitions(assets=[a, b, c])
