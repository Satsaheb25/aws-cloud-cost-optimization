# Project Progress

## Overall Status

**Project:** AWS Cloud Cost Optimization
**Status:** Active
**Current Lab:** Amazon S3 Versioning & Cleanup
**Region:** ap-south-1
**Date:** 2026-09-26

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

- [ ] S3 Lifecycle Policies
- [ ] S3 Storage-Class Optimization
- [ ] S3 Cost Analysis
- [ ] AWS Cost Explorer exercises
- [ ] AWS Budgets
- [ ] EC2 cost optimization
- [ ] EBS volume cleanup
- [ ] EBS snapshot cleanup
- [ ] Unused Elastic IP analysis
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
