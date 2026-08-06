resource "aws_s3_bucket" "bronze_data" {
  bucket = var.bucket_name

  tags = {
    Environment = var.environment
    Project     = "Batch ELT Pipeline"
    Layer       = "Bronze"
  }
}