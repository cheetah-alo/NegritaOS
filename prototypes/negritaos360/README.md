# NegritaOS 360 — interactive design prototype

Local NegritaOS 360 interface in the accepted Tepulume visual style. **Demo** uses only synthetic fixtures: Atlas, Brisa and Faro do not represent real client projects. **Local** reads explicitly allowed projects and their configured agents, skills and rules from the local Python service. Neither mode reads Brain sessions, Git activity, analytics, remote fonts or paid services.

## Run

From this worktree root, launch the integrated server on loopback only:

```sh
PYTHONPATH=src /Users/jackyb-cqi/repos/NegritaOS/.venv-pr-quality/bin/python -m negrita_brain.dashboard_local_server --port 8791 --access-file .local/dashboard-access.json
```

Open `http://127.0.0.1:8791/?source=local#agents` for the agent inventory, or `#projects` for projects. The Fuente selector switches between Demo and Local. The server serves only this prototype directory, `/api/v1/catalog`, and `/api/v1/capabilities`, with no public network binding. Its local policy file is Git-ignored and must be owned by the current user with mode `0600`. An absent file permits no projects. Never commit client grants or local policy data.

Example synthetic policy schema, with no grants:

```json
{"schema_version":1,"project_client_grants":[],"unknown_client_projects":[]}
```

For a separate static Demo preview, the old command remains valid:

```sh
python3 -m http.server 8790 --bind 127.0.0.1 --directory prototypes/negritaos360
```

The static preview cannot serve Local mode and will show a read error if it is selected.

```sh
node --test prototypes/negritaos360/*.test.mjs
```

## Review paths

- Panorama → project → filtered capability catalog → detail drawer → related capability.
- Capacidades → type/search filters; missing usage is “Sin medir”, never zero.
- Agentes → compact, keyboard-accessible directory. Each row shows a readable name, a short preview of the canonical description, and the project count; expand a row for its full description, technical ID, configuration state, and permitted project names. The project button opens that project's view. Global client, project, and search filters apply before grouping.
- Conocimiento → capability/knowledge views → depth and zoom → accessible node list → detail.
- Flujos → individual steps or simulated advance; no executable agent action or approval.
- Brain y Git → synthetic references only; no claim of live status or deployment.
- Interface-state selector → loading, empty, read error, stale snapshot; reset restores demo.
- Local → authorized project catalog on Panorama/Proyectos, a dedicated Agentes view, and configured agents, skills and rules on Capacidades. Filter by project, client, type and search. Other sections explicitly say their local source is not connected yet. Use the source selector to return to Demo.

## Source boundaries

`data.mjs`: synthetic Demo fixtures. `state.mjs`: Demo selectors. `components.mjs`: reusable controls. `graph.mjs`: bounded synthetic SVG. `views.mjs`: Demo views. `local-catalog.mjs` and `local-capabilities.mjs`: same-origin API validation and authorized-result filters. `local-view.mjs` and `local-capability-view.mjs`: Local presentation. `app.mjs`: source switching and event wiring. The CSS files keep visual layers separate. The backend source adapters and APIs live in `src/negrita_brain/dashboard_local_server.py`, `dashboard_local_service.py`, and `dashboard_capability_catalog.py`.

Demo short display statuses are illustrative labels, **not** the domain contract. Python dataclasses and read-only local project/capability catalogs now exist, but there is no connected plan activation, Brain/Git usage, goal outcome measurement or production API. Agent IDs and descriptions come from permitted project registries and `integrator.yaml`; known human aliases come from the canonical router/agent bridge (Pablo, Casilda, Gisel, Vera). Names without aliases are generated from stable IDs. Missing descriptions are shown explicitly, not inferred. Local capability states describe registry configuration only; they do not prove use, evidence validity or a healthy runtime. The Local project count is the number of entries visible under the local policy. Cytoscape.js and NetworkX remain future candidates, not dependencies here.

See the [plan review and UX decision](../../docs/negritaos_360_ux_plan_review__updated_20260927_134112.md) for the Astra findings, proposed contracts and traceable next tasks. Audience: the NegritaOS owner and implementation team. Frontend owns this prototype; update it when the user changes the visual direction or an interaction contract changes.

## Visual direction

An operational observatory: petroleum-green navigation, warm ivory canvas, restrained amber/terracotta attention states, serif page titles and legible system-font tables. A shared detail drawer keeps provenance near the decision. Graphs complement tables rather than replacing them.

### Alternative: Tepulume design system and project tracking

The default is now the Tepulume adaptation: exact petroleum-blue/magenta/warm-white tokens, upright Montserrat/Instrument Sans typography, near-square corners and restrained borders. Use the **Diseño visual** selector to compare with the original Observatorio. `tepulume-theme.css` is an adapter, not a rebrand or an imported public landing page.

Existing font binaries were copied locally from the user-selected Tepulume repo's `documents/lubricantes_venezuela/reproducibilidad/{Montserrat,InstrumentSans}.ttf` into `assets/fonts/`. They are Git-ignored preview assets; absent them, the CSS falls back to system fonts. No remote font calls. Review distribution/license requirements before promoting assets.

In Demo, open `http://127.0.0.1:8791/#tracking`. Client selection scopes synthetic projects, capabilities, graphs and plans. `tracking-data.mjs` owns fixtures, `tracking-model.mjs` owns the simulation rules, `tracking-view.mjs` owns view rendering, and `tracking-controller.mjs` owns forms. Demo interactions reset on reload; the separate, Git-ignored Local policy persists until the user edits it.

Try: Atlas → Proponer cambio → add functionality → compare versions → review activation → explicitly confirm. Delivery moves from 2/5 to 2/6 while old activation history remains. Changing F-02's criterion instead requires new evidence. Brisa demonstrates first activation; Faro cannot activate without a versioned design. Feature drawers can append synthetic accepted evidence when dependencies are met. Completing functionality does not mark the goal achieved.

See the [client, tracking and versioning proposal](../../docs/negritaos_360_project_tracking__updated_20260927_141408.md). Future production writes need backend authorization, concurrency and immutable evidence contracts; this simulation grants no real authority.
