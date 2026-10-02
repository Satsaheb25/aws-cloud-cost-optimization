# Kubernetes Job — AWS Cost Audit

## Objective

Convert the AWS Cost Audit workload from a Kubernetes Deployment to a Kubernetes Job because the audit is a one-time batch task.

The application performs an AWS resource audit and exits after completing the report. A Deployment is intended for long-running workloads, so the completed container was repeatedly restarted.

---

## Problem Identified

The original Deployment entered:

`CrashLoopBackOff`

### Root Cause

The workload type was incorrect.

A Deployment is designed for long-running applications such as:

- Web applications
- APIs
- Microservices

A Kubernetes Job is designed for:

- Batch processing
- One-time tasks
- Reports
- Data processing
- Administrative tasks

---

## Solution

Created:

`kubernetes/job.yaml`

The Job configuration uses:

- API version: `batch/v1`
- Job name: `aws-cost-audit`
- Namespace: `aws-cost-optimization`
- Completions: `1`
- Backoff limit: `2`
- Restart policy: `Never`
- AWS region: `ap-south-1`

### Job Configuration

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: aws-cost-audit
  namespace: aws-cost-optimization
spec:
  backoffLimit: 2
  template:
    metadata:
      labels:
        app: aws-cost-audit
    spec:
      restartPolicy: Never
      containers:
        - name: aws-cost-audit
          image: host.docker.internal:5000/aws-cost-audit:ci
          imagePullPolicy: IfNotPresent
          env:
            - name: AWS_DEFAULT_REGION
              value: ap-south-1
```

---

## Phase Status

**Phase 17.1 — Kubernetes Job: COMPLETED**

Completed:

- Deployment troubleshooting
- CrashLoopBackOff investigation
- Kubernetes Job creation
- Job validation
- Job execution
- Job log analysis
- Job lifecycle verification
- AWS authentication issue identification
- Security decision against static credentials
- Cost-safety verification
- Documentation

---

## Next Phase

**AWS Workload Identity / Amazon EKS**

The objective is to allow a Kubernetes workload to securely call AWS APIs without storing long-lived AWS access keys in Kubernetes.

Because EKS can incur AWS charges, resources will be created only for the required lab duration and cleaned up afterward.
