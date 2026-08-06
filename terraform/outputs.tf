output "bronze_bucket_name" {
  description = "Name of the Bronze S3 bucket"
  value       = aws_s3_bucket.bronze_data.bucket
}