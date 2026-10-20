---
description: Phase 5a — settle the DESIGN-v1 §5 Build carry-ins (open policy + architecture follow-ups), then cut v1 into vertical build slices via superpowers:writing-plans. Writes the build plan; writes no app code.
argument-hint: version to plan the build for, e.g. "v1" (defaults to v1)
---

Invoke the `farm-requirements` skill and run **Phase 5a: Build Planning**.

**Scope is v1 only** (per the skill's prime directive) — plan only the v1 screens and
services finalized in `DESIGN-v1.md`; v2/later items stay as notes.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 4 gate** ✅
   (design finalized). If it is open, STOP and tell the user to run `/design-finalize`.
2. Determine the target version from `$ARGUMENTS` (default `v1`).
3. Read `docs/requirements/DESIGN-<version>.md` (esp. **§5 open questions / Build
   follow-ups**), `ARCHITECTURE-<version>.md` (domain model + service layer) and
   `REQUIREMENTS-<version>.md` so the plan is consistent with all three.
4. **Resolve the carry-ins before planning:**
   - **Ask the user the one open policy decision** — the **per-owner edit/delete policy**
     (DESIGN-v1 §5: a family member cannot edit another member's record; admin can edit
     anyone's). Confirm it is acceptable, or capture the variant they want.
   - **Apply the architecture follow-ups** surfaced in Phase 4c as a **dated addendum** to
     `docs/requirements/20-architecture-decisions.md` (do not silently rewrite finalized
     decisions — append, cite §5): new service functions `record_transaction` /
     `record_payment` / `adjust_stock`; `record_sale` extended to create the initial
     `Payment` row; model field additions (`Item.code` required/unique/uppercase/2–8,
     optional `Entity.code`, `Contact.name`/`phone`/`notes`, `Transaction.note`, editable
     `Batch.origin`); "open outsourced batch" = a query, no status field.
5. **Reuse `superpowers:writing-plans`** to cut v1 into **vertical slices** (each slice =
   model + migration + service function + view/template + tests, shippable end-to-end).
   The approved `REQUIREMENTS-/ARCHITECTURE-/DESIGN-<version>.md` docs **are the spec** — do
   not re-brainstorm or write a new spec. **Two constraints on how you use the skill here:**
   - **Slice-level structure only** — this plan defines each slice's scope, files touched,
     test targets, and the `REQ-NNN`/service it serves. It does **not** contain per-step
     TDD code (that is worked out inside `/build-next` per slice), so the command writes no
     app code.
   - **Do not take writing-plans' execution handoff.** The execution method for this project
     is the `/build-next` command; stop after the plan is confirmed — do not let the skill
     launch implementation (that would skip the `/build-setup` consent + scaffold gate).

   Suggested slice order (confirm with the user): project skeleton → auth/roles/users →
   domain models + admin → `record_harvest` → `run_production` → `procure` → `record_sale` +
   `record_payment` → `record_transaction` → inventory/shortfall → reports/print → `/m/`
   subset. Keep YAGNI; v2 seams stay out.
6. Write the plan to **`docs/requirements/40-build-plan.md`** (slice list, order,
   per-slice scope + the `REQ-NNN`/service each serves, and the resolved policy). Follow the
   repo's numbering — do **not** use `superpowers`' default `docs/superpowers/specs/` path.
7. When the user confirms the build plan is settled:
   - Log a **Phase 5a sub-gate** ("build plan confirmed") ✅ in `STATUS.md` with today's date.
   - Add a **`## Slice progress`** table to `STATUS.md` with **one ⬜ row per slice** from
     `40-build-plan.md` (slice name · status · date · note) — this is the log `/build-next`
     flips to ✅ and `/build-finalize` checks.
   - Tell the user to run `/build-setup`.

Do not scaffold the project, create a git repo, install anything, or write application code
in this command — that begins in `/build-setup`.
