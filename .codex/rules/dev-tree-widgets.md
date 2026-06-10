# Tree Widget Development Rules

- Tree-like UI or data structures must keep node identity stable across renders and state updates.
- Selection, expansion, and filtering state must be deterministic: same input state must produce identical output.
- Rendering code must not mutate the source tree in place; always produce new node objects when state changes.
- Node keys must be stable identifiers (not array indices) to prevent spurious re-renders.
- Large trees (>500 nodes visible) must use virtualized rendering.
