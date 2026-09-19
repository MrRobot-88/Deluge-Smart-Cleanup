# Security Policy

## Reporting a vulnerability

Please do not publish credentials, private tracker details, NAS paths, or other sensitive information in an issue.

For security-sensitive reports, use GitHub's private vulnerability reporting / security advisory features when available.

## Operational safety

Deluge Smart Cleanup runs in dry-run mode by default. Review its output before enabling `--live`.

Use environment variables or protected local files for passwords and credentials. Never commit real Deluge passwords, VPN credentials, API keys, or tokens to this repository.

This project can remove torrents and data when live mode is explicitly enabled. Test with non-critical data first and maintain backups appropriate for your environment.
