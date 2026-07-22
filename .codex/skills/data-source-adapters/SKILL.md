---
name: data-source-adapters
description: >
  Use when selecting, routing, querying, validating, or documenting BigQuery,
  PostgreSQL, file, API, or other data-source adapters.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, backend, data_analytics]
  auto_invoke:
    - "Changing data source routing or physical object references"
    - "Adding or reviewing BigQuery or PostgreSQL adapters"
    - "Changing logical data contracts backed by external sources"
---

# Data Source Adapters

Read `skills/engineering/data_source_adapter_governance.md` and the active
project registry before making changes.

The provider is an implementation detail. Configuration owns source selection
and physical references; adapters own dialect-specific queries; domain
contracts own logical fields; routes own validation; frontends consume only
logical payloads.

For BigQuery, inspect partition and cost controls. For PostgreSQL, inspect
schema/relation routing, transaction behavior, and index-sensitive queries.
Both providers must preserve the same public contract when the project says
the contract is shared.
