#!/usr/bin/env python3
"""
run_extract_test.py

Simple test harness that runs `extract_attachments_from_eml.py` on `sample.eml`
and verifies the attachment was saved with the expected contents.
"""

import os
import shutil
import subprocess
import sys
import tempfile


def main():
    repo_root = os.path.dirname(__file__)
    sample = os.path.join(repo_root, "sample.eml")
    extractor = os.path.join(repo_root, "extract_attachments_from_eml.py")
    if not os.path.exists(sample):
        print("sample.eml not found; aborting")
        return 2
    if not os.path.exists(extractor):
        print("extract_attachments_from_eml.py not found; aborting")
        return 2

    with tempfile.TemporaryDirectory() as td:
        print("Running extractor...")
        cmd = [sys.executable, extractor, sample, td]
        subprocess.run(cmd, check=True)

        # look for hello.txt
        expected = os.path.join(td, "hello.txt")
        if not os.path.exists(expected):
            print("Test failed: expected attachment not found in output dir:", td)
            return 1
        with open(expected, "rb") as f:
            b = f.read()
        if b.strip() == b"Hello, world!":
            print("Test passed: attachment content OK")
            return 0
        else:
            print("Test failed: attachment content mismatch")
            print(b)
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
