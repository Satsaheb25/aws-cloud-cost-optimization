data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

resource "aws_s3_bucket" "terraform_lab" {
  bucket = "sagar-terraform-lab-2026-872575360359"

  tags = {
    Name        = "Terraform Learning Lab"
    Environment = "learning"
    ManagedBy   = "Terraform"
    Project     = "aws-cloud-cost-optimization"
  }
}
