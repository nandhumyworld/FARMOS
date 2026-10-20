---
description: Phase 4a — design the farmOS v1 UX & workflows (screen inventory, navigation, wireframe-level flows for the core journeys + the /m/ family subset). Produces Excalidraw wireframes/flow diagrams.
argument-hint: (optional) a flow to start with, e.g. "quick sale"
---

Invoke the `farm-requirements` skill and run **Phase 4a: UX & Workflow Design**.

**Scope is v1 only** (per the skill's prime directive) — design only the v1 in-scope
journeys; leave v2/later flows as notes.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 3 gate** ✅
   (architecture finalized). If it is open, STOP and tell the user to run `/arch-finalize`.
2. Read `docs/requirements/REQUIREMENTS-v1.md` and `ARCHITECTURE-v1.md` (esp. the system
   architecture: the **service-layer functions** `record_sale` / `record_harvest` /
   `run_production` / `procure` / corrections, the **roles** admin vs owner/family, and the
   **`/`, `/m/`, `/admin/`** route split) so flows map onto what the system actually does.
3. **Reuse `superpowers:brainstorming`** — walk the design **one decision at a time**:
   - **Screen inventory & navigation** — what pages exist and how they're reached
     (dashboard/P&L, entities, harvest, inventory/stock, production, procurement, quick
     sale, contacts, reports, admin), and the **`/m/` phone-first family subset** (which
     few flows it exposes, per SD-3).
   - **Wireframe-level flows** for the core v1 journeys: **quick sale** (price snapshot,
     payment/credit), **harvest** (opens batch), **production run** (multi-input → output,
     tally), **procurement** (buy-in → outsourced batch + vendor expense, REQ-036),
     **contacts**, **reports** (whole-farm + per-batch P&L, month/year/custom, print/share),
     and the **negative-stock "shortfall to procure"** surface.
   For each, present 2–3 concrete options with trade-offs and a recommendation; let the
   user choose. Keep it to structure/flow — visual styling is `/design-system` (4b).
4. **Diagram (Excalidraw).** Load tools: `ToolSearch` with
   `select:mcp__claude_ai_Excalidraw__read_me,mcp__claude_ai_Excalidraw__create_view`,
   call `read_me`, then draw **wireframes and/or a navigation/flow diagram** of the v1
   screens. Record the **checkpoint id** (Excalidraw gives no public URL). Optionally also
   export an SVG/PNG into `docs/requirements/` for a shareable file.
5. Record confirmed decisions in **`docs/requirements/30-design-decisions.md`** under a
   `## UX & flows` section as dated decisions (what + why + which `REQ-NNN` it serves +
   diagram checkpoint id). Create the file if absent, with empty `## Design system` and
   `## Detailed data & forms` headings.
6. When the user confirms the flows are settled, log a **Phase 4a sub-gate**
   ("UX & flows confirmed") ✅ in `STATUS.md` with today's date, and tell them to run
   `/design-system`.

Do not choose fonts/colors/components (that is `/design-system`), design field-level
forms/validation (that is `/design-data`), or write application code in this command.
