---
description: Phase 3 output — consolidate stack + domain model + system architecture into ARCHITECTURE-v1.md with its diagrams, confirm the Phase 3 gate, and advance to Phase 4 (Design).
argument-hint: version to finalize, e.g. "v1" (defaults to v1)
---

Invoke the `farm-requirements` skill and run **Phase 3 finalization**.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require all three sub-gates ✅:
   **3a stack confirmed**, **3b domain model confirmed**, **3c architecture confirmed**.
   If any is open, STOP and name which `/arch-*` command to run next.
2. Determine the target version from `$ARGUMENTS` (default `v1`).
3. Read `docs/requirements/20-architecture-decisions.md` and `REQUIREMENTS-<version>.md`.
4. Generate **`docs/requirements/ARCHITECTURE-<version>.md`** containing:
   - **Chosen stack** and the why (from `## Stack`), tied to the NFRs it satisfies.
   - **Data/domain model** (from `## Domain model`) with the resolved OD-1 / OD-3 / OD-5,
     and the ER/domain diagram (embed its Excalidraw checkpoint id).
   - **System architecture** (from `## System architecture`): components, API, auth/roles,
     Coolify deployment topology, audit logging — with the architecture diagram checkpoint id.
   - **Non-functional requirements** carried from v1 and how the architecture meets them.
   - **Requirement → architecture traceability** (each v1 `REQ-NNN` → where it is handled).
   - **Open questions / assumptions** carried into Phase 4 (Design).
5. If a diagram still needs (re)drawing, use **Excalidraw** (`ToolSearch` →
   `select:mcp__claude_ai_Excalidraw__read_me,mcp__claude_ai_Excalidraw__create_view`).
   Excalidraw renders inline and gives no public URL — record the **checkpoint id** in the MD.
   (Use Whimsical only if the user asks for a shareable link.)
6. Update `docs/requirements/STATUS.md`: mark the **Phase 3 gate** ✅ (architecture confirmed)
   with today's date, record `ARCHITECTURE-<version>.md` under "Finalized versions", and set
   the current phase to **4 — Design**.
7. Tell the user Phase 3 is done and that the Phase 4 (Design) commands will be added when
   they confirm they are ready to start it.

Do not begin UX/detailed design or write application code in this command.
