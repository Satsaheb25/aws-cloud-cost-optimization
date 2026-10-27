import csv
import json
import tempfile
import unittest
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

from scripts import aws_cost_audit
from botocore.exceptions import BotoCoreError, ClientError


class TestAuditReports(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.report_dir = Path(self.temp_dir.name) / "reports"
        self.json_report = self.report_dir / "audit.json"
        self.csv_report = self.report_dir / "audit.csv"

        self.patches = [
            patch.object(aws_cost_audit, "REPORT_DIR", self.report_dir),
            patch.object(aws_cost_audit, "JSON_REPORT", self.json_report),
            patch.object(aws_cost_audit, "CSV_REPORT", self.csv_report),
        ]

        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def test_json_report_is_written_and_readable(self):
        report = {
            "project": "AWS Cloud Cost Optimization",
            "region": "ap-south-1",
            "read_only": True,
            "resources": [],
            "errors": [],
        }

        aws_cost_audit.write_json_report(report)

        self.assertTrue(self.json_report.is_file())

        with self.json_report.open(encoding="utf-8") as file:
            actual = json.load(file)

        self.assertEqual(actual, report)

    def test_csv_report_contains_resource_fields(self):
        resources = [
            {
                "resource_type": "EC2 Instance",
                "resource_id": "i-test123",
                "state": "stopped",
                "risk": "Medium",
                "details": {"instance_type": "t3.small"},
            }
        ]

        aws_cost_audit.write_csv_report(resources)

        self.assertTrue(self.csv_report.is_file())

        with self.csv_report.open(
            newline="",
            encoding="utf-8",
        ) as file:
            rows = list(csv.DictReader(file))

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["resource_type"], "EC2 Instance")
        self.assertEqual(rows[0]["resource_id"], "i-test123")
        self.assertEqual(rows[0]["state"], "stopped")
        self.assertEqual(rows[0]["risk"], "Medium")
        self.assertIn("t3.small", rows[0]["details"])

    def test_csv_report_supports_empty_resource_list(self):
        aws_cost_audit.write_csv_report([])

        with self.csv_report.open(
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        self.assertEqual(rows, [])
        self.assertEqual(
            reader.fieldnames,
            [
                "resource_type",
                "resource_id",
                "state",
                "risk",
                "details",
            ],
        )


if __name__ == "__main__":
    unittest.main()

class TestSafeCall(unittest.TestCase):
    def test_successful_call_returns_result_without_error(self):
        result, error = aws_cost_audit.safe_call(
            "EC2 Instance",
            lambda: ["instance-1"],
        )

        self.assertEqual(result, ["instance-1"])
        self.assertIsNone(error)

    def test_client_error_returns_default_and_error_details(self):
        exception = ClientError(
            {
                "Error": {
                    "Code": "AccessDenied",
                    "Message": "Access denied",
                }
            },
            "DescribeInstances",
        )

        result, error = aws_cost_audit.safe_call(
            "EC2 Instance",
            lambda: (_ for _ in ()).throw(exception),
            default={"Reservations": []},
        )

        self.assertEqual(result, {"Reservations": []})
        self.assertIsNotNone(error)
        self.assertEqual(error["resource_type"], "EC2 Instance")
        self.assertIn("AccessDenied", error["error"])

    def test_botocore_error_returns_default_and_error_details(self):
        exception = BotoCoreError()

        result, error = aws_cost_audit.safe_call(
            "S3 Bucket",
            lambda: (_ for _ in ()).throw(exception),
            default={"Buckets": []},
        )

        self.assertEqual(result, {"Buckets": []})
        self.assertIsNotNone(error)
        self.assertEqual(error["resource_type"], "S3 Bucket")

    def test_unexpected_error_returns_default_and_error_details(self):
        result, error = aws_cost_audit.safe_call(
            "Load Balancer",
            lambda: 1 / 0,
            default={"LoadBalancers": []},
        )

        self.assertEqual(result, {"LoadBalancers": []})
        self.assertIsNotNone(error)
        self.assertEqual(error["resource_type"], "Load Balancer")
        self.assertIn("Unexpected error", error["error"])


class TestAuditStatus(unittest.TestCase):
    AUDIT_FUNCTIONS = (
        "audit_ec2",
        "audit_ebs",
        "audit_snapshots",
        "audit_elastic_ips",
        "audit_nat_gateways",
        "audit_load_balancers",
        "audit_s3",
    )

    def run_audit_with_outcomes(self, outcomes):
        with (
            patch.object(aws_cost_audit.boto3, "Session") as session_factory,
            patch.object(aws_cost_audit, "write_json_report") as json_writer,
            patch.object(aws_cost_audit, "write_csv_report"),
        ):
            session_factory.return_value.client.return_value = object()

            with ExitStack() as stack:
                for name, outcome in zip(self.AUDIT_FUNCTIONS, outcomes):
                    stack.enter_context(
                        patch.object(aws_cost_audit, name, return_value=outcome)
                    )

                exit_code = aws_cost_audit.main()

            report = json_writer.call_args.args[0]

        return exit_code, report

    def test_all_checks_succeed_returns_pass(self):
        outcomes = [([], None)] * 7

        exit_code, report = self.run_audit_with_outcomes(outcomes)

        self.assertEqual(exit_code, 0)
        self.assertEqual(report["audit_status"], "PASS")
        self.assertEqual(
            report["check_summary"],
            {
                "total_checks": 7,
                "successful_checks": 7,
                "failed_checks": 0,
            },
        )

        for result in report["summary"].values():
            self.assertEqual(result["count"], 0)
            self.assertEqual(result["risk"], "OK")

        for result in report["resource_visibility"].values():
            self.assertEqual(result["status"], "VISIBLE")
            self.assertEqual(result["resource_count"], 0)

    def test_some_checks_fail_returns_partial(self):
        error = {"resource_type": "EC2 Instance", "error": "AccessDenied"}
        outcomes = [([], error)] + [([], None)] * 6

        exit_code, report = self.run_audit_with_outcomes(outcomes)

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["audit_status"], "PARTIAL")
        self.assertEqual(report["check_summary"]["successful_checks"], 6)
        self.assertEqual(report["check_summary"]["failed_checks"], 1)
        self.assertEqual(len(report["errors"]), 1)

        self.assertIsNone(report["summary"]["EC2 Instance"]["count"])
        self.assertEqual(
            report["summary"]["EC2 Instance"]["risk"],
            "UNKNOWN",
        )
        self.assertEqual(
            report["resource_visibility"]["EC2 Instance"]["status"],
            "UNKNOWN",
        )
        self.assertEqual(
            report["resource_visibility"]["EBS Volume"]["status"],
            "VISIBLE",
        )

    def test_all_checks_fail_returns_failed(self):
        resource_types = [
            "EC2 Instance",
            "EBS Volume",
            "EBS Snapshot",
            "Elastic IP",
            "NAT Gateway",
            "Load Balancer",
            "S3 Bucket",
        ]

        outcomes = [
            ([], {"resource_type": name, "error": "AccessDenied"})
            for name in resource_types
        ]

        exit_code, report = self.run_audit_with_outcomes(outcomes)

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["audit_status"], "FAILED")
        self.assertEqual(report["check_summary"]["successful_checks"], 0)
        self.assertEqual(report["check_summary"]["failed_checks"], 7)

        for result in report["summary"].values():
            self.assertIsNone(result["count"])
            self.assertEqual(result["risk"], "UNKNOWN")

        for result in report["resource_visibility"].values():
            self.assertEqual(result["status"], "UNKNOWN")
            self.assertIsNone(result["resource_count"])
