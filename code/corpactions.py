# Import WRDS library
import wrds
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

def read_sql_script(fname):
    fd = open(fname, 'r')
    sqlFile = fd.read()
    fd.close()

    return sqlFile


# Get current path
this_path = os.path.abspath(os.curdir)
print(this_path)

# Establish live connection; requires user login (passwords will be masked)
db = wrds.Connection() # this will be used as a global variable


# Read sql script for corporate actions
query_corporate_actions =\
(
    read_sql_script('../SQL/get_corporate_actions.sql')
)
      

def get_corporate_actions(isin, start_date, end_date):
    
    print(f'Extracting corporate actions for {isin}...')

    df =\
    (
        db
        .raw_sql(
            query_corporate_actions.format(isin, start_date, end_date)
            )
    )

    if df.empty:
        print('Dataframe is empty. No results was returned!')
    
    print('--------------------------------------------------')

    return df


df =\
(
    pd
    .read_csv(
        "../output/ftse_largemid_rebalancing_summary.csv"
    )
)

corporate_actions = []

for date in df['Post Date'].unique():
        
    target_isins  =\
    (
        list(df
             .loc[
                 df['Post Date'] == date,
                 'ISIN\n'
                 ])
    )

    start_dates =\
    [
        (
            datetime.strptime(date, "%Y-%m-%d")
            -
            timedelta(days = 28)
        ).strftime("%d/%m/%Y")
    ] * len(target_isins)

    end_dates =\
    [
        (
            datetime.strptime(date, "%Y-%m-%d")
            +
            timedelta(days = 28)
        ).strftime("%d/%m/%Y")
    ] * len(target_isins)

    corporate_actions\
        .append(
            pd
            .concat(
                map(
                    get_corporate_actions,
                    target_isins,
                    start_dates,
                    end_dates
                )
            )
        )
    
df_ca =\
(
    pd
    .concat(
        corporate_actions
    )
)

df_ca.to_csv("../output/corporate_actions_summary.csv")
    






