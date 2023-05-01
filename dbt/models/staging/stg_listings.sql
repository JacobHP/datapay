select * EXCEPT(date, jobUrl, jobDescription, employerProfileId, employerProfileName),
  date AS createdDate
FROM `inbound.reed_listings`