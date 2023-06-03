select * EXCEPT(date, jobUrl, jobDescription, employerProfileId, employerProfileName),
  date AS createdDate
FROM `datapay.stg_listings`
WHERE DATE(_PARTITIONTIME) = CURRENT_DATE()