## Datapay

This is an example project setup for ELT pipeline using dbt and airflow on Google Cloud Platform. 

The pipeline itself is very simplistic pulling data from a single source (Reed Jobs API) and just performing some simple transformations and keyword extraction with the goal of understanding salaries in the data engineering space. The infrastructure is obviously overkill for the task but can easily be expanded to larger more complex pipelines.

#### Architecture:

*Todo*

#### Requirements

*Todo*

#### Extract:

Pull all listings matching keywords from Reed API. 

Pull details for all listings not currently in the target database (this is to save time as Reed API is slow for pulling individual listing details due to request limits)

Save outputs to GCS.


#### Load:

Raw listings and details loaded into ingestion-time partitioned staging tables in bigquery.



#### Transform:
*Todo*


#### Orchestration

Airflow pipeline or cloud workflows runs ELT daily.

#### Infrastructure

Terraform is used to provision environment objects. Note: One will need an existing project and service account with appropriate permissions.



#### Visualisation

*Todo* 

