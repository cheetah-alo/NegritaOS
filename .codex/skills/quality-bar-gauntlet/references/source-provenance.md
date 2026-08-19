# Source Provenance

This NegritaOS skill adapts the evaluator-loop pattern described by the public
RoboNuggets `gauntlet-loop` repository:

- Repository: `https://github.com/robonuggets/gauntlet-loop`
- Source skill reviewed: the upstream `gauntlet-loop` skill entrypoint file.
- License declared by source repository: CC BY 4.0
- Technique attribution in source repository: Matt Shumer, "Gauntlet Loop"

NegritaOS does not copy the source skill verbatim. The adaptation keeps the
general pattern of a real quality bar, separate builder/critic contexts, and
evidence-backed comparison, while replacing Claude-specific mechanics with
NegritaOS project routing, Brain gates, catalog profiles, document-control
rules, and provider-neutral validation.
