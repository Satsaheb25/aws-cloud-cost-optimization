# Phase 12 - EBS Cost Optimization

## Objective

Audit Amazon EBS resources for unnecessary storage costs and understand EBS cost optimization techniques without creating unnecessary billable resources.

## Environment

- AWS Region: ap-south-1 (Mumbai)
- Project: AWS Cloud Cost Optimization & DevOps Automation Platform
- Audit method: AWS CLI
- Approach: Read-only audit

## EBS Volume Audit

Command:

    aws ec2 describe-volumes --region ap-south-1 --query "Volumes[].{ID:VolumeId,SizeGiB:Size,Type:VolumeType,State:State,AZ:AvailabilityZone,AttachedTo:Attachments[0].InstanceId}" --output table --no-cli-pager

### Result

No EBS volumes were returned.

This means the AWS environment currently has:

- No attached EBS volumes
- No unattached EBS volumes
- No provisioned EBS storage requiring cleanup

## EBS Snapshot Audit

Command:

    aws ec2 describe-snapshots --region ap-south-1 --owner-ids self --query "Snapshots[].{ID:SnapshotId,SizeGiB:VolumeSize,State:State,StartTime:StartTime,VolumeId:VolumeId}" --output table --no-cli-pager

### Result

No EBS snapshots owned by the account were returned.

## Cost Optimization Concepts

### 1. Identify Unattached Volumes

An EBS volume can continue generating storage charges even when it is not attached to an EC2 instance.

Regular audits should identify volumes in the available state.

### 2. Right-Size EBS Storage

Provision only the storage capacity required by the workload.

Oversized volumes increase unnecessary storage costs.

### 3. Select the Appropriate Volume Type

EBS volume type should match application requirements.

Consider:

- General-purpose SSD requirements
- Provisioned IOPS requirements
- Throughput requirements
- Capacity requirements
- Latency requirements
- Workload characteristics

### 4. Consider gp3

For suitable general-purpose workloads, gp3 can provide configurable performance independently from storage capacity.

Migration decisions should consider workload requirements and current AWS pricing.

### 5. Manage Snapshots

Snapshots should be reviewed periodically.

Old or unnecessary snapshots can accumulate storage costs.

Retention policies should be based on:

- Recovery requirements
- Compliance requirements
- Backup strategy
- Business retention period

### 6. Avoid Unnecessary Lab Resources

For this learning project, an EBS volume was not created merely to demonstrate deletion.

The existing environment already provided sufficient evidence for a read-only cost audit.

## Cost Safety

No EBS resources were created during this phase.

Therefore, the Phase 12 audit did not introduce additional EBS storage resources requiring cleanup.

## Interview Explanation

I performed an EBS cost optimization audit using AWS CLI. I checked provisioned EBS volumes and account-owned snapshots. The environment contained no EBS volumes or snapshots, so I did not create temporary resources just for the demonstration.

I documented the main EBS optimization controls including identifying unattached volumes, right-sizing storage, selecting appropriate volume types, evaluating gp3, and managing snapshot retention.

## Result

Phase 12 read-only EBS audit completed successfully.

- EBS volumes: 0
- Unattached EBS volumes: 0
- EBS snapshots: 0
- Additional AWS resources created: 0
- Cleanup required: None

## Status

**Completed - Read-only EBS cost optimization audit**
