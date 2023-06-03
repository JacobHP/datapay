WITH cte AS (
    SELECT *, 
        ROW_NUMBER() OVER (PARTITION BY jobId ORDER BY datePosted DESC) AS rn 
    FROM `datapay.stg_details`
    WHERE jobId IN (
        SELECT jobId 
        FROM `datapay.stg_listings`
        WHERE DATE(_PARTITIONTIME) = CURRENT_DATE()
    )
)

SELECT * EXCEPT (rn)
FROM cte  
WHERE rn=1