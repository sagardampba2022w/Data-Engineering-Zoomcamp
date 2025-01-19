variable "credentials" {
  description = " my credentials"
  default     = "./keys/my-creds.json"
}


variable "project" {
  description = " project name"
  default     = "gentle-crossbar-378510"
}


variable "location" {
  description = " data and bucket location"
  default     = "US"
}


variable "bq_dataset_name" {
  description = " My big query dataset name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = " bucket name"
  default     = "gentle-crossbar-378510-terra-bucket"
}


variable "gcp_storage_class" {
  description = " bucket storage class"
  default     = "STANDARD"
}