# Real-time CAMEO-style validation bus — UEFN ↔ OpenStructure ↔ GitHub Pages

Status: design proposal (new, this pass). Extends
`03-org-docs/UEFN-MULTIPLAYER-RUNTIME-ARCHITECTURE.md`, which already
established the one constraint everything below is built around.

## 1. The constraint this proposal designs around, not against

`UEFN-MULTIPLAYER-RUNTIME-ARCHITECTURE.md` §1 already established, and a
fresh check (Aug 2026) confirms it is still true: Verse runs inside
Epic's sandbox and cannot open network sockets or call out to any
external service — including OpenStructure — while a match is live.
**This is a platform-level rule, not a qFoldIT limitation, and no design
below tries to route around it.** The goal instead is to get the closest
possible thing to "live global validation bus" within that rule, using
the same two-clock model the workspace already validated for the five
unlocked patterns.

## 2. Target architecture

```
[ Ops / Sci panel ]        [ UEFN island, live match ]        [ World, live ]
  target created              player places blocks               GitHub Pages
        |                     "Validate" pressed                      ^
        v                            |                                |
  qfoldit-scene-export         Verse: read placed                     |
  (already real, tested)       block coordinates,                     |
        |                      publish to Verse                       |
        v                      Persistence / a                        |
  building_grid_mapper.py  <-- per-session result                     |
  places BuildingProp/          object                                |
  BuildingFloor at authoring     |                                    |
  time (baked, per island)       v                                    |
        |                  match ends / player                        |
        v                  exits -> Persistence                       |
  Verse script generated,   value becomes readable                    |
  playback/trigger logic    by an external process                    |
  only, no science logic          |                                   |
                                   v                                  |
                       external reconciliation service                |
                       (new component, this proposal)                 |
                       - reads published Persistence data             |
                       - runs the SAME coordinates through            |
                         OpenStructure (lDDT / QS-score) --------------+
                       - writes result_hash + score into
                         scientific-contribution-record (0.2)
                       - pushes updated world STATE to
                         GitHub Pages (qfoldit.github.io)
```

## 3. What each piece actually is

1. **Target authoring (ops panel, Huawei/biotech engineer).** Unchanged
   from the existing pipeline: a `reference_mcp` job (e.g.
   `protein_design_mcp`) runs once, for real, off-platform. This is
   already the documented authoring-time flow.
2. **Procedural level assembly.** Already real and tested:
   `building_grid_mapper.py` (residue/module placements) +
   `qfoldit-scene-export`'s `ScenePlan` model turn that target into an
   ordered `BuildingProp`/`BuildingFloor` placement sequence — the level
   *does* get generated dynamically per target, at authoring time, per
   island build.
3. **In-match "Validate" button.** What Verse can honestly do here: read
   the coordinates of the blocks the player actually placed (this is
   local, in-sandbox data — fully allowed), compare them against the
   already-baked reference sequence (a local, in-sandbox comparison —
   also already the documented `UEFN-BUILDING-GAMEPLAY-ALGORITHM.md` §3
   pass/fail check), show the in-match result immediately, and **publish
   the session's placement record via Verse Persistence** — the one
   channel Verse *is* allowed to write through.
4. **External reconciliation service (the new piece this proposal adds).**
   A small service outside the sandbox — natural home is alongside the
   existing `UEFN-TOOLBELT` external MCP process — that:
   - polls or is notified of new Persistence data,
   - re-runs the same placement record through real OpenStructure
     scoring (lDDT / QS-score against the authoring-time reference
     structure),
   - writes the score into the `scientific-contribution-record` (schema
     `0.2`, already defined) as the `result_hash`/`evidence_level`
     fields,
   - pushes the updated aggregate as the single world **STATE** object to
     `qfoldit.github.io` (GitHub Pages), e.g. via a scheduled GitHub
     Actions job committing a generated `state.json` + the existing
     dashboard reading it.
5. **World page.** A static page reading `state.json` — no backend of its
   own needed, consistent with GitHub Pages' own constraints.

## 4. Honest latency characterization

This is **near-real-time global state, not literally live in-match
OpenStructure scoring.** The in-match "Validate" result the player sees
instantly is a local baked-sequence match (already real, already
working). The OpenStructure-verified score that lands on the world page
follows shortly after, on the reconciliation service's poll interval —
seconds to low minutes depending on how Persistence read-back is wired,
per `UEFN-MULTIPLAYER-RUNTIME-ARCHITECTURE.md` §5's still-open question
on read-back access. That question should be resolved first; it is the
one unknown this whole proposal depends on.

## 5. What this needs, in build order

1. Resolve `UEFN-MULTIPLAYER-RUNTIME-ARCHITECTURE.md` §5: confirm the
   external MCP process can read back published Verse Persistence values.
2. Stand up the reconciliation service (new; smallest useful version:
   poll → score → append to a JSON log).
3. Wire `scientific-contribution-record` (0.2) writes from step 2.
4. Add the GitHub Actions job that regenerates `state.json` and publishes
   it to `qfoldit.github.io`.
5. Point the dashboard (see the HTML deliverable) at `state.json` once it
   exists — until then it reflects the specs/docs snapshot only.

## 6. Explicitly out of scope here (unchanged from existing docs)

Live, mid-match OpenStructure calls; live two-independent-run replication
mid-match (`arena_showdown`'s corrected description, §3 of the runtime
doc, already covers what *is* honestly buildable there); any workaround
of the Verse sandbox.
