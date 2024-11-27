
from dagster import asset, AssetExecutionContext, MetadataValue, sensor, SensorEvaluationContext, RunRequest, SkipReason, Definitions
import pandas as pd
import os

# https://youtu.be/iroAyNM0kxA

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


@sensor(
        target=["bike_raw_cleaned*"]
)
def run_pipeline_on_csv_change(context: SensorEvaluationContext):
    file_path = "solutions/bike_info.csv"

    # Get the last modified time in seconds since the Epoch
    last_modified_time = os.path.getmtime(file_path)

    if context.cursor is None:
        context.log.info(f"First time through so we are launching a run and updating the cursor")
        context.update_cursor(str(last_modified_time))
        return RunRequest()
    
    if last_modified_time > float(context.cursor):
        context.log.info(f"Cursor value was {context.cursor} which was newer than our last evaluated run which used {str(last_modified_time)}")
        context.update_cursor(str(last_modified_time))
        return RunRequest()
    
    return SkipReason(f"The file was last updated at {context.cursor} and we observed the same modified time in this tick: {str(last_modified_time)}")
    
    

defs = Definitions(
    assets=[bike_raw_cleaned, bikes_summary,  c],
    sensors=[run_pipeline_on_csv_change]
)