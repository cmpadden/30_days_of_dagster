"""

dagster dev -f day01.py

"""

import dagster as dg


@dg.asset
def a():
    return 1


@dg.asset
def b(a):
    return a + 1


@dg.asset
def c(b):
    return b**2


defs = dg.Definitions(assets=[a, b, c])
