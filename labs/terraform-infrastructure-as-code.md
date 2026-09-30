# Terraform Infrastructure as Code

## Objective

Implement Infrastructure as Code (IaC) using Terraform to provision, verify, manage, and destroy an AWS resource safely.

This lab extends the AWS Cloud Cost Optimization project from manual AWS CLI administration into repeatable infrastructure automation.

## Environment

- OS: Windows 11
- Terraform: v1.16.2
- AWS CLI: 2.36.44
- AWS Region: ap-south-1 (Mumbai)
- AWS Account: 872575360359
- Project: AWS Cloud Cost Optimization & DevOps Automation Platform

## Terraform Project

Location:

`terraform/`

Files:

- `provider.tf` - Terraform and AWS provider configuration
- `variables.tf` - configurable AWS region
- `main.tf` - AWS data sources and S3 resource
- `outputs.tf` - Terraform outputs
- `README.md` - Terraform lab overview
- `.terraform.lock.hcl` - provider dependency lock file

## Terraform Workflow

The lab followed this Infrastructure as Code workflow:

1. `terraform init`
2. `terraform validate`
3. `terraform plan`
4. `terraform apply`
5. Verify the AWS resource
6. Inspect Terraform state
7. `terraform destroy`
8. Verify AWS cleanup

## AWS Resource

Terraform temporarily created:

- Resource: Amazon S3 bucket
- Bucket: `sagar-terraform-lab-2026-872575360359`
- Region: `ap-south-1`
- Managed by: Terraform

Terraform successfully created the bucket and the AWS CLI was used to verify that the resource existed.

## Terraform State

Terraform state showed the managed resource:

`aws_s3_bucket.terraform_lab`

The state also contained the AWS account identity and region data sources.

After `terraform destroy`, the resource was removed from Terraform state.

## Cleanup

The temporary S3 bucket was destroyed using:

`terraform destroy`

AWS CLI verification after destruction returned a 404 for the bucket, confirming that the temporary lab resource had been removed.

No objects were uploaded to the bucket.

## Cost Safety

This lab was designed to minimize AWS cost:

- Only one temporary S3 bucket was created.
- No objects were uploaded.
- No EC2, NAT Gateway, load balancer, or other compute resources were created.
- The resource was destroyed immediately after verification.
- Terraform state and working files are excluded from Git where appropriate.

## Security Considerations

Terraform state can contain sensitive infrastructure information and should not be committed to a public repository.

The project `.gitignore` excludes:

- Terraform state files
- Terraform working directory
- Terraform variable files
- Terraform crash logs

The `.terraform.lock.hcl` file is intentionally retained because it records provider dependency selections.

## Troubleshooting

### Terraform initialized in an empty directory

If `terraform init` is run from the repository root instead of the Terraform directory, Terraform may report:

`Terraform initialized in an empty directory!`

The correct working directory is:

`C:\Projects\aws-cloud-cost-optimization\terraform`

### AWS authentication

If the AWS login session expires, reauthenticate with:

`aws login`

Then verify:

`aws sts get-caller-identity`

## Interview Perspective

This lab demonstrates the transition from manual AWS administration to Infrastructure as Code.

Key interview points:

- Terraform configuration defines infrastructure declaratively.
- `terraform plan` provides a preview before changes are applied.
- `terraform apply` provisions resources from code.
- Terraform state tracks resources managed by Terraform.
- `terraform destroy` provides controlled cleanup of lab infrastructure.
- Provider lock files improve dependency reproducibility.
- `.gitignore` prevents Terraform state and local working files from being committed.
- The workflow can later be integrated with GitHub Actions for automated validation and deployment workflows.

## Status

Completed - Terraform Infrastructure as Code fundamentals.
