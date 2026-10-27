# AWS Cloud Cost Optimization & DevOps Automation Platform

A hands-on AWS learning project focused on resource visibility,
cost-awareness, cleanup, Python/Boto3 automation, Docker, Terraform
validation, and CI/CD security.

**Status:** Active --- hands-on AWS cost optimization and DevOps
learning project.

> **Scope:** The current audit inventories resources and reports
> visibility/errors. It is not a complete billing or spend-analysis
> engine; that would require billing data integration.

## Features

-   Read-only inventory audit for EC2 instances, EBS volumes and
    snapshots, Elastic IPs, NAT gateways, load balancers, and S3
    buckets.
-   JSON and CSV reports.
-   Explicit `UNKNOWN` status when an AWS API request fails, rather than
    incorrectly reporting zero resources.
-   Dockerized audit execution.
-   Python unit tests and secret-pattern checks.
-   GitHub Actions validation for Python, tests, secret checks, Docker
    builds, and Terraform configuration.
-   Terraform configuration-only validation.
-   Documented S3 versioning and cleanup lab.

## Architecture

``` text
Python + Boto3 audit
  ├── EC2 / EBS / Snapshots
  ├── Elastic IPs / NAT gateways / Load balancers
  └── S3 buckets
          |
          v
Visibility classification + API error details
          |
          +--> JSON report
          +--> CSV report

GitHub Actions
  ├── Python validation and tests
  ├── Secret-pattern checks
  ├── Docker build
  └── Terraform fmt / init / validate
```

The audit is designed to be read-only: it inspects resources and reports
errors; it does not create, modify, or delete AWS resources.

## Technology Stack

  -----------------------------------------------------------------------
  Technology                          Purpose
  ----------------------------------- -----------------------------------
  AWS, AWS CLI, STS                   Cloud services, CLI access,
                                      identity verification

  Python and Boto3                    Resource inventory and automation

  JSON and CSV                        Audit reports

  Docker                              Reproducible execution

  Terraform                           Infrastructure-as-code learning and
                                      validation

  Git and GitHub                      Version control and collaboration

  GitHub Actions                      Automated validation
  -----------------------------------------------------------------------

## Audit Status Semantics

  Result      Meaning
  ----------- ------------------------------------------------------
  `0 / OK`    Check succeeded and no matching resources were found
  `UNKNOWN`   The category could not be checked reliably
  `PARTIAL`   Some audit checks failed and others succeeded
  `FAILED`    All audit checks failed

The JSON report includes `resource_visibility`, which records visibility
status and a resource count when available. API error details are also
reported. Permission failures must not be treated as proof that no
resources exist.

## Repository Structure

``` text
aws-cloud-cost-optimization/
├── .github/workflows/terraform-ci.yml
├── docs/
├── iam/
├── kubernetes/
├── labs/
├── scripts/
│   ├── aws_cost_audit.py
│   └── check_secrets.py
├── terraform/
├── tests/
│   └── test_aws_cost_audit.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
├── progress.md
└── README.md
```

## Getting Started

### Prerequisites

Install Python 3.13 or a supported version, AWS CLI, Docker Desktop,
Terraform, and Git. Commands below use PowerShell on Windows.

### 1. Clone

``` powershell
git clone https://github.com/Satsaheb25/aws-cloud-cost-optimization.git
Set-Location aws-cloud-cost-optimization
```

### 2. Verify AWS identity

Authenticate with your configured AWS CLI method, then run:

``` powershell
aws sts get-caller-identity
```

Confirm the account and identity are the ones intended for the lab. Use
appropriately restricted IAM permissions and enable MFA.

### 3. Install Python dependencies

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the audit

``` powershell
python scripts/aws_cost_audit.py
```

Reports are written to `reports/aws_cost_audit.json` and
`reports/aws_cost_audit.csv`. The IAM identity needs read permissions
for the resource categories being inspected. Investigate permission
errors rather than treating them as empty results.

### 5. Run tests and secret checks

``` powershell
python -m py_compile scripts/aws_cost_audit.py tests/test_aws_cost_audit.py
python -m unittest discover -s tests -v
python scripts/check_secrets.py
```

### 6. Validate Terraform

``` powershell
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
```

These are configuration checks, not deployment commands.

### 7. Build Docker image

``` powershell
docker build -t aws-cost-audit:1.0 .
```

Supply credentials at runtime using the project's configured mount
approach. Never bake AWS access keys into an image.

## Cost and Security Safeguards

-   Use a non-root identity for routine work; enable MFA.
-   Configure billing budgets and cost alerts.
-   Check credits, Free Tier eligibility, and current service pricing
    before labs.
-   Use `ap-south-1` (Mumbai) for regional labs unless a lab specifies
    otherwise.
-   Prefer read-only audit operations.
-   Never commit access keys, session tokens, private keys, or sensitive
    reports.
-   Avoid public resources unless a reviewed lab specifically requires
    them.
-   Verify resources before cleanup; delete only resources confirmed
    safe to remove.
-   Avoid unnecessary always-on resources, NAT gateways, load balancers,
    and Kubernetes clusters.
-   Keep Terraform state, local backups, and generated reports out of
    source control.
-   Do not run `terraform apply` just to validate syntax.

AWS credits are not a substitute for monitoring actual account usage and
charges.

## Completed S3 Lab

The S3 lab covered bucket creation in `ap-south-1`, uploading and
verifying a test object, enabling versioning, inspecting object
versions, testing delete markers, removing the pre-versioning `null`
version, permanently deleting test versions, and deleting the bucket
after cleanup validation.

The test bucket was deleted after the lab. This demonstrated that
deleting an object in a versioned bucket does not necessarily delete its
stored versions.

## Historical Milestone: Phase 28

**Commit:** `367395a` --- `Improve audit resource visibility reporting`

Completed: - `UNKNOWN` status and `null` count for inaccessible resource
categories. - JSON `resource_visibility` metadata. - Console output
distinguishing unknown visibility from a successful zero count. -
Regression tests for successful, partial-failure, and total-failure
outcomes. - Updated `progress.md`.

Local validation passed: - Python compilation. - 10 unit tests. -
Secret-pattern scan across 48 tracked files. - Terraform formatting,
initialization with backend disabled, and validation. -
`git diff --check`.

These are local results; check the remote Actions page for the GitHub
Actions result.

## Interview Talking Points

**Why Boto3?** It enables repeatable inventory and reporting through AWS
service APIs.

**Why `UNKNOWN` instead of zero?** A failed API request does not prove
that a resource category is empty. Explicit visibility prevents
incomplete results from being presented as a successful audit.

**Why Docker?** It makes the runtime and dependencies more reproducible
across local and CI environments.

**Why GitHub Actions?** Automated checks can catch syntax errors,
regressions, secret-pattern matches, container build issues, and invalid
Terraform configuration.

**How does this help cost optimization?** Resource inventory helps
identify resources for review, but it does not replace billing analysis
or service-specific cost calculations.

## Future Enhancements

-   Integrate AWS Cost Explorer for actual spend and service-level
    trends.
-   Add cost recommendations with documented assumptions.
-   Produce historical audit comparisons and trend reports.
-   Expand resource-specific regression tests.
-   Improve CI summaries and artifact handling.
-   Add Terraform policy/security checks without provisioning resources.
-   Consider optional cleanup workflows with explicit approval, dry-run
    behavior, and safeguards.

## Links

-   **Repository:**
    https://github.com/Satsaheb25/aws-cloud-cost-optimization
-   **GitHub Actions:**
    https://github.com/Satsaheb25/aws-cloud-cost-optimization/actions
-   **Branch:** `master`
-   **Regional lab region:** `ap-south-1` (Mumbai, India)

------------------------------------------------------------------------

*This is an active hands-on learning project. Update feature and
validation claims as implementation evolves. No production-readiness or
guaranteed cost-savings claims are made.*


## Historical Milestone: Phase 32

**Status:** Local validation passed.

- Strengthened report-contract assertions against actual generated audit reports.
- Validated required JSON report fields, read-only mode, check totals, audit status, and error counts.
- Replaced a weak standalone arithmetic test with assertions on PASS, PARTIAL, and FAILED audit outcomes.
- Unit tests: 14 passed.
- Python compilation and `git diff --check`: passed.
- No AWS infrastructure was created, modified, or deleted.

See `progress.md` and `tests/test_aws_cost_audit.py` for the project record and implementation.

## Historical Milestone: Phase 33

**Status:** Completed; commit pushed and GitHub Actions passed.

- Added three direct classification unit tests.
- Tested zero-count behavior, all seven known cost-risk resource types, and the unknown-type fallback.
- Unit tests: 17 passed.
- Python compilation, secret scan, Terraform formatting, Terraform validation, and `git diff --check`: passed.
- No AWS infrastructure was created, modified, or deleted.

See `progress.md` and `tests/test_aws_cost_audit.py` for details.


## Latest Milestone: Phase 34 ? Classification Enrichment Tests

- Added three unit tests for `add_classification()`.
- Verified classification across multiple resources.
- Verified existing resource fields are preserved.
- Verified empty resource lists are handled safely.
- Validation: Python compilation, all 20 unit tests, and `git diff --check` passed.
- Safety: no AWS resources created, modified, or deleted.
- Status: Local validation passed; commit and CI verification pending.

### Phase 35 ? Report-Generation Test Coverage
- Added tests for JSON Unicode and nested-data round trips.
- Added CSV tests for nested details, non-string values, and missing optional fields.
- Full test suite: 23 tests passed.
- Scope: local unit tests only; no AWS resources changed.


## Latest Milestone: Phase 36 - Error-Handling Test Coverage

- Added a regression test for AWS session initialization failure.
- Verified exit code 1 and confirmed report writers and the EC2 audit are not called.
- Unit tests: 24 passed.
- `git diff --check`: passed; Git may display a Windows line-ending warning.
- No AWS infrastructure was created, modified, or deleted.
- Status: Local validation passed; commit and CI verification pending.

See `progress.md` and `tests/test_aws_cost_audit.py` for details.


## Project Closeout — Core Scope Complete

**Completed through:** Phase 36  
**Final feature commit:** `e023ab7`

### Delivered
- Read-only AWS cost-audit automation using Python and Boto3.
- Docker packaging for the audit tool.
- Terraform configuration formatting and validation.
- GitHub Actions CI/CD checks for Python, Docker, and Terraform.
- Unit tests covering classification, report generation, and session initialization failure.
- Secret-pattern scanning and project progress documentation.

### Scope and Safety
- No AWS infrastructure was provisioned as part of this closeout.
- Terraform validation does not mean infrastructure was deployed.
- EKS/Kubernetes deployment is not claimed as production-ready.
- Confirm the latest GitHub Actions run before claiming final remote CI success.

**Status:** Core learning-project scope complete; optional Phase 37 skipped.
