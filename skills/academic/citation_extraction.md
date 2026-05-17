# Skill: Citation Extraction

**Type:** Domain — Academic
**Applicable agents:** paper_review_agent

## Purpose
Extracts citation metadata and source traceability before a paper is summarized.

## Required Fields
- Title
- Authors
- Venue or publisher
- Publication year
- URL or DOI when available
- Source type
- Date accessed when the source is current or web-based

## Rules
- Do not invent missing citation fields.
- Mark unavailable fields as `Not available in source`.
- Keep citations separate from interpretation.
