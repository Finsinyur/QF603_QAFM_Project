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
query_historical_prices = read_sql_script('../SQL/get_historical_prices.sql')
query_shares_outstanding = read_sql_script('../SQL/get_shares_outstanding.sql')

# Define query dates (end dates)
dates =\
[
    '20220524',
    '20220823',
    '20221122',
    '20230221',
    '20230523'
]

# Establish live connection; requires user login (passwords will be masked)
db = wrds.Connection() # this will be used as a global variable


def get_historical_prices(isin, start_date, end_date):
    
    print(f'Extracting historical prices for {isin}...')

    df =\
    (
        db
        .raw_sql(
            query_historical_prices.format(isin, start_date, end_date), 
            date_cols = ['trade_date']
            )
    )

    if df.empty:
        print('Dataframe is empty. No results was returned!')
    
    print('--------------------------------------------------')

    return df
        
    

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

    end_date =\
    (
        datetime
        .strptime(date, '%Y%m%d')
    )

    start_date =\
    (
        end_date - timedelta(days = 5*365)
    )

    target_isins =\
    (
        list(df.ISIN)
    )

    start_dates =\
    [
        start_date
        .strftime("%d/%m/%Y")
    ]*len(target_isins)

    end_dates =\
    [
        (
            end_date + timedelta(days = 2)
            )
        .strftime("%d/%m/%Y")
    ]*len(target_isins)

    historical_prices =\
    (
        pd.
        concat(
            map(
                get_historical_prices,
                target_isins,
                start_dates,
                end_dates
            )
        )
    )

    (
        historical_prices
        .to_csv(
            f'../output/historical_prices_{date}.csv',
            index = False
            )
    )

    print('===================================================')
    








