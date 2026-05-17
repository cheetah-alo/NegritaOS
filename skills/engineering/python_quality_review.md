# Skill: Python Quality Review

**Type:** Domain — Engineering
**Applicable agents:** code_review_agent

## Purpose
Reviews Python code for production readiness in DS/ML contexts.
Prioritizes: reproducibility, logging, configuration management, error handling, and maintainability.

## Review Checklist

### Reproducibility (P1 if failing)
- [ ] Random seeds are fixed and configurable (not hardcoded as magic numbers)
- [ ] Dependencies are versioned (`requirements.txt` or `pyproject.toml` with pinned versions)
- [ ] Data paths are configurable, not hardcoded
- [ ] Experiment parameters are in config files, not inline in code

### Logging (P1 if absent)
- [ ] Uses `logging` module, not `print()`
- [ ] Log levels are appropriate: DEBUG for dev, INFO for production milestones, WARNING/ERROR for exceptions
- [ ] Logs include: timestamp, module name, key parameter values at run start
- [ ] Errors are logged with stack trace, not silently swallowed

### Configuration Management (P1 if failing)
- [ ] No hardcoded paths, credentials, or environment-specific values
- [ ] Config loaded from YAML, JSON, or environment variables
- [ ] Config schema is validated at startup
- [ ] No credentials in code or tracked files

### Error Handling (P1 if absent for critical paths)
- [ ] Expected failure modes are explicitly handled
- [ ] Exceptions are specific, not bare `except:` blocks
- [ ] Failure messages are informative enough to diagnose without a debugger

### Code Structure (P2)
- [ ] Functions have single responsibility
- [ ] Function length: max ~50 lines (flag for review above this)
- [ ] No duplicated logic across functions or modules
- [ ] Docstrings on public functions and classes

### Data Handling Safety (P0/P1)
- [ ] Input data is validated before processing
- [ ] Schema assumptions are checked explicitly
- [ ] Missing value handling is explicit, not implicit

### Testing (P2)
- [ ] Unit tests exist for data transformation functions
- [ ] No tests = technical debt, not a blocker unless deployment-critical
- [ ] If no tests: add to recommendations with priority

## Output Format (per issue)
```
[SEVERITY] location: [file:function or file:line]
Issue: [what is wrong]
Risk: [what could go wrong in production]
Fix: [specific recommendation]
```
