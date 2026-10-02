# Phase 18 — Terraform EKS Infrastructure as Code

## Objective

Build a reusable Terraform configuration for deploying an Amazon EKS learning environment while applying AWS cost-control and Infrastructure-as-Code practices.

## Project Context

- Project: AWS Cloud Cost Optimization
- Region: ap-south-1 (Mumbai)
- Infrastructure tool: Terraform
- Cloud provider: AWS
- Kubernetes platform: Amazon EKS
- Environment: Learning

## Terraform Structure

| File | Purpose |
|---|---|
| `versions.tf` | Terraform and AWS provider requirements |
| `variables.tf` | Configurable EKS and node parameters |
| `main.tf` | VPC and EKS infrastructure |
| `outputs.tf` | Cluster and networking outputs |
| `.terraform.lock.hcl` | Provider dependency lock file |

## Infrastructure Design

### VPC

- CIDR: `10.20.0.0/16`
- Availability Zones: 2
- Public subnets: 2
- NAT Gateway: disabled
- Public IP assignment: enabled

NAT Gateway is intentionally disabled for this learning configuration to avoid unnecessary recurring NAT Gateway costs.

### EKS

- Kubernetes version: `1.34`
- EKS managed node group
- Instance type: `t3.small`
- Minimum nodes: `1`
- Desired nodes: `1`
- Maximum nodes: `1`
- CloudWatch log retention: 7 days
- EKS API endpoint: public access enabled

The node group is intentionally kept at a single node for the learning configuration.

## EKS Add-ons

The configuration includes:

- CoreDNS
- kube-proxy
- VPC CNI
- EKS Pod Identity Agent

## Validation Performed

Terraform formatting and validation were completed successfully.

Commands used:

``powershell
terraform -chdir=terraform/eks fmt -check
terraform -chdir=terraform/eks fmt
terraform -chdir=terraform/eks validate
``

Validation result:

`Success! The configuration is valid.`

## Deployment Status

This phase was completed as an Infrastructure-as-Code validation exercise.

`terraform apply` was intentionally **not executed** during this stage.

EKS and supporting AWS resources can generate charges while running. The project therefore focuses on Terraform configuration, validation, review, and Git-based Infrastructure-as-Code practices without leaving unnecessary infrastructure deployed.

## Cost-Control Practices

- NAT Gateway disabled
- Single worker node
- Node autoscaling limited to 1
- CloudWatch retention limited to 7 days
- Terraform state excluded from Git
- `.terraform` working directory excluded from Git
- Provider binaries excluded from Git
- Terraform plan files excluded from Git
- No AWS credentials stored in Terraform files

## Git Hygiene

The repository tracks Terraform source code and `.terraform.lock.hcl`.

The following are intentionally ignored:

- `.terraform/`
- `*.tfstate`
- `*.tfstate.*`
- `*.tfvars`
- `*.tfvars.json`
- `*.tfplan`
- `*.plan`
- Terraform crash logs

## Interview Perspective

This phase demonstrates practical Infrastructure-as-Code knowledge:

1. Define infrastructure declaratively with Terraform.
2. Use reusable modules instead of manually creating every AWS resource.
3. Separate configuration into variables, modules, versions, and outputs.
4. Lock provider dependencies with `.terraform.lock.hcl`.
5. Format and validate Terraform before deployment.
6. Protect Terraform state and sensitive variable files from Git.
7. Design infrastructure with cost controls in mind.
8. Avoid unnecessary infrastructure deployment when the learning objective can be achieved through validation and code review.

## Safety Note

Before running `terraform apply`, review the Terraform plan carefully and confirm the expected AWS resources and estimated costs.

After a temporary lab deployment, destroy resources that are no longer required:

```powershell`r`nterraform -chdir=terraform/eks destroy`r`n```

Do not run `destroy` unless the infrastructure was actually created by this Terraform configuration and you intend to remove it.
