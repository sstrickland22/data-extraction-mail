# Contributing to Email Attachment Extractor

Thank you for your interest in contributing to this project! Here's how you can help:

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/data-extraction-mail.git
   cd data-extraction-mail
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-feature
   ```

## Making Changes

- Follow **PEP 8** style guidelines
- Add docstrings to new functions
- Keep functions focused and testable
- Use descriptive commit messages:
  ```
  feat: add OAuth2 support for Gmail
  fix: handle malformed MIME headers
  docs: update README with examples
  ```

## Testing Your Changes

Before submitting a PR, test your code:

```bash
# Run the demo test
python3 run_extract_test.py

# Check syntax
python3 -m py_compile extract_attachments_from_eml.py extract_attachments_from_imap.py
```

All tests must pass before your PR can be merged.

## Submitting a Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/my-feature
   ```
2. **Open a Pull Request** on GitHub
3. **Write a clear description** of what your PR does
4. **Wait for CI checks** to pass
5. **Respond to feedback** if reviewers suggest changes

## Code Guidelines

### Function Documentation
```python
def extract_from_message_bytes(message_bytes, output_dir):
    """Extract attachments from email message bytes.
    
    Args:
        message_bytes: Email message as bytes
        output_dir: Directory to save attachments
        
    Returns:
        List of extracted filenames
    """
```

### Error Handling
- Validate file paths before writing
- Handle connection errors gracefully
- Provide clear error messages

## Feature Ideas

Want to contribute but not sure what to work on? Consider:

- **OAuth2 authentication** for Gmail and Outlook
- **PST/MBOX support** for archive formats
- **Attachment filtering** by type, size, or date
- **Unit tests** for edge cases
- **Performance improvements** for large batches

## Questions?

Open an issue on GitHub to discuss:
- Bug reports
- Feature requests
- Documentation improvements
- Questions about the codebase

## License

By contributing, you agree your code will be licensed under the MIT License.
