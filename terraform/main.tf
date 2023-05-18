##########
# BUCKETS #
##########

resource "google_storage_bucket" "static" {
    name = "datapay"
    location = var.region
    storage_class = "STANDARD"
    uniform_bucket_level_access = true 
}

#####################
# ARTIFACT REGISTRY #
#####################


resource "google_artifact_registry_repository" "datapay-dbt" {
    location = var.region
    repository_id = "datapay-dbt"
    description = "Repository for datapay dbt image"
    format = "DOCKER"

    docker_config {
        immutable_tags = true
    }
}

resource "google_artifact_registry_repository" "datapay-extract" {
    location = var.region
    repository_id = "datapay-extract"
    description = "Repository datapay extract script"
    format = "DOCKER"

    docker_config {
        immutable_tags = true
    }
}

############
# BigQuery #
############

resource "google_bigquery_dataset" "dataset" {
    dataset_id = "datapay"
    location = "EU" 
}

#########
#API Key#
#########
resource "google_secret_manager_secret" "reed-api"{
    secret_id = "reed_api_key"
    replication {
        user_managed {
            replicas {
                location = var.region
            }
        }
    }
}

resource "google_secret_manager_secret" "service-account"{
    secret_id = "service_account_json"
    replication {
        user_managed {
            replicas {
                location = var.region
            }
        }
    }
}

#################
#Service Account#
#################

# TODO


#############
#Github OIDC#
#############

module "github-actions-runners_gh-oidc" {
    source      = "terraform-google-modules/github-actions-runners/google//modules/gh-oidc"
    version     = "3.1.1"
    project_id  = var.project
    pool_id     = var.pool_id
    provider_id = var.provider_id
    sa_mapping  = {
        "${var.service_account}" = {
            sa_name     = "projects/${var.project}/serviceAccounts/${var.service_account}@${var.project}.iam.gserviceaccount.com"
            attribute   = "attribute.repository/${var.repository}"
        }
    }
}