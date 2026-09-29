import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError


REGION = "ap-south-1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "reports"

JSON_REPORT = REPORT_DIR / "aws_cost_audit.json"
CSV_REPORT = REPORT_DIR / "aws_cost_audit.csv"


def utc_timestamp():
    return datetime.now(timezone.utc).isoformat()


def classify(resource_type, count):
    """
    Cost-risk classification.

    OK:
        No resources of this type were found.

    REVIEW:
        Resources exist and should be reviewed for necessity/configuration.

    POTENTIAL COST:
        Resource type can create ongoing or usage-based AWS charges.
    """
    if count == 0:
        return "OK"

    potential_cost_resources = {
        "EC2 Instance",
        "EBS Volume",
        "EBS Snapshot",
        "Elastic IP",
        "NAT Gateway",
        "Load Balancer",
        "S3 Bucket",
    }

    if resource_type in potential_cost_resources:
        return "POTENTIAL COST"

    return "REVIEW"


def safe_call(resource_type, function, default=None):
    """Execute a read-only AWS API call with error handling."""
    try:
        return function(), None

    except (ClientError, BotoCoreError) as exc:
        return default, {
            "resource_type": resource_type,
            "error": str(exc),
        }

    except Exception as exc:
        return default, {
            "resource_type": resource_type,
            "error": f"Unexpected error: {exc}",
        }


def audit_ec2(ec2):
    response, error = safe_call(
        "EC2 Instance",
        lambda: ec2.describe_instances(),
        {"Reservations": []},
    )

    resources = []

    for reservation in response["Reservations"]:
        for instance in reservation.get("Instances", []):
            resources.append(
                {
                    "resource_type": "EC2 Instance",
                    "resource_id": instance.get("InstanceId"),
                    "state": instance.get("State", {}).get("Name"),
                    "details": {
                        "instance_type": instance.get("InstanceType"),
                        "availability_zone": instance.get("Placement", {}).get(
                            "AvailabilityZone"
                        ),
                        "private_ip": instance.get("PrivateIpAddress"),
                        "public_ip": instance.get("PublicIpAddress"),
                    },
                }
            )

    return resources, error


def audit_ebs(ec2):
    response, error = safe_call(
        "EBS Volume",
        lambda: ec2.describe_volumes(),
        {"Volumes": []},
    )

    resources = []

    for volume in response["Volumes"]:
        attached_to = None

        if volume.get("Attachments"):
            attached_to = volume["Attachments"][0].get("InstanceId")

        resources.append(
            {
                "resource_type": "EBS Volume",
                "resource_id": volume.get("VolumeId"),
                "state": volume.get("State"),
                "details": {
                    "size_gib": volume.get("Size"),
                    "volume_type": volume.get("VolumeType"),
                    "availability_zone": volume.get("AvailabilityZone"),
                    "attached_to": attached_to,
                },
            }
        )

    return resources, error


def audit_snapshots(ec2):
    response, error = safe_call(
        "EBS Snapshot",
        lambda: ec2.describe_snapshots(OwnerIds=["self"]),
        {"Snapshots": []},
    )

    resources = []

    for snapshot in response["Snapshots"]:
        resources.append(
            {
                "resource_type": "EBS Snapshot",
                "resource_id": snapshot.get("SnapshotId"),
                "state": snapshot.get("State"),
                "details": {
                    "size_gib": snapshot.get("VolumeSize"),
                    "start_time": str(snapshot.get("StartTime")),
                    "volume_id": snapshot.get("VolumeId"),
                },
            }
        )

    return resources, error


def audit_elastic_ips(ec2):
    response, error = safe_call(
        "Elastic IP",
        lambda: ec2.describe_addresses(),
        {"Addresses": []},
    )

    resources = []

    for address in response["Addresses"]:
        resources.append(
            {
                "resource_type": "Elastic IP",
                "resource_id": address.get("AllocationId"),
                "state": "associated"
                if address.get("AssociationId")
                else "unassociated",
                "details": {
                    "public_ip": address.get("PublicIp"),
                    "association_id": address.get("AssociationId"),
                    "instance_id": address.get("InstanceId"),
                    "network_interface_id": address.get(
                        "NetworkInterfaceId"
                    ),
                },
            }
        )

    return resources, error


def audit_nat_gateways(ec2):
    response, error = safe_call(
        "NAT Gateway",
        lambda: ec2.describe_nat_gateways(),
        {"NatGateways": []},
    )

    resources = []

    for gateway in response["NatGateways"]:
        public_ips = []

        for address in gateway.get("NatGatewayAddresses", []):
            public_ip = address.get("PublicIp")

            if public_ip:
                public_ips.append(public_ip)

        resources.append(
            {
                "resource_type": "NAT Gateway",
                "resource_id": gateway.get("NatGatewayId"),
                "state": gateway.get("State"),
                "details": {
                    "subnet_id": gateway.get("SubnetId"),
                    "vpc_id": gateway.get("VpcId"),
                    "public_ips": public_ips,
                },
            }
        )

    return resources, error


def audit_load_balancers(elbv2):
    response, error = safe_call(
        "Load Balancer",
        lambda: elbv2.describe_load_balancers(),
        {"LoadBalancers": []},
    )

    resources = []

    for load_balancer in response["LoadBalancers"]:
        resources.append(
            {
                "resource_type": "Load Balancer",
                "resource_id": load_balancer.get("LoadBalancerArn"),
                "state": load_balancer.get("State", {}).get("Code"),
                "details": {
                    "name": load_balancer.get("LoadBalancerName"),
                    "type": load_balancer.get("Type"),
                    "vpc_id": load_balancer.get("VpcId"),
                    "dns_name": load_balancer.get("DNSName"),
                },
            }
        )

    return resources, error


def audit_s3(s3):
    response, error = safe_call(
        "S3 Bucket",
        lambda: s3.list_buckets(),
        {"Buckets": []},
    )

    resources = []

    for bucket in response["Buckets"]:
        resources.append(
            {
                "resource_type": "S3 Bucket",
                "resource_id": bucket.get("Name"),
                "state": "active",
                "details": {
                    "creation_date": str(bucket.get("CreationDate")),
                },
            }
        )

    return resources, error


def add_classification(resources):
    for resource in resources:
        resource["risk"] = classify(
            resource["resource_type"],
            1,
        )


def write_json_report(report):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    with JSON_REPORT.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)


def write_csv_report(resources):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "resource_type",
        "resource_id",
        "state",
        "risk",
        "details",
    ]

    with CSV_REPORT.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for resource in resources:
            writer.writerow(
                {
                    "resource_type": resource.get("resource_type"),
                    "resource_id": resource.get("resource_id"),
                    "state": resource.get("state"),
                    "risk": resource.get("risk"),
                    "details": json.dumps(
                        resource.get("details", {}),
                        default=str,
                    ),
                }
            )


def main():
    print("=" * 70)
    print("AWS COST OPTIMIZATION - PYTHON/BOTO3 AUDIT")
    print("=" * 70)
    print(f"Region: {REGION}")
    print(f"Audit time: {utc_timestamp()}")
    print()

    try:
        session = boto3.Session(region_name=REGION)

        ec2 = session.client("ec2")
        elbv2 = session.client("elbv2")
        s3 = session.client("s3")

    except Exception as exc:
        print(f"ERROR: Unable to initialize AWS session: {exc}")
        return 1

    audit_functions = [
        ("EC2", lambda: audit_ec2(ec2)),
        ("EBS", lambda: audit_ebs(ec2)),
        ("Snapshots", lambda: audit_snapshots(ec2)),
        ("Elastic IPs", lambda: audit_elastic_ips(ec2)),
        ("NAT Gateways", lambda: audit_nat_gateways(ec2)),
        ("Load Balancers", lambda: audit_load_balancers(elbv2)),
        ("S3", lambda: audit_s3(s3)),
    ]

    all_resources = []
    errors = []

    for name, audit_function in audit_functions:
        try:
            resources, error = audit_function()

            if resources:
                add_classification(resources)
                all_resources.extend(resources)

            if error:
                errors.append(error)

        except Exception as exc:
            errors.append(
                {
                    "resource_type": name,
                    "error": str(exc),
                }
            )

    resource_types = [
        "EC2 Instance",
        "EBS Volume",
        "EBS Snapshot",
        "Elastic IP",
        "NAT Gateway",
        "Load Balancer",
        "S3 Bucket",
    ]

    counts = {}

    for resource_type in resource_types:
        count = sum(
            1
            for resource in all_resources
            if resource["resource_type"] == resource_type
        )

        counts[resource_type] = {
            "count": count,
            "risk": classify(resource_type, count),
        }

    report = {
        "project": "AWS Cloud Cost Optimization & DevOps Automation Platform",
        "region": REGION,
        "audit_timestamp_utc": utc_timestamp(),
        "read_only": True,
        "summary": counts,
        "resources": all_resources,
        "errors": errors,
    }

    write_json_report(report)
    write_csv_report(all_resources)

    print("RESOURCE SUMMARY")
    print("-" * 70)

    for resource_type, result in counts.items():
        print(
            f"{resource_type:<18} "
            f"{result['count']:<5} "
            f"{result['risk']}"
        )

    print()
    print("REPORTS")
    print("-" * 70)
    print(f"JSON: {JSON_REPORT}")
    print(f"CSV : {CSV_REPORT}")

    print()
    print(f"API errors: {len(errors)}")

    if errors:
        print()
        print("ERROR DETAILS")

        for error in errors:
            print(f"- {error['resource_type']}: {error['error']}")

    print()
    print("Audit completed.")
    print("No AWS resources were created, modified, or deleted.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
