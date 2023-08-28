# Import WRDS library
import wrds
import pandas as pd

def read_sql_script(fname, db, date_cols = ['trading_date']):
    fd = open(fname, 'r')
    sqlFile = fd.read()
    fd.close()

    df = db.raw_sql(sqlFile, date_cols=date_cols)

    return df

def main():
    # Establish live connection; requires user login (passwords will be masked)
    db = wrds.Connection()

    # Get VIX
    # library = 'cboe_all', table = 'cboe' 
    vix_fn = "./SQL/get_vix.sql"
    df_vix = read_sql_script(vix_fn, db)
    df_vix.to_csv('./data/vix_20130301_20230228.csv', index = False)
    print('VIX data extracted')

    # Get S&P 500 Index
    # S&P 500 index price:  library='optionm_all', table='secprd'
    spx_fn = "./SQL/get_spx.sql"
    df_spx = read_sql_script(spx_fn, db)
    df_spx.to_csv('./data/spx_20130301_20230228.csv', index = False)
    print('SPX data extracted')

    # Get S&P 500 Call, Put options volume and flag
    # volume: library = optionm_all, table = opvold
    opvol_fn = "./SQL/get_option_volume.sql"
    df_opvol = read_sql_script(opvol_fn, db)
    df_opvol.to_csv('./data/opvol_20130301_20230228.csv', index = False)
    print('option volume data extracted')

if __name__ == "__main__":
    main()

