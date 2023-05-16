
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
