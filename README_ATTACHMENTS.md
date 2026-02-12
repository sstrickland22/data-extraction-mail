# Attachment extractor

This folder contains two small Python scripts to extract attachments from email messages.

- `extract_attachments_from_eml.py`: extract attachments from a single `.eml` file or from all `.eml` files in a directory.
- `extract_attachments_from_imap.py`: connect to an IMAP server and extract attachments matching an IMAP search criteria.

Quick examples (zsh):

Single EML:
```
python3 extract_attachments_from_eml.py /path/to/message.eml ./attachments
```

Directory of EMLs:
```
python3 extract_attachments_from_eml.py --dir /path/to/eml_folder ./attachments
```

IMAP (example):
```
python3 extract_attachments_from_imap.py --host imap.example.com --user you@example.com --password 'yourpassword' --mailbox INBOX --criteria 'UNSEEN' ./attachments
```

Notes:
- Scripts use only Python standard library (no extra packages required).
- For Gmail, prefer using an app password or OAuth token.

Quick test (run from repo root):
```
python3 run_extract_test.py
```

This will extract the attachment from `sample.eml` into a temporary directory and verify the saved file's contents.
