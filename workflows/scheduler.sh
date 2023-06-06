#!/usr/bin/env bash

PROJECT=$(gcloud config get-value project)
SERVICE_ACCOUNT=$(gcloud iam service-accounts list | grep "Default compute service account" | awk '{print $5}')

if gcloud scheduler jobs list --location="europe-west1" | grep -q "reed_pipeline"; then
    echo "y" | gcloud scheduler jobs delete reed_pipeline --location "europe-west1"
fi

gcloud scheduler jobs create http reed_pipeline --location="europe-west1" --schedule="0 0 * * *" \
    --uri="https://workflowexecutions.googleapis.com/v1/projects/${PROJECT}/locations/europe-west1/workflows/reed_workflow/executions" \
    --message-body="{\"argument\":\"{\\\"extractImage\\\":\\\"europe-west1-docker.pkg.dev/${PROJECT}/datapay-extract/extract:latest\\\", \\\"dbtImage\\\":\\\"europe-west1-docker.pkg.dev/${PROJECT}/datapay-dbt/dbt:latest\\\", \\\"locationId\\\":\\\"europe-west1\\\"}\"}" \
    --time-zone="UTC" --oauth-service-account-email=$SERVICE_ACCOUNT

echo "Schedule deployed successfully!"