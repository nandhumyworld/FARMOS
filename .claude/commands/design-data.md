---
description: Phase 4c — design farmOS v1 detailed forms & data entry (per-screen fields, validation, defaults, which service each screen calls, empty/error states). Bridges design → build. No app code.
argument-hint: (optional) a screen to start with, e.g. "quick sale form"
---

Invoke the `farm-requirements` skill and run **Phase 4c: Detailed Data & Forms Design**.

**Scope is v1 only** — field-level design for the v1 screens confirmed in 4a; v2 fields
stay as notes.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 4b sub-gate**
   ("design system confirmed") ✅. If it is open, STOP and tell the user to run
   `/design-system`.
2. Read `docs/requirements/30-design-decisions.md` (`## UX & flows`, `## Design system`),
   `ARCHITECTURE-v1.md` (the **domain model** — 18 tables, field lists, Decimal money/qty,
   accrual income, StockMovement ledger, REQ-036 Procurement/origin/vendors) and the
   **service-layer functions** each screen must call.
3. **Reuse `superpowers:brainstorming`** — for each core screen/form, settle **one at a
   time**:
   - **Fields** (bound to which model/attribute), **required vs optional**, **defaults**
     (e.g. price snapshot from catalog, today's date, fiscal-year context), **units**,
     **Decimal precision** for money & quantities.
   - **Validation & rules** — e.g. batch-number uniqueness, **negative stock allowed**
     (warn, don't block; surface shortfall), payment ≤ outstanding, vendor required on
     procurement, atomic posting via the service function (`record_sale`/`record_harvest`/
     `run_production`/`procure`).
   - **Which service function** each submit calls, and the **edit-in-place correction**
     behaviour (atomic re-post; auditlog).
   - **Empty / loading / error states** and HTMX partial-update points.
   Present concrete options with a recommendation; let the user choose.
4. Record confirmed decisions in **`docs/requirements/30-design-decisions.md`** under the
   `## Detailed data & forms` section as dated decisions (screen → fields/validation/
   defaults/service + which `REQ-NNN` it serves). Note any diagram checkpoint id if drawn.
5. When the user confirms the detailed data/forms are settled, log a **Phase 4c sub-gate**
   ("detailed data confirmed") ✅ in `STATUS.md` with today's date, and tell them to run
   `/design-finalize`.

Do not change the stack or domain model (those are finalized in `ARCHITECTURE-v1.md` — if a
real gap appears, surface it, don't silently redesign), build components, or write
application code in this command.
