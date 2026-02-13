#!/usr/bin/env python3
"""
extract_attachments_from_eml.py

Extract attachments from a single .eml file or all .eml files in a directory.

Usage:
  python extract_attachments_from_eml.py /path/to/message.eml /output/dir
  python extract_attachments_from_eml.py --dir /path/to/eml_folder /output/dir
"""

import argparse
import os
import re
from email import policy
from email.parser import BytesParser


def sanitize_filename(name: str) -> str:
    name = os.path.basename(name or "")
    name = re.sub(r'[^A-Za-z0-9._-]', '_', name)
    return name or "attachment"


def save_attachment(payload_bytes: bytes, out_dir: str, filename: str) -> str:
    filename = sanitize_filename(filename)
    base, ext = os.path.splitext(filename)
    candidate = filename
    i = 1
    while os.path.exists(os.path.join(out_dir, candidate)):
        candidate = f"{base}_{i}{ext}"
        i += 1
    out_path = os.path.join(out_dir, candidate)
    with open(out_path, "wb") as f:
        f.write(payload_bytes)
    return out_path


def extract_from_message_bytes(msg_bytes: bytes, out_dir: str) -> list:
    saved = []
    msg = BytesParser(policy=policy.default).parsebytes(msg_bytes)
    for part in msg.walk():
        disposition = part.get_content_disposition()
        filename = part.get_filename()
        if disposition == "attachment" or filename:
            payload = part.get_payload(decode=True) or b""
            if not filename:
                ext = part.get_content_subtype() or "bin"
                filename = f"attachment.{ext}"
            path = save_attachment(payload, out_dir, filename)
            saved.append(path)
    return saved


def process_eml_file(path: str, out_dir: str) -> None:
    with open(path, "rb") as f:
        b = f.read()
    saved = extract_from_message_bytes(b, out_dir)
    if saved:
        print(f"Saved {len(saved)} attachment(s) from {path}:")
        for p in saved:
            print("  -", p)
    else:
        print(f"No attachments found in {path}")


def main():
    ap = argparse.ArgumentParser(description="Extract attachments from EML files.")
    ap.add_argument("source", help="Path to .eml file or folder (use --dir for folder mode)")
    ap.add_argument("outdir", help="Output directory to save attachments")
    ap.add_argument("--dir", action="store_true", dest="is_dir", help="Treat source as a directory of .eml files")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    if args.is_dir:
        for root, _, files in os.walk(args.source):
            for fn in files:
                if fn.lower().endswith(".eml"):
                    process_eml_file(os.path.join(root, fn), args.outdir)
    else:
        process_eml_file(args.source, args.outdir)


if __name__ == "__main__":
    main()
