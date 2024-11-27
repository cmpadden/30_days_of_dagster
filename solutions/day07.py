
from dagster import asset, AssetExecutionContext, MetadataValue
import pandas as pd

# https://youtu.be/u9V0As2RZ5k

@asset(
    owners=["lopp@dagsterlabs.com"],
    tags={'layer': 'bronze'},
    kinds={'pandas', 'csv'},
) 
def bike_raw_cleaned(context: AssetExecutionContext):
    """ Reads in the raw bike sales data from a local csv file. TODO: pull the file from the web dynamically """
    df = pd.read_csv('solutions/bike_info.csv')
    df.columns = df.columns=['index','junk', 'bike', 'msrp', 'price', 'brand','category','type','details', 'junk2']
    df = df.drop(['index', 'junk', 'junk2', 'details'], axis=1)
    bikes = df.dropna()
    bikes['price'] = bikes['price'].str.replace(',', '')
    bikes['price'] = bikes['price'].str.replace('$', '').astype(float)
    nrow = len(bikes)
    context.log.info(f"Parsed a csv file and now have {nrow}")
    context.add_output_metadata({
       "rows": nrow,
       "head": MetadataValue.md(bikes.head().to_markdown()),
       "columns": MetadataValue.md(str(bikes.columns))  
    })

    bikes.to_csv("bike_raw_cleaned.csv")

    return 

@asset(
   deps=[bike_raw_cleaned]
) 
def bikes_summary(context: AssetExecutionContext): 

    bike_raw_cleaned: pd.DataFrame = pd.read_csv("bike_raw_cleaned.csv")

    context.log.info(bike_raw_cleaned)
    bike_summary = bike_raw_cleaned.groupby('type')['price'].mean()
    print(bike_summary)
    return 

@asset(
    deps=[bikes_summary]
) 
def c(): ...

