# AWS Cost Explorer & Cost Visibility

## Objective

Understand how AWS Cost Explorer provides account-level visibility into cloud spending and how service-level cost analysis supports cost optimization.

## Environment

- AWS Region: ap-south-1 (Mumbai)
- Project: AWS Cloud Cost Optimization
- Analysis period: 2026-09-01 to 2026-09-29
- Primary service analyzed: Amazon S3

## Cost Explorer Analysis

Cost Explorer was analyzed using AWS CLI with:

- Time range: 2026-09-01 to 2026-09-29
- Granularity: Monthly
- Metric: UnblendedCost
- Grouping: AWS Service

### Observed Cost

Current Cost Explorer result:

- Unblended Cost: -0.0000000002 USD
- Effective cost at normal reporting precision: approximately $0.00 USD
- Billing status: Estimated: true

The September billing period is still in progress, so the displayed amount is an estimate and may change as AWS processes additional usage and billing adjustments.

## S3 Cost Optimization Connection

The S3 labs demonstrated:

- Versioning can retain multiple object versions
- Lifecycle policies can automatically expire data
- Storage classes can reduce storage costs based on access patterns
- Unused resources should be cleaned up

Cost Explorer provides account-level visibility needed to validate these optimization practices.

## Key Learning

Cost optimization starts with cost visibility.

Cost Explorer can be used to:

- Identify AWS service costs
- Analyze spending over time
- Monitor current billing-period costs
- Investigate cost changes
- Support cost optimization decisions

A near-zero current cost also demonstrates the importance of avoiding unnecessary always-on infrastructure during learning labs.

## Interview Explanation

> "I use AWS Cost Explorer to analyze cloud spending by service and time period. I can use the Cost Explorer API through AWS CLI to retrieve cost data and correlate AWS usage with cost-optimization activities. In my lab, I monitored the current billing period and maintained a near-zero cost by using temporary resources and cleaning them up after testing."

## Result

AWS Cost Explorer API access was successfully verified and the current September billing-period cost was analyzed.

**Status: Completed**
