#!/usr/bin/env python3
"""
extract_attachments_from_imap.py

Connect to an IMAP server, search messages, and extract attachments to an output directory.

Usage:
  python extract_attachments_from_imap.py --host imap.example.com --user me@example.com --password secret --mailbox INBOX --criteria "ALL" ./outdir

Notes:
  - For Gmail, use host "imap.gmail.com" and prefer an app password or OAuth token.
  - Criteria is an IMAP SEARCH string, e.g. 'ALL', 'UNSEEN', 'SINCE 01-Feb-2025'
"""

import argparse
import imaplib
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


def fetch_and_extract(imap: imaplib.IMAP4_SSL, mailbox: str, criteria: str, out_dir: str) -> None:
    imap.select(mailbox)
    typ, data = imap.search(None, criteria)
    if typ != "OK":
        print("Search failed:", typ, data)
        return
    ids = data[0].split()
    print(f"Found {len(ids)} messages matching '{criteria}'")
    for i, mid in enumerate(ids, 1):
        typ, msg_data = imap.fetch(mid, "(RFC822)")
        if typ != "OK":
            print("Failed to fetch message", mid)
            continue
        raw = msg_data[0][1]
        saved = extract_from_message_bytes(raw, out_dir)
        if saved:
            print(f"[{i}/{len(ids)}] Saved {len(saved)} attachments from message {mid.decode()}")
        else:
            print(f"[{i}/{len(ids)}] No attachments in message {mid.decode()}")


def main():
    ap = argparse.ArgumentParser(description="Extract attachments via IMAP.")
    ap.add_argument("--host", required=True, help="IMAP host (e.g. imap.gmail.com)")
    ap.add_argument("--user", required=True, help="Username / email")
    ap.add_argument("--password", required=True, help="Password or app-password")
    ap.add_argument("--mailbox", default="INBOX", help="Mailbox/folder to search")
    ap.add_argument("--criteria", default="ALL", help="IMAP search criteria")
    ap.add_argument("outdir", help="Output directory")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    imap = imaplib.IMAP4_SSL(args.host)
    try:
        imap.login(args.user, args.password)
    except imaplib.IMAP4.error as e:
        print("Login failed:", e)
        return
    try:
        fetch_and_extract(imap, args.mailbox, args.criteria, args.outdir)
    finally:
        imap.logout()


if __name__ == "__main__":
    main()
