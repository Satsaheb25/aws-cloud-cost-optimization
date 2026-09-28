# S3 Storage Class Cost Analysis

## Objective

Understand how S3 storage classes can be selected based on access frequency, retrieval requirements, resilience requirements, and retention.

## Lab Environment

- AWS Region: ap-south-1 (Mumbai)
- Bucket: sagar-aws-lifecycle-2026
- Prefix: lifecycle-test/
- Versioning: Enabled

## Practical Test

An S3 object was initially stored using the default S3 Standard storage class.

The current object was then copied using the STANDARD_IA storage class.

Verification with HeadObject confirmed:

- StorageClass: STANDARD_IA
- A new object VersionId was created
- The previous STANDARD version became noncurrent

## Storage Class Decision Matrix

| Storage Class | Suitable Access Pattern | Key Consideration |
|---|---|---|
| S3 Standard | Frequently accessed data | Higher storage cost but designed for frequent access |
| S3 Standard-IA | Infrequently accessed data | Lower storage cost with retrieval charges and minimum-duration considerations |
| S3 One Zone-IA | Infrequently accessed, reproducible data | Lower-cost single-AZ storage; not suitable when multi-AZ resilience is required |
| S3 Glacier Instant Retrieval | Rarely accessed archive data requiring rapid retrieval | Archive storage with retrieval charges |
| S3 Glacier Flexible Retrieval | Archive data accessed occasionally | Retrieval time and retrieval charges must be considered |
| S3 Glacier Deep Archive | Very rarely accessed long-term data | Designed for long-term archival with longer retrieval times |

## Cost Optimization Principles

Storage class selection should consider:

- Access frequency
- Data retrieval requirements
- Data retention period
- Availability and resilience requirements
- Storage cost
- Retrieval charges
- Request charges
- Minimum storage duration requirements

## Versioning Consideration

Because S3 Versioning was enabled, changing the storage class of the current object created a new object version.

The previous version remained stored independently using S3 Standard.

This demonstrates why storage-class optimization and lifecycle policies should be considered together.

## Interview Explanation

I tested S3 storage-class optimization by moving an object from S3 Standard to Standard-IA using CopyObject and verified the resulting storage class with HeadObject. Because versioning was enabled, the operation created a new version while the previous version remained independently stored. I then evaluated storage classes based on access patterns, retrieval requirements, resilience, and retention.

## Result

S3 Storage Class Cost Analysis completed successfully.
