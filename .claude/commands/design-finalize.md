---
description: Phase 4 output — consolidate UX/flows + design system + detailed data into DESIGN-v1.md with its diagrams, confirm the Phase 4 gate, and advance to Phase 5 (Build).
argument-hint: version to finalize, e.g. "v1" (defaults to v1)
---

Invoke the `farm-requirements` skill and run **Phase 4 finalization**.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require all three sub-gates ✅:
   **4a UX & flows confirmed**, **4b design system confirmed**, **4c detailed data
   confirmed**. If any is open, STOP and name which `/design-*` command to run next.
2. Determine the target version from `$ARGUMENTS` (default `v1`).
3. Read `docs/requirements/30-design-decisions.md` and `ARCHITECTURE-<version>.md` and
   `REQUIREMENTS-<version>.md` so the design doc is consistent with all three.
4. Generate **`docs/requirements/DESIGN-<version>.md`** containing:
   - **UX & flows** (from `## UX & flows`): screen inventory, navigation, the `/m/` family
     subset, and the core journey flows — with wireframe/flow diagram checkpoint ids / files.
   - **Design system** (from `## Design system`): typography, color + semantic roles,
     spacing, components, responsive + print rules (Tailwind).
   - **Detailed data & forms** (from `## Detailed data & forms`): per-screen fields,
     validation, defaults, and the service function each screen calls.
   - **Screen → requirement/architecture traceability** (each v1 screen → the `REQ-NNN` it
     serves and the service-layer function / tables it touches).
   - **Open questions / assumptions** carried into Phase 5 (Build).
5. If a diagram still needs (re)drawing, use **Excalidraw** (`ToolSearch` →
   `select:mcp__claude_ai_Excalidraw__read_me,mcp__claude_ai_Excalidraw__create_view`),
   record the **checkpoint id** in the MD, and optionally export SVG/PNG into
   `docs/requirements/`. (Use Whimsical only if the user asks for a shareable link.)
6. Update `docs/requirements/STATUS.md`: mark the **Phase 4 gate** ✅ (design confirmed)
   with today's date, record `DESIGN-<version>.md` under "Finalized versions", and set the
   current phase to **5 — Build**.
7. Tell the user Phase 4 is done and that the Phase 5 (Build) commands will be added when
   they confirm they are ready to start it.

Do not begin implementation, scaffold the project, or write application code in this command.
