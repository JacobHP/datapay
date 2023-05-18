
variable "project" {
  type        = string
  description = "The GCP Project to use"
}

variable "sa_file" {
  type        = string
  description = "The Service Account to use for running Terraform"
}

variable "region" {
  type        = string
  description = "The GCP region to use"
}

variable "zone" {
  type        = string
  description = "The GCP zone to use"
}

variable "service_account" {
  type        = string 
  description = "Service Account email"
}

variable "pool_id" {
  type        = string 
  description = "gh oidc pool id"
}

variable "provider_id" {
  type        = string 
  description = "gh oidc provider id"
}

variable "repository" {
  type        = string 
  description = "gh repo - <USER>/<REPOSITORY>"
}