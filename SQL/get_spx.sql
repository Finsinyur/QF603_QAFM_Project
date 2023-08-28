/*
Link to reference document: https://wrds-www.wharton.upenn.edu/documents/1504/IvyDB_US_v5.4_Reference_Manual.pdf
Requires logging into WRDS
*/

SELECT
    A.date AS trading_date,
    A.open AS open_price,
    A.high AS high_price,
    A.low AS low_price,
    A.close AS close_price
    
FROM optionm_all.secprd A
WHERE A.secid = 108105 /*security id of the S&P 500 index*/
AND A.date BETWEEN TO_DATE('2013-03-01', 'YYYY-MM-DD') AND TO_DATE('2023-02-28', 'YYYY-MM-DD')
