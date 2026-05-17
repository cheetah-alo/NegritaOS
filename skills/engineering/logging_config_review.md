# Skill: Logging and Config Review

**Type:** Domain — Engineering
**Applicable agents:** code_review_agent

## Purpose
Reviews whether code exposes enough configuration and logging for production operation.

## Checks
- Runtime configuration is not hardcoded.
- Logs include phase, entity, and failure context.
- Errors preserve root cause information.
- Sensitive values are not logged.
- Long-running workflows expose progress.
