FROM ghcr.io/dbt-labs/dbt-bigquery:1.5.0

ARG PROJECT_ID
ARG BQ_DATASET
ARG DBT_DIR
ARG CREDENTIALS

ENV PROJECT_ID=$PROJECT_ID
ENV BQ_DATASET=$BQ_DATASET
ENV DBT_DIR=$DBT_DIR
ENV CREDENTIALS=$CREDENTIALS   
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/app/auth/gcp-service-account.json
ENV DBT_PROFILES_DIR=/usr/app/dbt/
ENV DBT_PROJECT_DIR=/usr/app/dbt/
ENV TARGET=prod


USER root 

COPY $DBT_DIR/ /usr/app/dbt/
RUN echo ls /usr/app/dbt/
COPY $CREDENTIALS /usr/app/auth/gcp-service-account.json

RUN dbt debug --target=$TARGET

ENTRYPOINT dbt deps && dbt run --target=$TARGET


