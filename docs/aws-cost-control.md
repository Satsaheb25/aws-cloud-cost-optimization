# AWS Cost Control

## Purpose

This document records practical AWS cost-control concepts demonstrated through hands-on labs.

## S3 Cost-Control Considerations

Amazon S3 costs can accumulate from:

- Stored objects
- Older object versions
- Data retrieval
- Data transfer
- API requests
- Incomplete multipart uploads
- Long-term retained data

A resource that is no longer visible through the normal object listing may still consume storage when Versioning is enabled.

## S3 Versioning and Cost

S3 Versioning provides protection against accidental overwrites and deletions, but it can increase storage consumption because previous versions remain stored.

Example:

Object Version 1
  -> Object Version 2
  -> Object Version 3
  -> Delete Marker

A Delete Marker does not automatically remove previous object versions.

Therefore, version lifecycle management is important in cost-sensitive environments.

## Recommended Controls

### 1. Lifecycle Policies

Use S3 Lifecycle rules to manage older object versions.

Typical actions can include:

- Transition objects to lower-cost storage classes
- Expire old object versions
- Remove expired Delete Markers
- Abort incomplete multipart uploads

### 2. Storage-Class Optimization

Select storage classes according to access patterns.

Examples include:

- S3 Standard
- S3 Intelligent-Tiering
- S3 Standard-IA
- S3 One Zone-IA
- S3 Glacier storage classes

The appropriate choice depends on access frequency, retrieval requirements, availability requirements, and retention period.

### 3. Regular Resource Cleanup

Temporary development resources should be removed after testing when they are no longer required.

During the S3 lab:

- Test object was created
- Multiple versions were created
- Delete Marker was created
- Versions were individually removed
- Bucket was emptied
- Bucket was deleted

This demonstrates a basic resource-cleanup workflow.

## CLI Verification

``powershell
aws s3 ls
``

``powershell
aws s3 ls s3://<bucket-name>/
``

``powershell
aws s3api list-object-versions ` 
  --bucket <bucket-name> ` 
  --prefix <object-key>
``

``powershell
aws s3api head-bucket ` 
  --bucket <bucket-name>
``

## Important Operational Principle

Before deleting a versioned S3 bucket, verify:

1. Current objects
2. Object versions
3. Delete Markers
4. Incomplete multipart uploads
5. Lifecycle policies
6. Data-retention requirements

For production systems, cleanup should follow organizational retention and recovery requirements.

## Future Cost-Optimization Labs

- [ ] S3 Lifecycle Policies
- [ ] S3 Storage Classes
- [ ] S3 Cost Analysis
- [ ] AWS Cost Explorer
- [ ] AWS Budgets
- [ ] EC2 right-sizing
- [ ] EBS volume cleanup
- [ ] EBS snapshot management
- [ ] Unused Elastic IP analysis
- [ ] CloudWatch cost monitoring
- [ ] Python/Boto3 automation
- [ ] Terraform resource management
- [ ] Automated cleanup scripts
