 # Python / Boto3 AWS Cost Audit Automation

## Phase 14 — Python / Boto3 Automation


## Objective

Automate AWS resource cost-risk auditing using Python and Boto3. The automation replaces repetitive manual AWS CLI audits with a reusable, read-only Python script.


## Environment

- OS: Windows 11
- Python: 3.13.7
- Boto3: 1.43.104
- Botocore: 1.43.104
- AWS CRT: 0.36.0
- AWS CLI: 2.36.44
- AWS Region: ap-south-1 (Mumbai, India)


## Automation Script

scripts/aws_cost_audit.py`r

The script performs read-only inventory checks for EC2, EBS volumes, EBS snapshots, Elastic IPs, NAT gateways, load balancers, and S3 buckets.


## Read-Only Safety

The automation does not create, modify, stop, or delete AWS resources. It uses read-only inventory APIs.


## Cost-Risk Classification

- **OK** — no resources of that type were found.
- **POTENTIAL COST** — resources exist that can generate ongoing or usage-based AWS charges and should be reviewed.
- **REVIEW** — additional evaluation is required.

POTENTIAL COST does not mean a resource is unnecessary. Business need and utilization must be evaluated separately.


## Reports

The script generates 
eports/aws_cost_audit.json and 
eports/aws_cost_audit.csv. Generated reports are excluded from Git.


## Validation

Syntax validation: python -m py_compile .\scripts\aws_cost_audit.py`r

Audit execution: python .\scripts\aws_cost_audit.py`r


## Successful Result

EC2 Instance: 0
EBS Volume: 0
EBS Snapshot: 0
Elastic IP: 0
NAT Gateway: 0
Load Balancer: 0
S3 Bucket: 0

API errors: 0.

The audit completed successfully and no AWS resources were created, modified, or deleted.


## Relationship to Previous Phases

Phase 14 builds on the S3, Cost Explorer, Budgets, EC2, EBS, and Elastic IP/network cost-optimization audits completed in previous phases.

The major improvement is repeatability: multiple manual AWS CLI audits are now represented by a reusable Python/Boto3 automation.


## Productionization

Future extensions can include AWS Lambda, EventBridge scheduling, S3 report storage, SNS notifications, CloudWatch monitoring, tagging compliance, cost anomaly detection, GitHub Actions, and Terraform-managed deployment.


## Interview Perspective

I built a Python and Boto3 based AWS cost-audit automation tool. It performs read-only inventory checks across EC2, EBS, snapshots, Elastic IPs, NAT gateways, load balancers, and S3. The automation classifies resources based on potential cost exposure and generates JSON and CSV reports.

A key design principle is that POTENTIAL COST identifies possible charge exposure; it does not automatically identify a resource as wasteful.


## Result

**Status: Completed — Python/Boto3 AWS Cost Audit Automation**

