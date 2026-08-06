variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}


variable "bucket_name" {
  description = "S3 bucket name for bronze data"
  type        = string
  default     = "nyc-taxi-bronze-sruthi"
}


variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}