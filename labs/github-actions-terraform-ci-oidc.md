# GitHub Actions Terraform CI + AWS OIDC

## Objective

Implement a secure GitHub Actions CI pipeline for Terraform and integrate GitHub Actions with AWS using OpenID Connect (OIDC), avoiding long-lived AWS access keys.

## Project

AWS Cloud Cost Optimization & DevOps Automation Platform

Repository: Satsaheb25/aws-cloud-cost-optimization

AWS Region: ap-south-1

## Architecture

Git push
  |
  v
GitHub Actions
  |
  +--> Terraform fmt
  +--> Terraform init
  +--> Terraform validate
  +--> GitHub OIDC
          |
          v
     AWS IAM OIDC Provider
          |
          v
     GitHubActionsTerraformPlanRole
          |
          v
     Temporary AWS credentials
          |
          v
     Terraform plan

## Workflow

Workflow file: .github/workflows/terraform-ci.yml

The pipeline performs:

1. Repository checkout
2. Terraform setup
3. Terraform format validation
4. Terraform initialization without a backend
5. Terraform validation
6. AWS OIDC authentication on trusted master pushes
7. AWS identity verification
8. Terraform plan

## Pull Request Security Model

Pull requests run Terraform validation but do not receive AWS credentials.

AWS authentication and Terraform plan are restricted to pushes to refs/heads/master.

## AWS OIDC Provider

Provider: token.actions.githubusercontent.com

Audience: sts.amazonaws.com

## IAM Role

Role: GitHubActionsTerraformPlanRole

ARN: arn:aws:iam::872575360359:role/GitHubActionsTerraformPlanRole

Immutable repository subject:

repo:Satsaheb25@213299334/aws-cloud-cost-optimization@1389390803:ref:refs/heads/master

## IAM Permissions

Attached policy: GitHubActionsTerraformPlanReadOnly

The policy provides read-only permissions required for Terraform plan and identity verification.

No AdministratorAccess policy is attached.

## OIDC Troubleshooting

The initial workflow failed with:

Not authorized to perform sts:AssumeRoleWithWebIdentity

The original trust policy used the legacy repository subject format.

Repository metadata was retrieved from GitHub:

- Owner ID: 213299334
- Repository ID: 1389390803

The IAM trust policy was updated to use the immutable repository subject and restrict access to master.

The workflow subsequently completed successfully.

## Final Validation

GitHub Actions successfully completed:

- Terraform Format Check
- Terraform Init
- Terraform Validate
- Configure AWS credentials
- Verify AWS identity
- Terraform Plan

AWS credentials were obtained through GitHub OIDC and AWS STS rather than long-lived access keys.

## Security Considerations

- No long-lived AWS access keys are stored in GitHub.
- GitHub OIDC provides temporary AWS credentials.
- IAM trust is restricted to the repository.
- IAM trust is restricted to the master branch.
- AWS permissions are read-only.
- Pull requests do not receive AWS credentials.
- Terraform backend initialization is disabled for CI validation.
- The workflow does not create, modify, or delete AWS infrastructure.

## Interview Explanation

### What did you implement?

I implemented GitHub Actions CI for Terraform and integrated GitHub Actions with AWS using OIDC. Trusted pushes to master can assume a least-privilege AWS IAM role using temporary credentials and execute Terraform plan.

### Why use OIDC?

OIDC avoids storing long-lived AWS access keys in GitHub Secrets. GitHub Actions receives temporary credentials through AWS STS.

### How did you secure the trust relationship?

The IAM trust policy uses the GitHub OIDC audience and immutable repository subject containing the owner ID, repository ID, and master branch.

### How did you troubleshoot the initial failure?

The initial OIDC trust relationship used the legacy repository subject. I retrieved the repository and owner IDs from GitHub, updated the IAM trust policy to the immutable subject format, and successfully reran the workflow.

### Why don't pull requests receive AWS credentials?

Pull requests can execute workflow code. Restricting AWS authentication to trusted master pushes reduces unnecessary AWS credential exposure.

## Phase Result

Phase 16 - GitHub Actions CI/CD: COMPLETED

Capabilities demonstrated:
- GitHub Actions
- Terraform CI
- Terraform validation
- Terraform plan
- AWS IAM
- AWS STS
- GitHub OIDC
- Temporary AWS credentials
- Least-privilege IAM
- Branch-restricted trust
- CI/CD security controls
