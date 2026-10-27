# Project Progress

## Overall Status

**Project:** AWS Cloud Cost Optimization
**Status:** Active
**Current Lab:** Terraform EKS Infrastructure as Code
**Region:** ap-south-1
**Date:** 2026-10-02

---

## Phase 1 — Project Setup

- [x] Project directory created
- [x] Git repository structure created
- [x] README created
- [x] Documentation structure created

## Phase 2 — AWS CLI

- [x] AWS CLI installed
- [x] AWS authentication configured
- [x] AWS identity verified using aws sts get-caller-identity

## Phase 3 — Amazon S3 Fundamentals

- [x] S3 bucket created
- [x] Bucket region verified
- [x] Test object created
- [x] Object uploaded
- [x] Object listing verified

## Phase 4 — S3 Versioning

- [x] Bucket Versioning enabled
- [x] Versioning status verified
- [x] Multiple object versions created
- [x] Object metadata verified

## Phase 5 — S3 Delete Marker & Recovery

- [x] Delete Marker created using normal object deletion
- [x] HeadObject behavior verified after Delete Marker creation
- [x] Delete Marker identified using list-object-versions
- [x] Delete Marker removed
- [x] Previous object version became visible again

## Phase 6 — Permanent Cleanup

- [x] Version 2 permanently deleted
- [x] Pre-versioning null version identified
- [x] null version permanently deleted
- [x] All object versions verified as removed
- [x] Bucket confirmed empty
- [x] Bucket deleted
- [x] Final S3 account listing verified

## S3 Lab Result

The S3 lab successfully demonstrated:

1. Object creation
2. S3 Versioning
3. Multiple object versions
4. Delete Markers
5. Object recovery
6. Permanent version deletion
7. Cleanup verification
8. Bucket deletion

## Next Phases

- [x] S3 Lifecycle Policies
- [x] S3 Storage-Class Optimization
- [x] S3 Cost Analysis
- [x] AWS Cost Explorer exercises
- [x] AWS Budgets
- [x] EC2 cost optimization
- [x] EBS volume cleanup
- [x] EBS snapshot cleanup
- [x] Unused Elastic IP analysis
- [ ] Python/Boto3 automation
- [ ] Terraform automation
- [ ] Automated cleanup scripts
- [ ] Testing and documentation
- [ ] Final project review

---

## Phase 8 — S3 Storage Class & Cost Analysis

**Date:** 2026-09-28
**Region:** ap-south-1 (Mumbai)

### Completed

- Reviewed S3 storage classes and access patterns
- Verified S3 Standard as the default storage class
- Changed lifecycle-test/object1.txt to STANDARD_IA
- Verified StorageClass: STANDARD_IA using head-object
- Verified the new storage-class version using list-object-versions
- Confirmed the previous STANDARD version remained as a noncurrent version
- Documented storage-class cost and access considerations

### Key Learning

Storage-class optimization must consider access frequency, retrieval requirements, retention period, resilience requirements, request costs, and minimum storage duration.

S3 Versioning and storage-class selection should be considered together because different object versions can have different storage classes.

### Documentation

- labs/s3-storage-class-cost-analysis.md

### Status

**Completed**

---

## Phase 9 — AWS Cost Explorer & Cost Visibility

**Date:** 2026-09-28
**Region:** ap-south-1 (Mumbai)

### Completed

- Reviewed AWS Cost Explorer
- Verified Cost Explorer API access through AWS CLI
- Analyzed September 2026 billing-period cost
- Queried costs using the UnblendedCost metric
- Analyzed costs by AWS service
- Verified current estimated cost is approximately $0.00 USD
- Connected Cost Explorer analysis with S3 cost optimization practices

### Key Learning

Cost optimization requires visibility into actual cloud spending. Cost Explorer can provide service-level and time-based cost analysis.

### Documentation

- labs/aws-cost-explorer-cost-visibility.md

### Status

**Completed**

---

## Phase 10 — AWS Budgets & Cost Alerts

**Date:** 2026-09-28
**Region:** ap-south-1 (Mumbai)

### Completed

- Created AWS-Learning-Monthly-Budget
- Configured $5 USD monthly cost budget
- Verified current spend of $0.00
- Verified budget utilization of .00%
- Verified forecasted utilization of .00%
- Verified budget health as Healthy
- Verified alert status as OK
- Configured spending notification thresholds

### Key Learning

AWS Budgets provides proactive cost monitoring. Budget alerts allow spending to be investigated before costs become unexpected.

### Documentation

- labs/aws-budgets-cost-alerts.md

### Status

**Completed**
---

## Phase 11 - EC2 Cost Optimization & Resource Audit

**Date:** 2026-10-02
**Region:** ap-south-1 (Mumbai)

### Completed

- Audited EC2 instances using AWS CLI
- Verified no EC2 instances were running
- Audited the default VPC and subnets
- Audited EBS volumes
- Verified no EBS volumes existed
- Audited Elastic IP allocations
- Verified no Elastic IP allocations existed
- Reviewed EC2 instance-type characteristics
- Validated the environment against Cost Explorer service-level data
- Avoided creating unnecessary billable EC2 resources for the demonstration

### Key Learning

Cloud cost optimization starts with resource visibility and inventory. Unused compute, storage, and public IPv4 resources should be identified before creating new infrastructure.

### Documentation

- labs/ec2-cost-optimization-resource-audit.md

### Status

**Completed**
---

## Phase 12 - EBS Cost Optimization

**Date:** 2026-10-02
**Region:** ap-south-1 (Mumbai)

### Completed

- Audited EBS volumes using AWS CLI
- Verified zero EBS volumes
- Verified zero unattached EBS volumes
- Audited account-owned EBS snapshots
- Verified zero EBS snapshots
- Reviewed EBS right-sizing considerations
- Reviewed EBS volume-type selection
- Reviewed gp3 optimization considerations
- Reviewed EBS snapshot retention and cleanup
- Avoided creating unnecessary billable EBS resources

### Key Learning

EBS cost optimization includes identifying unattached volumes, right-sizing storage, selecting appropriate volume types, evaluating gp3, and controlling snapshot retention.

### Cost Safety

No EBS resources were created during this phase.

### Documentation

- labs/ebs-cost-optimization.md

### Status

**Completed - Read-only EBS cost optimization audit**

## Phase 13 - Elastic IP & Network Cost Optimization

- Audited Elastic IP allocations using AWS CLI
- Result: 0 Elastic IP allocations
- Audited NAT Gateways
- Result: 0 NAT Gateways
- Audited Application/Network Load Balancers
- Result: 0 ALB/NLB resources
- Audited Classic Load Balancers
- Result: 0 Classic Load Balancers
- Audited Internet Gateway configuration
- Existing Internet Gateway: igw-08072c34454d5ee8f
- Existing VPC: vpc-0dfe1384592bcb446
- No unnecessary billable networking resources identified
- No networking resources created during the lab
- Documentation: labs/elastic-ip-network-cost-optimization.md
- Status: Completed

## Phase 14 - Python / Boto3 AWS Cost Audit Automation

**Date:** 2026-10-02
**Region:** ap-south-1 (Mumbai)

### Completed

- Verified Python 3.13.7 environment
- Verified Boto3 1.43.104
- Verified Botocore 1.43.104
- Verified AWS CRT 0.36.0 support
- Verified AWS authentication using AWS STS
- Developed read-only Python/Boto3 AWS cost audit automation
- Audited EC2 instances
- Audited EBS volumes
- Audited EBS snapshots
- Audited Elastic IPs
- Audited NAT Gateways
- Audited Load Balancers
- Audited S3 buckets
- Added AWS API error handling
- Added cost-risk classification
- Generated JSON audit report
- Generated CSV audit report
- Added generated reports to .gitignore
- Validated Python syntax with py_compile
- Executed the audit successfully with 0 API errors

### Audit Result

- EC2 Instances: 0
- EBS Volumes: 0
- EBS Snapshots: 0
- Elastic IPs: 0
- NAT Gateways: 0
- Load Balancers: 0
- S3 Buckets: 0
- API Errors: 0

### Safety

The automation is strictly read-only. No AWS resources were created, modified, stopped, or deleted.

### Key Learning

Python and Boto3 can transform repetitive AWS CLI resource audits into reusable automation with structured reporting, exception handling, and future integration with scheduled jobs, CI/CD, Lambda, monitoring, and Terraform.

### Documentation

- labs/python-boto3-cost-audit.md
- scripts/aws_cost_audit.py

### Status

**Completed - Python/Boto3 AWS Cost Audit Automation**


---

## Phase 15 — Terraform / Infrastructure as Code

**Date:** 2026-09-30
**Region:** `ap-south-1`
**Status:** Completed

### Completed

- Installed and verified Terraform
- Configured the AWS provider
- Configured AWS region using a Terraform variable
- Added AWS account and region data sources
- Created an S3 bucket using Terraform
- Ran `terraform init`
- Ran `terraform validate`
- Ran `terraform plan`
- Ran `terraform apply`
- Verified the AWS resource using AWS CLI
- Inspected Terraform outputs
- Inspected Terraform state
- Ran `terraform destroy`
- Verified AWS resource cleanup
- Added Terraform provider lock file
- Added Terraform state and working-directory exclusions to `.gitignore`

### Temporary Resource

S3 bucket:

`sagar-terraform-lab-2026-872575360359`

The bucket was created only for the Terraform lab and destroyed after verification.

### Key Learning

Terraform provides a declarative Infrastructure as Code workflow that allows infrastructure to be defined, reviewed, provisioned, tracked through state, and safely destroyed.

Workflow practiced:

`init → validate → plan → apply → verify → state → destroy`

### Cost Safety

No objects were uploaded to the temporary bucket.

No EC2, NAT Gateway, load balancer, or other compute infrastructure was created.

The Terraform-managed S3 bucket was destroyed after the lab.

### Documentation

- `labs/terraform-infrastructure-as-code.md`
- `terraform/README.md`
- `terraform/provider.tf`
- `terraform/variables.tf`
- `terraform/main.tf`
- `terraform/outputs.tf`

### Interview Perspective

This phase demonstrates practical Infrastructure as Code experience, including declarative configuration, execution planning, resource provisioning, state management, and controlled cleanup.

The project now progresses from AWS CLI administration and cost auditing to automated infrastructure provisioning with Terraform.

### Next Phase

Phase 16 — GitHub Actions CI/CD

## Phase 17 — Kubernetes Deployment

Status: **Completed**

### Completed

- Enabled Docker Desktop Kubernetes.
- Verified Kubernetes node availability.
- Created `aws-cost-optimization` namespace.
- Created Kubernetes Deployment for the AWS Cost Audit application.
- Built and used the Dockerized `aws-cost-audit:ci` image.
- Configured a local container registry for Docker Desktop Kubernetes.
- Verified the image through Kubernetes containerd using `crictl`.
- Successfully started the audit Pod.
- Verified Kubernetes rollout.
- Executed the Python/Boto3 audit application inside Kubernetes.
- Confirmed no AWS resources were created, modified, or deleted.

### Authentication Finding

The Kubernetes Pod does not inherit the host AWS CLI login session.

AWS API calls therefore returned:

`Unable to locate credentials`

No AWS credentials were stored in Kubernetes manifests.

Secure Kubernetes-to-AWS authentication will be implemented in a later phase.

### Current Kubernetes State

- Cluster: Docker Desktop Kubernetes
- Kubernetes: v1.36.1
- Namespace: `aws-cost-optimization`
- Workload: `aws-cost-audit`
- Region: `ap-south-1`
- Pod execution: Successful
- AWS resource changes: None

### Phase 17.1 — Kubernetes Job

**Status: COMPLETED**

Converted the AWS Cost Audit workload from a Kubernetes Deployment to a Kubernetes Job because the audit process is a one-time batch workload that terminates after execution.

### Implementation

- Created `kubernetes/job.yaml`.
- Configured `restartPolicy: Never`.
- Configured Job `backoffLimit: 2`.
- Validated the Job manifest using `kubectl apply --dry-run=client`.
- Removed the previous long-running Deployment.
- Applied the Kubernetes Job successfully.
- Verified Job completion with `kubectl get job,pods`.
- Retrieved application logs using `kubectl logs job/aws-cost-audit`.
- Inspected Job configuration and lifecycle using `kubectl describe job`.

### Troubleshooting

- Identified that the original Deployment was unsuitable for a one-shot audit process.
- Investigated the resulting `CrashLoopBackOff` behavior.
- Replaced the Deployment with a Kubernetes Job.
- Job completed successfully with `1/1` completion and zero failed Pods.
- Application execution revealed `Unable to locate credentials` for AWS API calls.

### Security Finding

The Kubernetes workload does not automatically inherit the host AWS CLI authentication session.

Static AWS access keys were deliberately not added to Kubernetes YAML or container images.

Secure AWS workload identity will be implemented in a future EKS-based phase.

### Cost Safety

- No AWS resources were created, modified, or deleted by the Kubernetes audit.
- Docker Desktop Kubernetes was used for the local Kubernetes lab.
- The workload executed as a short-lived batch Job.

### Interview Perspective

This phase demonstrates troubleshooting from workload behavior to root cause: Deployment → CrashLoopBackOff → workload classification → Kubernetes Job → successful batch execution → AWS authentication discovery → secure remediation decision.

### Next

Phase 18 — AWS Workload Identity / Amazon EKS.

The objective is to securely allow Kubernetes workloads to call AWS APIs without storing long-lived AWS access keys in Kubernetes.


---

## Phase 18 — AWS Workload Identity / Amazon EKS Infrastructure

**Date:** 2026-10-02
**Region:** `ap-south-1`
**Status:** Terraform infrastructure foundation completed

### Objective

Create a reusable Terraform foundation for Amazon EKS that can later support secure Kubernetes-to-AWS workload identity without storing long-lived AWS credentials in Kubernetes manifests.

### Completed

- Created Terraform EKS infrastructure configuration
- Added reusable Terraform variables
- Added AWS provider version constraints
- Added VPC configuration using the Terraform AWS VPC module
- Added Amazon EKS configuration using the Terraform AWS EKS module
- Configured two Availability Zones
- Configured two public subnets
- Disabled NAT Gateway to reduce unnecessary lab costs
- Configured a single `t3.small` EKS worker node
- Limited node scaling to 1 minimum, 1 desired, and 1 maximum
- Configured CloudWatch log retention for 7 days
- Configured EKS managed add-ons
- Added Terraform outputs for cluster and networking information
- Added `.terraform.lock.hcl`
- Updated `.gitignore` to exclude Terraform working directories and state files
- Ran `terraform fmt -check`
- Ran `terraform fmt`
- Ran `terraform validate`
- Validation completed successfully
- Reviewed Terraform configuration for credentials and cost risks
- Did not execute `terraform apply`

### Terraform Validation

Validation completed successfully with Terraform.

### Cost Safety

The EKS configuration was validated without deployment.

Cost-control measures include:

- NAT Gateway disabled
- One worker node
- Minimum/desired/maximum node count set to 1
- CloudWatch log retention limited to 7 days
- Terraform state excluded from Git
- Terraform working directory excluded from Git

### Security

No AWS access keys or secrets are stored in the Terraform source files.

The EKS API endpoint is configured for public access for learning purposes. Production environments should use an access design appropriate to their security requirements.

Secure Kubernetes-to-AWS workload authentication remains the next implementation objective.

### Git Hygiene

Tracked:

- Terraform `.tf` source files
- `.terraform.lock.hcl`
- Terraform documentation

Ignored:

- `.terraform/`
- Terraform state files
- Terraform variable files
- Terraform plan files
- Terraform crash logs

### Documentation

- `terraform/eks/README.md`
- `terraform/eks/versions.tf`
- `terraform/eks/variables.tf`
- `terraform/eks/main.tf`
- `terraform/eks/outputs.tf`

### Interview Perspective

This phase demonstrates how Terraform can be used to define reusable AWS infrastructure while applying cost, security, validation, and Git hygiene practices.

The configuration provides the infrastructure foundation required for a future EKS workload-identity implementation.

### Next

Continue Phase 18 with secure AWS workload identity for Kubernetes workloads, avoiding long-lived AWS access keys in Pods.

---

## Phase 22 - AWS Cost Audit Unit Testing and CI Validation

**Date:** 2026-10-11
**Status:** Local implementation and validation completed; remote CI pending

### Completed

- Added offline unit tests for JSON report generation.
- Added offline unit tests for CSV resource-field validation.
- Added a test for CSV output with zero resources.
- Ran all three tests successfully.
- Compiled the audit script and test module successfully.
- Added the unit-test command to GitHub Actions.
- Added Git ignore rules for Terraform state backups and the temporary state-address file.

### Validation

- Unit tests: 3 passed.
- Python compilation: passed.
- Git diff whitespace check: passed.
- GitHub Actions remote execution: pending.

### Cost and Security Safety

- No AWS resources were created or modified for unit testing.
- Terraform state files and backups remain excluded from Git.
- The existing AWS audit remains read-only.

### Documentation

- `labs/phase-22-audit-unit-testing.md`

### Next

Review changes, commit and push the implementation, then verify the GitHub Actions result.

---

## Phase 23 - AWS Cost Audit Quality and Security Hardening

**Date:** 2026-10-11
**Status:** Local validation completed; remote CI verification pending

### Completed

- Added four offline tests for successful calls, AWS ClientError, BotoCoreError, and unexpected exceptions.
- Expanded the unit test suite from three to seven tests.
- Added `scripts/check_secrets.py` to scan Git-tracked files for common AWS credential patterns.
- Integrated the credential-pattern check into the Python GitHub Actions job.
- Added `labs/phase-23-security-hardening.md`.

### Validation

- Unit tests: 7 passed.
- Python compilation: passed.
- Credential-pattern check: passed; 45 tracked files scanned at the last check.
- Git diff check: no whitespace errors reported; line-ending warnings appeared.
- AWS infrastructure changes: none performed for this phase.

### Cost and Security Safety

- Tests use local files and mocked failures rather than live AWS API calls.
- The credential-pattern check is a basic safeguard, not a complete secret scanner.
- Review generated reports before sharing because resource metadata and API errors may contain operational details.
- No Terraform apply or destroy operation was performed.

### Documentation

- `labs/phase-23-security-hardening.md`
- `progress.md`

### Next

Review the complete diff, commit and push the intended changes, and verify the remote GitHub Actions run.

**Status: Completed** — Local validation passed and all GitHub Actions jobs are green.

---

## Phase 24 - AWS Cost Audit Status and Failure Reporting

**Date:** 2026-10-11
**Status:** Local implementation and validation completed; remote CI verification pending

### Completed

- Added `PASS`, `PARTIAL`, and `FAILED` audit statuses.
- Added total, successful, and failed check counts to the JSON report.
- Configured exit code `0` for a full pass and `1` for partial or complete failure.
- Added three offline tests covering all status outcomes.
- Added `labs/phase-24-audit-status.md`.

### Validation

- Unit tests: 10 passed.
- Python compilation: passed.
- Git diff check: passed with no whitespace errors.
- Remote GitHub Actions verification: pending.

### Cost and Security Safety

- Status tests mock the AWS session and audit functions.
- No live AWS resources were created, modified, or deleted for these tests.
- The audit remains read-only.

### Interview Perspective

A reliable audit must distinguish a complete pass from partial visibility and total failure. Exit codes let CI/CD pipelines detect incomplete audits instead of silently treating them as successful.

### Next

Review the complete code and documentation diff, then commit and push the intended Phase 24 changes after approval. Verify GitHub Actions.

## 2026-10-27 — Terraform recovery and Docker validation

- Confirmed the root Terraform configuration initializes and validates.
- Built the local Docker image `aws-cost-audit:final`.
- Confirmed the audit script compiles inside the Docker image.
- Investigated the retired EKS/VPC deployment and removed stale module resources from Terraform state.
- Archived the EKS Terraform configuration for future learning without recreating AWS infrastructure.
- Kept the Terraform state backup in the Git-ignored `backups/` directory.
- Next: validate the final changes, commit and push, then verify GitHub Actions.

## 2026-10-27 - Phase 26: Terraform CI Safety Gates

### Completed
- Removed workflow-wide OIDC token permission; CI retains contents read permission only.
- Removed AWS credential configuration, identity verification, and the live Terraform plan from CI.
- Renamed the Terraform job to Terraform Configuration Validation.
- Retained Terraform formatting, initialization with backend disabled, and validation.
- Preserved the Python validation, unit tests, secret scan, and Docker build checks.

### Validation
- Terraform formatting, initialization, and validation: previously passed locally.
- Python compilation: passed.
- Unit tests: 10 passed.
- Secret-pattern scan: passed; 48 tracked files scanned.
- Workflow diff review: passed; no whitespace errors.

### Cost and Security Safety
- No AWS resources were created, modified, or deleted for these workflow changes.
- Terraform state remains local and Git-ignored.
- CI validates Terraform configuration without AWS credentials or a live plan.

### Next
- Run final local validation.
- Commit and push the workflow and progress documentation.
- Verify the GitHub Actions run.

## 2026-10-27 - Phase 28: Accurate AWS Audit Visibility

### Completed
- Updated resource summaries to distinguish inaccessible AWS resource categories from confirmed zero-resource results.
- Added `UNKNOWN` risk status and a `null` count when an audit category has an API error.
- Added `resource_visibility` to the JSON report, including visibility status and resource count.
- Updated console output to display `UNKNOWN` for inaccessible categories.
- Added regression tests for successful, partial-failure, and total-failure audit outcomes.

### Validation
- Python compilation: passed.
- Unit tests: 10 passed.
- Secret-pattern scan: passed; 48 tracked files scanned.
- `git diff --check`: passed.

### Cost and Security Safety
- Tests use mocked AWS outcomes.
- No AWS resources were created, modified, or deleted for this change.
- The audit remains read-only.

### Interview Perspective
A cost audit must not interpret an API permission failure as proof that no resources exist. Explicit visibility states prevent misleading reports and help CI pipelines distinguish complete results from partial or failed audits.

### Next
- Run final Python and Terraform configuration checks.
- Review the complete diff, commit, and push the changes.


---

## Phase 31 - AWS Audit Report Contract Tests

**Date:** 2026-10-27
**Status:** Completed; GitHub Actions passed.

- Added report-contract tests for required JSON fields and report readability.
- Verified the report structure and required metadata.
- Confirmed the corresponding GitHub Actions workflow completed successfully.
- No AWS infrastructure changes were performed.

## Phase 32 - Audit Report Contract Test Improvements

**Date:** 2026-10-27
**Status:** Local validation passed; commit and remote verification pending.

### Completed
- Added a shared contract assertion to the actual audit-status tests.
- Checked required report fields and read-only mode.
- Verified total checks equal successful checks plus failed checks.
- Verified all seven audit checks are accounted for.
- Verified audit status is PASS, PARTIAL, or FAILED.
- Verified the number of reported errors matches the failed-check count.
- Removed a standalone arithmetic test that did not validate a generated report.

### Validation
- Python compilation: passed.
- Unit tests: 14 passed.
- `git diff --check`: passed; Git displayed a line-ending warning only.

### Cost and Security Safety
- The test suite uses mocked AWS sessions and audit functions.
- No AWS resources were created, modified, or deleted.
- The audit remains read-only.

### Next
- Review documentation and code changes.
- Run final Python, Terraform, and secret-scan checks.
- Commit and push the verified changes.
- Confirm GitHub Actions succeeds.
