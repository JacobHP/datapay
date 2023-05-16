WITH technologies AS (
    SELECT *
    FROM
    UNNEST([
        'Spark',
        'PySpark',
        'AWS',
        'GCP',
        'Azure',
        'Scala',
        'Python',
        'Java',
        'SQL',
        'Airflow',
        'Dataflow',
        'Beam',    
        'Dbt',
        'Dagster',
        'Prefect',
        'Kafka',
        'Snowflake',
        'Databricks',
        'Fivetran',
        'Kubernetes',
        'Docker',
        'Terraform',
    'Bigquery',
        'Postgres',
        'MongoDB',
        'Redshift',
        'Athena',
        'Datalake',
        'Lakehouse',
        'Hive',
        'Flink',
        'Graph' ]) AS skill
)


, details AS (
    SELECT * except (jobUrl, jobDescription, 
        yearlyMaximumSalary, maximumSalary, yearlyMinimumSalary, minimumSalary),

    CASE WHEN currency = 'EUR' THEN 0.88 * yearlyMaximumSalary 
        ELSE yearlyMaximumSalary END AS yearlyMaximumSalary,
    CASE WHEN currency = 'EUR' THEN 0.88 * yearlyMinimumSalary 
        ELSE yearlyMinimumSalary END AS yearlyMinimumSalary,
    CASE WHEN currency = 'EUR' THEN 0.88 * maximumSalary 
        ELSE maximumSalary END AS maximumSalary,
    CASE WHEN currency = 'EUR' THEN 0.88 * minimumSalary 
        ELSE minimumSalary END AS minimumSalary,

    regexp_replace(
    regexp_replace(
        regexp_replace(
            jobDescription, 
            r'(&)([^&;]*)(;)', r'<\2>'
            ),r'\<[^<>]*\>',    ' '
        ), 
        r'\s+', ' ') as jobDescription

    FROM `datapay.int_details`
)

, splitted as (
    SELECT jobId, SPLIT(LOWER(jobDescription), ' ') AS description_split
    FROM details
)

, unnested AS (
    SELECT jobId, REGEXP_REPLACE(description_term, r'[^a-zA-Z]', '') AS description_term
    FROM splitted,
    UNNEST(description_split) AS description_term
)

, skills AS (
    SELECT a.jobId,  ARRAY_AGG(DISTINCT b.skill) AS skill_requirements
    FROM unnested a 
    INNER JOIN technologies b
    ON a.description_term LIKE CONCAT('%', LOWER(b.skill), '%')
    GROUP BY a.jobId
)

SELECT a.*, b.skill_requirements
FROM details a
LEFT JOIN skills b
ON a.jobId = b.jobId