---
name: testing-coverage
description: >
  Provider-neutral testing and coverage gates for backend, frontend, data
  contracts, and browser workflows.
  Use for behavior changes, bug fixes, API changes, and refactors.
license: Apache-2.0
metadata:
  author: negritaos
  version: "1.0"
  scope: [root, backend, frontend, data_analytics]
---

# Testing And Coverage

Write the regression test before or with the behavior change. Cover the happy
path, validation and error paths, edge cases, logical contract fields, and
provider adapter behavior where applicable.

Use the repository's declared runners rather than assuming Go, pytest, or a
single frontend tool. Report exact commands and results for unit tests,
contract tests, integration tests, browser/E2E checks, and coverage. A visual
change also needs connected-page and state coverage.

Never commit coverage directories, temporary files, screenshots, generated
outputs, local settings, credentials, or other run artifacts.
