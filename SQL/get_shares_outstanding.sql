/*
Link to reference document: 
- Reference manual: https://wrds-www.wharton.upenn.edu/documents/1505/QADDatabaseSchemaDatastreamv1-1-6-20190530-.pdf
Requires logging into WRDS
*/


SELECT
    C.eventdate AS date,
    A.dsseccode AS security_code,
    A.dssecname AS security_name,
    A.primexchmnem AS primary_exchange,
    A.primqtinfocode AS refinitiv_code,
    B.isin AS isin_code,
    C.numshrs AS shares_outstanding
    
FROM
    tr_ds_equities.ds2security A

INNER JOIN
    tr_ds_equities.ds2isinchg B
ON
    A.dsseccode = B.dsseccode

INNER JOIN
    tr_ds_equities.ds2numshares C
ON
    A.primqtinfocode = C.infocode
    
WHERE
    B.isin = '{0}'
AND
    EXTRACT(YEAR FROM C.eventdate) = '{1}'

ORDER BY C.eventdate
