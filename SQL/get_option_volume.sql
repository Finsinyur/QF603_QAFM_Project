/*
Link to reference document: 
- Reference manual: https://wrds-www.wharton.upenn.edu/documents/1504/IvyDB_US_v5.4_Reference_Manual.pdf
- Data schema: https://wrds-www.wharton.upenn.edu/data-dictionary/optionm_all/opvold/
Requires logging into WRDS
*/

SELECT
    A.date AS trading_date,
    A.cp_flag AS call_or_put,
    A.open_interest AS open_interest,
    A.volume AS volume
    
FROM optionm_all.opvold A
WHERE A.secid = 108105 /*security id of the S&P 500 index*/
AND A.date BETWEEN TO_DATE('2013-03-01', 'YYYY-MM-DD') AND TO_DATE('2023-02-28', 'YYYY-MM-DD')
AND A.cp_flag IN ('C', 'P')
