# Observable Development Rules

- Observable or callback-driven components must expose explicit state transitions (start, update, complete, error).
- Public observable events must have stable names and documented payload fields; rename requires a version bump.
- Long-running observable flows must log phase-level progress and failures via `PhaseLogger`.
- Observers must not modify shared state directly; use typed event payloads and let consumers handle side effects.
- Unsubscribe or dispose observables when the consuming component or pipeline phase is torn down.
