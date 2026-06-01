---
id: security
domain: dev
enforcement: strict
applyTo: [python, sql, config, ci, repo]
depends_on:
  - coding-standards
  - logging
  - error-handling
provides:
  - secrets-handling
  - pii-policy
  - gitignore-policy
description: >
  Repository-wide security policy for the ML-as-code churn platform. Covers
  secrets, credentials, .env files, .gitignore hygiene, PII handling in code,
  tests, docs, logs, and AI-generated examples. Loaded only for engineering
  modes MR / CR / DQ as defined by the NegritaOS router.
version: 1.0.0
priority: critical
---

# Security & Secrets Standard

This rule is **strict** and applies to every engineering-mode change.
It complements the one-line note in `dev-coding-standards.md` \u00a79
("Sensitive Files") with concrete, enforceable rules.

---

## 1. Secrets, Tokens, Credentials

### 1.1 Forbidden in the repo (any branch, any history)

- API keys, OAuth tokens, JWT signing keys
- Cloud credentials (GCP service-account JSON, AWS access keys, Azure SAS)
- Database connection strings with embedded passwords
- Private keys (`*.pem`, `*.key`, `id_rsa`)
- BigQuery service-account JSON files
- MLflow tracking tokens
- Slack / GitHub / Notion / Confluence personal access tokens

### 1.2 Allowed pattern

- Load secrets from environment variables resolved at runtime.
- Local development: read from `.env` (which MUST be gitignored, see \u00a73).
- CI / production: read from the platform's secret manager (GCP Secret
  Manager, AWS Secrets Manager, Azure Key Vault, GitHub Actions secrets).

Example:

```python
import os
BQ_PROJECT = os.environ["BQ_PROJECT"]              # required
MLFLOW_URI = os.getenv("MLFLOW_URI", "file:./mlruns")  # optional with default
```

NEVER:

```python
BQ_PROJECT = "my-prod-project"                   # hard-coded -> forbidden
OPENAI_API_KEY = "sk-..."                        # forbidden
```

### 1.3 Pre-commit secret scanning

A pre-commit hook MUST run a secret scanner (recommended: `gitleaks` or
`detect-secrets`) and block the commit on any positive match. False
positives are resolved by adding the match to the scanner's allowlist
file, never by removing the hook.

---

## 2. PII and Sensitive Customer Data

### 2.1 Forbidden in code, tests, docs, fixtures, logs

- Real customer IDs, MSISDNs (phone numbers), IMEIs, IMSIs
- Real names, emails, postal addresses
- Real billing amounts tied to identifiable customers
- Any field flagged as PII in the dataset contract

### 2.2 Allowed in tests and examples

- Synthetic IDs (`customer_id=1001`, `msisdn="+34900000001"`)
- Faker-generated names / emails
- Hashed or tokenised identifiers when realistic shape is required

### 2.3 Logging

- Logs MUST NOT print raw PII. When a customer identifier must appear in a
  log line for debugging, log a hashed or truncated form
  (`customer_id_hash=ab12cd34`).
- Stack traces that may carry PII (e.g., a record dict) MUST be scrubbed
  before being emitted at WARNING or above.

---

## 3. `.env` and `.gitignore` Hygiene

### 3.1 Mandatory entries in `.gitignore`

The repository `.gitignore` MUST contain at minimum:

```
.env
.env.*
!.env.example
*.pem
*.key
*-credentials.json
*-service-account.json
.secrets/
```

### 3.2 `.env.example`

A committed `.env.example` (or `.env.template`) MUST list every environment
variable the code consults, with placeholder values and a comment
explaining each. This is the contract between operator and code.

### 3.3 Never commit

- `.env` (any environment-specific values)
- Generated credential files downloaded from cloud consoles
- Notebook outputs that leak environment variables (clear outputs before
  commit, see [notebooks.md](notebooks.md))

---

## 4. Code Patterns

### 4.1 Boundary validation

All credential loading MUST happen at one boundary (a `settings.py` or
`config.py` module). Business logic receives credentials via dependency
injection, never via direct `os.environ` reads scattered through the code.

### 4.2 No credentials in error messages

```python
# BAD
raise ConnectionError(f"Failed to connect with token {api_token}")

# GOOD
raise ConnectionError("Failed to connect: invalid or expired credentials")
```

### 4.3 No credentials in log context

```python
# BAD
logger.info("Calling API", extra={"token": api_token})

# GOOD
logger.info("Calling API", extra={"token_present": bool(api_token)})
```

---

## 5. Dependencies and Supply Chain

- Pin dependency versions in `pyproject.toml` / `uv.lock`.
- Run `pip-audit` (or `uv pip audit`) in CI; block on high/critical CVEs.
- New direct dependencies require a one-line justification in the PR
  description.

---

## 6. AI-Generated Code

AI agents (Claude, Codex, Copilot) MUST NOT:

- Invent example secrets that look real (e.g., a plausible-looking API key).
- Echo back any secret found in the conversation context.
- Generate code that bypasses the boundary in \u00a74.1.

AI agents MUST:

- Use obvious placeholders (`<YOUR_API_KEY>`, `"REDACTED"`) in examples.
- Flag any secret-shaped string they detect in user-provided code and ask
  whether it should be rotated.

---

## 7. Pre-Commit Checks (mandatory for engineering modes)

The following MUST be green before any commit:

| Check | Tool | Failure action |
| --- | --- | --- |
| Secret scan | `gitleaks` or `detect-secrets` | Block commit; rotate secret if exposed. |
| `.gitignore` audit | manual diff review | Block commit; restore missing entries. |
| PII scan in tests/fixtures | `grep` for known PII patterns | Block commit; replace with synthetic data. |
| Dependency CVE scan | `pip-audit` | Block PR on high/critical. |

---

## 8. Learnings

```
## Learnings
* Centralise credential loading in one module to limit the blast radius of leaks. (1)
* `.env.example` must list every variable the code reads, or operators will misconfigure prod. (1)
* AI-generated examples must use obvious placeholders; plausible-looking keys train muscle memory for the wrong pattern. (1)
```
