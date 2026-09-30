output "aws_account_id" {
  description = "AWS account ID used by Terraform"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_arn" {
  description = "AWS identity ARN used by Terraform"
  value       = data.aws_caller_identity.current.arn
}

output "aws_region" {
  description = "AWS region used by Terraform"
  value       = data.aws_region.current.region
}

output "terraform_s3_bucket_name" {
  description = "Name of the S3 bucket managed by Terraform"
  value       = aws_s3_bucket.terraform_lab.bucket
}

