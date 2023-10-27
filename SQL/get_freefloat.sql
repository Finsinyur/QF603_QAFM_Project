/*
Link to reference document: 
- Reference manual: https://wrds-www.wharton.upenn.edu/documents/1505/QADDatabaseSchemaDatastreamv1-1-6-20190530-.pdf
Requires logging into WRDS
*/

SELECT
    A.dsseccode AS security_code,
    A.dssecname AS security_name,
    A.primexchmnem AS primary_exchange,
    A.primqtinfocode AS refinitiv_code,
    B.isin AS isin_code,
    E.value_date AS value_date,
    E.consolidated_market_value AS consolidated_market_value,
    E.consolidated_shares_outstanding AS consolidated_shares_outstanding,
    E.free_float AS free_float
FROM
    tr_ds_equities.ds2security A
INNER JOIN
    tr_ds_equities.ds2isinchg B
ON
    A.dsseccode = B.dsseccode
LEFT JOIN (
    SELECT
        C.infocode,
        C.valdate AS value_date,
        C.consolmktval AS consolidated_market_value,
        C.consolnumshrs AS consolidated_shares_outstanding,
        D.freefloatpct AS free_float
    FROM
        tr_ds_equities.ds2mktval C
    INNER JOIN
        tr_ds_equities.ds2sharehldgs D
    ON
        C.infocode = D.infocode
    AND
        C.valdate = D.valdate
    WHERE
        C.valdate BETWEEN TO_DATE('01/01/2022', 'DD/MM/YYYY') AND TO_DATE('{1}', 'DD/MM/YYYY')
) AS E
ON
    A.primqtinfocode = E.infocode
WHERE
    B.isin = '{0}';