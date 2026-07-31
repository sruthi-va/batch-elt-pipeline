provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "bronze_data" {
  bucket = "nyc-taxi-bronze-sruthi"
}