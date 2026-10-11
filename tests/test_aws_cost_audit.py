import csv
import json
import tempfile
import unittest
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
