# Security Policy

## Supported Versions

Security fixes will be applied to the `main` branch. No long-term support branches are currently maintained.

## Reporting a Vulnerability

If you discover a security vulnerability:

1. DO NOT create a public GitHub issue initially.
2. Email the maintainer (open an issue asking for a secure contact channel if no email is visible).
3. Provide a minimal reproduction and impact assessment if possible.

You will receive a response within 7 days. If the issue is confirmed, a coordinated disclosure process will be followed.

## Scope

-   Code execution vulnerabilities
-   Sensitive data leakage (API keys, credentials)
-   Insecure dependency usage
-   Injection / deserialization vulnerabilities

## Out of Scope

-   Vulnerabilities in third‑party dependencies unless introduced by project code
-   Social engineering
-   Denial of service from unrealistic resource exhaustion scenarios for an educational project

## Handling Secrets

-   Use `.env` – never commit real keys
-   Git history scans are performed; rotate compromised keys immediately

Thank you for helping keep the community safe.
