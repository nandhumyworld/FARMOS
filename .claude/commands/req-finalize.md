---
description: Phase 2 output — produce the finalized versioned requirements MD + an Excalidraw context/workflow diagram, and confirm the version-scope gate.
argument-hint: version to finalize, e.g. "v1" (defaults to v1)
---

Invoke the `farm-requirements` skill and run **Phase 2 finalization**.

1. **Gate check.** Read `docs/requirements/STATUS.md` and `10-requirements-register.md`.
   Require at least one `confirmed` requirement. If the register is still all `draft`,
   recommend running `/req-review` first (but allow the user to override).
2. Determine the target version from `$ARGUMENTS` (default `v1`).
3. Generate **`docs/requirements/REQUIREMENTS-<version>.md`** containing:
   - Purpose & the "why" (from `00-big-picture.md`).
   - In-scope requirements for this version, grouped by area, each with its `REQ-NNN`.
   - Explicitly out-of-scope / deferred items (so scope creep is visible).
   - A non-functional requirements section.
   - Open questions / assumptions.
4. **Diagram (Excalidraw — user's explicit choice).** First load the deferred tools:
   `ToolSearch` with `select:mcp__claude_ai_Excalidraw__read_me,mcp__claude_ai_Excalidraw__create_view`,
   then call `read_me` to learn the workflow, then draw a **context / end-to-end workflow
   diagram** of the farm system for this version. Embed the diagram link in the MD.
   (Use Whimsical instead only if the user asks.)
5. Update `docs/requirements/STATUS.md`: mark the **Phase 1 gate** ✅ (requirements
   gathered) and the **Phase 2 gate** ✅ (version scope confirmed) with today's date,
   record which version was finalized, and set the current phase to **3 — Architecture & Stack**.
6. Tell the user Phase 2 is done and that the next step (architecture & stack selection,
   plus the `/arch-*` commands) will be added when they confirm they are ready to start Phase 3.

Do not begin architecture or stack selection in this command.
