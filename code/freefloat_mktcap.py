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

# Define sql file names
# these will be used as a global variable
query_freefloat = read_sql_script('../SQL/get_freefloat.sql')

db = wrds.Connection() # this will be used as a global variable

def get_historical_prices(isin, date):
    
    print(f'Extracting free float shares for {isin}...')

    df =\
    (
        db
        .raw_sql(
            query_freefloat.format(isin, date)
            )
    )

    if df.empty:
        print('Dataframe is empty. No results was returned!')
    
    print('--------------------------------------------------')

    return df

dates =\
[
    '20220524',
    '20220823',
    '20221122',
    '20230221',
    '20230523'
]

for date in dates:
    print(f'===================== {date} =====================')
    df =\
    (
        pd
        .read_excel(
            "../output/target_stock_universe.xlsx", 
            sheet_name = date
        )
        .set_index('Ticker')
    )

    target_isins =\
    (
        list(df.ISIN)
    )

    dates =\
    [
        datetime
        .strptime(date, '%Y%m%d')
        .strftime("%d/%m/%Y")
        
    ] * len(target_isins)

    freefloat_shares =\
    (
        pd.
        concat(
            map(
                get_historical_prices,
                target_isins,
                dates
            )
        )
    )

    freefloat_shares =\
    (
        freefloat_shares
        .loc[
            freefloat_shares['value_date']
            == 
            freefloat_shares['value_date'].max()
            ]
    )

    freefloat_shares['consolidated_market_value'] *= 1000000

    freefloat_shares['consolidated_shares_outstanding'] *= 1000

    freefloat_shares['free_float'] /= 100

    freefloat_shares['free_float_market_value'] =\
    (
        freefloat_shares['consolidated_market_value']
        *
        freefloat_shares['free_float']
    )

    freefloat_shares =\
    (
        freefloat_shares
        .sort_values(
            by = 'free_float_market_value',
            ascending = False
        )
    )

    (
        freefloat_shares
        .to_csv(
            f'../output/freefloat_marcap_{date}.csv',
            index = False
            )
    )

    print('===================================================')

