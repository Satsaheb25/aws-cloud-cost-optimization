
import re
import subprocess
import sys


PATTERNS = {
    "AWS access key ID": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "AWS secret access key assignment": re.compile(
        r"(?i)\baws_secret_access_key\s*=\s*[\"']?[A-Za-z0-9/+=]{40}"
    ),
}


def main():
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
        text=True,
    )

    tracked_files = [
        path for path in result.stdout.split("\0") if path
    ]

    findings = []

    for filename in tracked_files:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
        except (OSError, UnicodeError):
            continue

        for description, pattern in PATTERNS.items():
            if pattern.search(content):
                findings.append((filename, description))

    if findings:
        print("Potential AWS credential pattern detected:")
        for filename, description in findings:
            print(f"- {filename}: {description}")
        print("Review the findings and remove any real credentials.")
        return 1

    print(
        f"Secret-pattern check passed "
        f"({len(tracked_files)} tracked files scanned)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())