# Rule Compliance Gate (Agent Routing)

This skill is mandatory before writing/modifying code.

Auto-invoke when:
- Creating or editing any Python modules
- Refactoring repo structure
- Writing execution scripts for analyses
- Writing tests
- Modifying SQL queries or loaders
- Producing plots/reports outputs

If user did not specify a profile:
- Analytics execution => use `analysis-run`
- Audit/review => use `review`
- Refactor => use `refactor`
