"""Day 4

DESCRIPTION

    Update asset A so that it fails half the time. Find a way to make the pipeline automatically more robust.

USAGE

    dagster dev -f day04.py

"""

import random

import dagster as dg


@dg.asset(
    automation_condition=dg.AutomationCondition.on_cron("* * * * *"),
    retry_policy=dg.RetryPolicy(
        max_retries=5,
        delay=1,
    ),
)
def a():
    if random.random() < 0.5:
        raise Exception("Randomly raised exception!")


@dg.asset(deps=[a], automation_condition=dg.AutomationCondition.on_cron("*/10 * * * *"))
def b(): ...


@dg.asset(deps=[b], automation_condition=dg.AutomationCondition.eager())
def c(): ...


defs = dg.Definitions(assets=[a, b, c])
