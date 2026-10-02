resource "aws_iam_policy" "eks_workload_s3_readonly" {
  name        = "${var.cluster_name}-workload-s3-readonly"
  description = "Read-only S3 access for an EKS workload identity lab"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = "*"
      }
    ]
  })

  tags = {
    Project     = "aws-cloud-cost-optimization"
    Environment = "learning"
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_role" "eks_workload" {
  name = "${var.cluster_name}-workload-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "pods.eks.amazonaws.com"
        }
        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }
    ]
  })

  tags = {
    Project     = "aws-cloud-cost-optimization"
    Environment = "learning"
    ManagedBy   = "Terraform"
  }
}

resource "aws_iam_role_policy_attachment" "eks_workload_s3_readonly" {
  role       = aws_iam_role.eks_workload.name
  policy_arn = aws_iam_policy.eks_workload_s3_readonly.arn
}

resource "aws_eks_pod_identity_association" "workload" {
  cluster_name    = module.eks.cluster_name
  namespace       = "cost-audit"
  service_account = "cost-audit"
  role_arn        = aws_iam_role.eks_workload.arn
}
