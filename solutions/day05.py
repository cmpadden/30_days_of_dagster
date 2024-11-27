from dagster import asset   

# https://youtu.be/jNCaAYA-MVU

import pandas as pd

@asset 
def bike_raw():
    df = pd.read_csv('solutions/bike_info.csv')
    print(df)
    return df

@asset(
    deps=[bike_raw]
) 
def b(): ... 

@asset(
    deps=[b]
) 
def c(): ...

bike_raw()