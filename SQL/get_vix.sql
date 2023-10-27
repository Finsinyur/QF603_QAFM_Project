/*
Link to reference document: https://wrds-www.wharton.upenn.edu/pages/get-data/cboe-indexes/cboe-indexes/
Requires logging into WRDS
*/

SELECT
    A.date AS trading_date,
    A.vixo AS open_price,
    A.vixh AS high_price,
    A.vixl AS low_price,
    A.vix AS close_price

FROM cboe_all.cboe A

WHERE A.date BETWEEN TO_DATE('2013-03-01', 'YYYY-MM-DD') AND TO_DATE('2023-02-28', 'YYYY-MM-DD')
