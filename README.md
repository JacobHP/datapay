## Datapay

This is an example project setup for ELT pipeline using dbt on Google Cloud Platform. 

The pipeline itself is very simplistic pulling data from a single source (Reed Jobs API) and just performing some simple transformations and keyword extraction with the goal of understanding salaries in the data engineering space. The infrastructure is obviously overkill for the task but can easily be expanded to larger more complex pipelines.

Pipeline runs daily at midnight UTC.

Visualisation: https://lookerstudio.google.com/reporting/8fd12efe-4903-4c4d-ad12-2bd60905471e

### Architecture:

*TODO*

#### Requirements

*Todo*

### Extract:
Extract is done using docker images stored in Artifact Registry and can be ran as a Cloud Run or Cloud Build job.

The extract process is as follows:

* Pull all listings matching keywords from Reed API

* Pull details for all listings not currently in the target database (this is to save time as Reed API is slow for pulling individual listing details due to request limits)

* Save outputs to GCS


### Load:

* Raw listings and details loaded into ingestion-time partitioned staging tables in bigquery.



### Transform:
Transforms are done in dbt using docker images stored in Artifact Registry and can be ran as a Cloud Run or Cloud Build job. 


### Orchestration

Airflow pipeline or Cloud Workflows runs ELT daily, I have set up the CI with Cloud Workflows as this is a lot more cost effective.

#### Infrastructure

Terraform is used to provision environment objects. Note: You will need an existing project and service account with appropriate permissions.

### CI

Github actions are used to run CI and tests for airflow pipelines

#### Visualisation

Dashboard is built in Google Looker Data Studio and can be found at: https://lookerstudio.google.com/reporting/8fd12efe-4903-4c4d-ad12-2bd60905471e

The salary figures, where available, are calculated as an average of the minimum and maximum salary provided by Reed.

**Note on limitations in visualisation:**

Data Studio is a free tool limited in it's functionality. In particular when filtering by skills (a repeated field/multi-valued dimension) you will observe that selecting multiple skills runs **OR** logic in the filtering rather than **AND**. 

For example, selecting skills 'GCP' and 'AWS' will display jobs containing 'GCP' or 'AWS'. Selecting skill 'Python' and unselecting 'Spark' will display jobs requiring 'Python' even if they also require 'Spark'. 

For skills you don't want displayed I debated adding a 'non skill requirements' filter but this would create more confusion with the **OR** filtering logic. 

I have not found a solution to this problem in Data Studio. As such I would recommend only using the skills filter when interested in averages for more advanced skills (e.g. Spark, Scala, Kafka), and not including the more common skills (e.g. Python, SQL)

