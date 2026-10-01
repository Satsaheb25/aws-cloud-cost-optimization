# Kubernetes Deployment Lab

## Objective

Deploy the Dockerized AWS Cost Audit application to a local Kubernetes cluster using Docker Desktop Kubernetes.

## Environment

- Kubernetes: Docker Desktop
- Kubernetes version: v1.36.1
- Cluster mode: Kind
- Namespace: `aws-cost-optimization`
- AWS Region: `ap-south-1`
- Container image: `host.docker.internal:5000/aws-cost-audit:ci`

## Architecture

Docker Image
? Local Registry
? Docker Desktop Kubernetes
? Kubernetes Deployment
? AWS Cost Audit Pod
? Python/Boto3 Audit

## Implementation

### Namespace

Created namespace:

`aws-cost-optimization`

### Deployment

Created Kubernetes Deployment:

`aws-cost-audit`

Replica configuration:

`1`

The container receives the AWS region through:

`AWS_DEFAULT_REGION=ap-south-1`

## Local Registry

Docker Desktop Kubernetes runs with its own containerd image store.

The application image was therefore pushed to a local registry:

`host.docker.internal:5000/aws-cost-audit:ci`

The image was successfully pulled into the Kubernetes container runtime using `crictl`.

## Validation

Deployment status:

- Deployment created successfully
- Pod successfully started
- Kubernetes rollout completed successfully

The audit application generated its normal console output.

## AWS Authentication

The Kubernetes Pod does not automatically inherit the AWS CLI login session from the Windows host.

The application therefore reported:

`Unable to locate credentials`

for the AWS API calls.

No AWS credentials were placed in the Kubernetes manifest.

Secure workload identity/authentication will be addressed in a later phase.

## Safety

This local Kubernetes lab did not create, modify, or delete AWS resources.

No AWS access keys or secrets are stored in Kubernetes YAML.

## Interview Perspective

I containerized a Python/Boto3 AWS cost-audit application and deployed it to a local Kubernetes cluster using a Kubernetes Deployment. Because Docker Desktop Kubernetes uses a separate containerd image store, I used a local container registry and verified the image through the Kubernetes container runtime.

The workload is batch-oriented and terminates after the audit completes. A later improvement will convert the Deployment into a Kubernetes Job, which is a more appropriate Kubernetes workload type for a one-time audit.

## Commands Used

```powershell
kubectl get nodes
kubectl get namespaces
kubectl apply -f .\kubernetes\namespace.yaml
kubectl apply -f .\kubernetes\deployment.yaml
kubectl get pods -n aws-cost-optimization
kubectl rollout status deployment/aws-cost-audit -n aws-cost-optimization
kubectl logs deployment/aws-cost-audit -n aws-cost-optimization
@
@
