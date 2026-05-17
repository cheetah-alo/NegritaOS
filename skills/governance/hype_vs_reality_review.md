# Skill: Hype vs. Reality Review

**Type:** Domain — Governance
**Applicable agents:** ai_trend_radar_agent, blockchain_ai_watcher_agent

## Purpose
Evaluates technology, research, or product claims against evidence of real-world production
readiness. Prevents hype-driven adoption decisions and unsupported dismissal of genuine advances.

## Maturity Classification Framework

### Level 1 — Research
- Exists in papers only
- No public implementation
- Results are benchmark-specific
- Signal: "We propose..." / "Our results suggest..." on a curated dataset

### Level 2 — Prototype / Proof of Concept
- Open-source implementation exists (GitHub, HuggingFace, etc.)
- Runs in controlled conditions
- Not production-tested
- Signal: demos, blog posts, research code with limited documentation

### Level 3 — Early Adopter
- Used in production by a small number of organizations
- Results are promising but not generalizable
- Significant engineering required to operationalize
- Signal: conference case studies, startup deployments, limited benchmarks

### Level 4 — Maturing
- Multiple production deployments across organizations
- Known failure modes are documented
- Community support, tooling ecosystem developing
- Signal: practitioners sharing real-world results, failure postmortems, consultancy demand

### Level 5 — Production Ready
- Battle-tested across diverse production environments
- Predictable behavior under scale and edge cases
- Supported tooling, monitoring, governance frameworks
- Signal: enterprise adoption, regulatory guidance exists, textbook coverage

### Level 6 — Commoditized
- Standard component. Differentiation is in application, not the technology itself
- Signal: included in cloud platform defaults, tutorials for beginners

## Evaluation Protocol

For any technology or claim being evaluated:

1. Identify the maturity level (1–6) with evidence
2. Flag if marketing language exceeds demonstrated capability
3. Identify the use case being claimed — is maturity level 1–6 appropriate for that use case?
4. State what would need to be true for the next maturity level to be reached

## Output Format

```
TECHNOLOGY: [Name]
Claimed Capability: [what is being asserted]
Maturity Level: [1–6] — [label]
Evidence Basis: [what supports this classification]
Hype Flag: [YES / NO] — [if YES, state what is overclaimed]
Relevant for TFM: [YES / NO]
Recommended Action: [adopt / monitor / defer / avoid]
```
