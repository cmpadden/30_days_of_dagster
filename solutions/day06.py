
from dagster import asset, AssetExecutionContext, MetadataValue
import pandas as pd

# https://youtu.be/RSUk6DU531w

@asset(
    owners=["lopp@dagsterlabs.com"],
    tags={'layer': 'bronze'},
    kinds={'pandas', 'csv'},
) 
def bike_raw(context: AssetExecutionContext):
    """ Reads in the raw bike sales data from a local csv file. TODO: pull the file from the web dynamically """
    df = pd.read_csv('solutions/bike_info.csv')
    df.columns = df.columns=['index','junk', 'bike', 'msrp', 'price', 'brand','category','type','details', 'junk2']
    df = df.drop(['index', 'junk', 'junk2', 'details'], axis=1)
    bikes = df.dropna()
    nrow = len(bikes)
    context.log.info(f"Parsed a csv file and now have {nrow}")
    context.add_output_metadata({
       "rows": nrow,
       "head": MetadataValue.md(bikes.head().to_markdown()),
       "columns": MetadataValue.md(str(bikes.columns))  
    })
    return bikes 

@asset(
    deps=[bike_raw]
) 
def b(context: AssetExecutionContext): ... 

@asset(
    deps=[b]
) 
def c(): ...

