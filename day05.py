"""Day 5

DESCRIPTION

    Update the code from asset A to read CSV from disk.

USAGE

    dagster dev -f day05.py

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
def a(context: dg.AssetExecutionContext) -> dg.MaterializeResult:
    if random.random() < 0.5:
        raise Exception("Randomly raised exception!")

    filename = "./data/example.csv"
    context.log.info(f"reading {filename}")
    with open(filename, "r") as f:
        lines = f.readlines()

    return dg.MaterializeResult(metadata={"rows": len(lines)})


@dg.asset(deps=[a], automation_condition=dg.AutomationCondition.on_cron("*/10 * * * *"))
def b(): ...


@dg.asset(deps=[b], automation_condition=dg.AutomationCondition.eager())
def c(): ...


defs = dg.Definitions(assets=[a, b, c])
