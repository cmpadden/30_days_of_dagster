"""Day 6

DESCRIPTION

    Update the code from yesterday to include meaningful definition time and runtime metadata about asset A. Also log something useful to the event log.

USAGE

    dagster dev -f day06.py

"""

import random

import dagster as dg


@dg.asset(
    automation_condition=dg.AutomationCondition.on_cron("* * * * *"),
    retry_policy=dg.RetryPolicy(
        max_retries=5,
        delay=1,
    ),
    metadata={"definition_time_metadata": "Hello!"},  # definition-time metadata
)
def a(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    if random.random() < 0.5:
        raise Exception("Randomly raised exception!")

    filename = "./data/example.csv"
    context.log.info(f"reading {filename}")
    with open(filename, "r") as f:
        lines = f.readlines()

    return dg.MaterializeResult(metadata={"rows": len(lines)})  # runtime metadata


@dg.asset(deps=[a], automation_condition=dg.AutomationCondition.on_cron("*/10 * * * *"))
def b(): ...


@dg.asset(deps=[b], automation_condition=dg.AutomationCondition.eager())
def c(): ...


defs = dg.Definitions(assets=[a, b, c])
