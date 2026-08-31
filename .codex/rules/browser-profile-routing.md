# Canonical Rule Pointer: Browser Profile Routing

Load and enforce:

- `../../rules/global/browser_profile_routing_rule.md`
- `../../core/orchestration/browser_profile_routing.yaml`

Resolve authenticated Brave access with:

```bash
python3 /Users/jackyb-cqi/repos/NegritaOS/scripts/open_governed_browser.py \
  --root "$PWD" --purpose <purpose> --url <url> --dry-run
```

Do not select another browser profile when resolution is blocked.
