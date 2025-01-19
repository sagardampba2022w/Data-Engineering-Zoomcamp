terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.16"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }
}


resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}
