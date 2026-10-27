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

    def test_json_report_contract_has_required_fields(self):
        report = {
            "project": "AWS Cloud Cost Optimization",
            "region": "ap-south-1",
            "audit_timestamp_utc": "2026-10-27T12:00:00+00:00",
            "read_only": True,
            "audit_status": "PASS",
            "check_summary": {
                "total_checks": 7,
                "successful_checks": 7,
                "failed_checks": 0,
            },
            "summary": {},
            "resource_visibility": {},
            "resources": [],
            "errors": [],
        }

        aws_cost_audit.write_json_report(report)

        with self.json_report.open(encoding="utf-8") as file:
            actual = json.load(file)

        required_fields = {
            "project",
            "region",
            "audit_timestamp_utc",
            "read_only",
            "audit_status",
            "check_summary",
            "summary",
            "resource_visibility",
            "resources",
            "errors",
        }

        self.assertTrue(required_fields.issubset(actual.keys()))
        self.assertIs(actual["read_only"], True)
        self.assertIn(
            actual["audit_status"],
            {"PASS", "PARTIAL", "FAILED"},
        )
        self.assertEqual(actual["region"], "ap-south-1")
        self.assertEqual(actual["check_summary"]["total_checks"], 7)

    def test_csv_headers_match_report_contract(self):
        aws_cost_audit.write_csv_report([])

        with self.csv_report.open(
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)
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
            default=[],
        )

        self.assertEqual(result, [])
        self.assertEqual(error["resource_type"], "EC2 Instance")
        self.assertIn("AccessDenied", error["error"])

    def test_botocore_error_returns_default_and_error_details(self):
        exception = BotoCoreError()

        result, error = aws_cost_audit.safe_call(
            "EBS Volume",
            lambda: (_ for _ in ()).throw(exception),
            default=[],
        )

        self.assertEqual(result, [])
        self.assertEqual(error["resource_type"], "EBS Volume")

    def test_unexpected_error_returns_default_and_error_details(self):
        result, error = aws_cost_audit.safe_call(
            "Load Balancer",
            lambda: (_ for _ in ()).throw(RuntimeError("simulated failure")),
            default=[],
        )

        self.assertEqual(result, [])
        self.assertIn("simulated failure", error["error"])


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
                    if isinstance(outcome, Exception):
                        stack.enter_context(
                            patch.object(
                                aws_cost_audit,
                                name,
                                side_effect=outcome,
                            )
                        )
                    else:
                        stack.enter_context(
                            patch.object(
                                aws_cost_audit,
                                name,
                                return_value=outcome,
                            )
                        )

                exit_code = aws_cost_audit.main()

            report = json_writer.call_args.args[0]

        return exit_code, report

    def assert_report_contract(self, report):
        required_fields = {
            "project",
            "region",
            "audit_timestamp_utc",
            "read_only",
            "audit_status",
            "check_summary",
            "summary",
            "resource_visibility",
            "resources",
            "errors",
        }
        self.assertTrue(required_fields.issubset(report.keys()))
        self.assertIs(report["read_only"], True)

        checks = report["check_summary"]
        self.assertEqual(
            checks["total_checks"],
            checks["successful_checks"] + checks["failed_checks"],
        )
        self.assertEqual(checks["total_checks"], 7)
        self.assertIn(report["audit_status"], {"PASS", "PARTIAL", "FAILED"})
        self.assertEqual(len(report["errors"]), checks["failed_checks"])

    def test_all_checks_succeed_returns_pass(self):
        outcomes = [([], None)] * 7

        exit_code, report = self.run_audit_with_outcomes(outcomes)

        self.assert_report_contract(report)
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

        self.assert_report_contract(report)
        self.assertEqual(exit_code, 1)
        self.assertEqual(report["audit_status"], "PARTIAL")
        self.assertEqual(report["check_summary"]["successful_checks"], 6)
        self.assertEqual(report["check_summary"]["failed_checks"], 1)
        self.assertEqual(len(report["errors"]), 1)

        self.assertIsNone(report["summary"]["EC2 Instance"]["count"])
        self.assertEqual(report["summary"]["EC2 Instance"]["risk"], "UNKNOWN")
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

        self.assert_report_contract(report)
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


class TestAuditFailureRegression(unittest.TestCase):
    AUDIT_FUNCTIONS = (
        "audit_ec2",
        "audit_ebs",
        "audit_snapshots",
        "audit_elastic_ips",
        "audit_nat_gateways",
        "audit_load_balancers",
        "audit_s3",
    )

    def run_audit(self, outcomes):
        with (
            patch.object(aws_cost_audit.boto3, "Session") as session_factory,
            patch.object(aws_cost_audit, "write_json_report") as json_writer,
            patch.object(aws_cost_audit, "write_csv_report") as csv_writer,
            ExitStack() as stack,
        ):
            session_factory.return_value.client.return_value = object()

            for name, outcome in outcomes.items():
                if isinstance(outcome, Exception):
                    stack.enter_context(
                        patch.object(
                            aws_cost_audit,
                            name,
                            side_effect=outcome,
                        )
                    )
                else:
                    stack.enter_context(
                        patch.object(
                            aws_cost_audit,
                            name,
                            return_value=outcome,
                        )
                    )

            exit_code = aws_cost_audit.main()

        return (
            exit_code,
            json_writer.call_args.args[0],
            csv_writer.call_args.args[0],
        )

    def test_partial_failure_keeps_csv_resources_and_json_visibility_consistent(self):
        ec2_error = {
            "resource_type": "EC2 Instance",
            "error": "AccessDenied",
        }

        exit_code, report, csv_resources = self.run_audit(
            {
                "audit_ec2": ([], ec2_error),
                "audit_ebs": (
                    [
                        {
                            "resource_type": "EBS Volume",
                            "resource_id": "vol-test123",
                            "state": "available",
                            "risk": "POTENTIAL COST",
                            "details": {},
                        }
                    ],
                    None,
                ),
            }
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["audit_status"], "PARTIAL")
        self.assertIsNone(report["summary"]["EC2 Instance"]["count"])
        self.assertEqual(
            report["resource_visibility"]["EC2 Instance"]["status"],
            "UNKNOWN",
        )
        self.assertEqual(report["summary"]["EBS Volume"]["count"], 1)
        self.assertEqual(
            [item["resource_id"] for item in csv_resources],
            ["vol-test123"],
        )

    def test_unexpected_audit_exception_marks_resource_unknown(self):
        exit_code, report, csv_resources = self.run_audit(
            {
                "audit_ec2": RuntimeError("simulated audit failure"),
                "audit_ebs": ([], None),
                "audit_snapshots": ([], None),
                "audit_elastic_ips": ([], None),
                "audit_nat_gateways": ([], None),
                "audit_load_balancers": ([], None),
                "audit_s3": ([], None),
            }
        )

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["audit_status"], "PARTIAL")
        self.assertEqual(report["check_summary"]["successful_checks"], 6)
        self.assertEqual(report["check_summary"]["failed_checks"], 1)
        self.assertEqual(report["check_summary"]["total_checks"], 7)
        self.assertIsNone(report["summary"]["EC2 Instance"]["count"])
        self.assertEqual(
            report["resource_visibility"]["EC2 Instance"]["status"],
            "UNKNOWN",
        )
        self.assertTrue(report["errors"])

if __name__ == "__main__":
    unittest.main()


class TestClassification(unittest.TestCase):
    def test_zero_count_is_ok_for_known_and_unknown_types(self):
        resource_types = [
            "EC2 Instance",
            "EBS Volume",
            "EBS Snapshot",
            "Elastic IP",
            "NAT Gateway",
            "Load Balancer",
            "S3 Bucket",
            "Unlisted Resource",
        ]

        for resource_type in resource_types:
            with self.subTest(resource_type=resource_type):
                self.assertEqual(
                    aws_cost_audit.classify(resource_type, 0),
                    "OK",
                )

    def test_positive_count_for_cost_resources_is_potential_cost(self):
        resource_types = [
            "EC2 Instance",
            "EBS Volume",
            "EBS Snapshot",
            "Elastic IP",
            "NAT Gateway",
            "Load Balancer",
            "S3 Bucket",
        ]

        for resource_type in resource_types:
            with self.subTest(resource_type=resource_type):
                self.assertEqual(
                    aws_cost_audit.classify(resource_type, 1),
                    "POTENTIAL COST",
                )

    def test_positive_count_for_unlisted_type_requires_review(self):
        self.assertEqual(
            aws_cost_audit.classify("Unlisted Resource", 1),
            "REVIEW",
        )


    def test_add_classification_handles_multiple_resources(self):
        resources = [
            {"resource_type": "EC2 Instance", "resource_id": "i-test123",
             "region": "ap-south-1"},
            {"resource_type": "Unlisted Resource", "resource_id": "custom-test",
             "region": "ap-south-1"},
        ]
        aws_cost_audit.add_classification(resources)
        self.assertEqual(resources[0]["risk"], "POTENTIAL COST")
        self.assertEqual(resources[1]["risk"], "REVIEW")

    def test_add_classification_preserves_existing_fields(self):
        resource = {
            "resource_type": "S3 Bucket",
            "resource_id": "test-bucket",
            "region": "ap-south-1",
        }
        aws_cost_audit.add_classification([resource])
        self.assertEqual(resource["resource_id"], "test-bucket")
        self.assertEqual(resource["region"], "ap-south-1")
        self.assertEqual(resource["resource_type"], "S3 Bucket")
        self.assertEqual(resource["risk"], "POTENTIAL COST")

    def test_add_classification_handles_empty_list(self):
        resources = []
        result = aws_cost_audit.add_classification(resources)
        self.assertIsNone(result)
        self.assertEqual(resources, [])
