
terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
        }
        google-beta = {
            source = "hashicorp/google-beta"
        }
    }
}

provider "google" {
    credentials = file(var.sa_file)   
    project = var.project
    region = var.region
    zone = var.zone 
}

provider "google-beta" {
    credentials = file(var.sa_file)
    project = var.project
    region = var.region
    zone = var.zone 
}