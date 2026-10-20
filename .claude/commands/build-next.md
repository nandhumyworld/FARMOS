---
description: Phase 5c — build the next (or a named) slice from 40-build-plan.md end-to-end (Stage A UI slice, or Stage B backend slice under TDD), then record slice progress in STATUS.md. Repeat until all slices are done.
argument-hint: (optional) slice name/number from the build plan, e.g. "A2" or "B6"; defaults to the next unbuilt slice
---

Invoke the `farm-requirements` skill and run **Phase 5c: Build a Slice**.

The plan is **UI-first** (see `40-build-plan.md` "Build strategy"): **Stage A** slices
(A1–A4) are **static UI** — templates + Tailwind + HTMX/Alpine fed by **mock context, no DB /
no models / no services**; **Stage B** slices (B0–B10) wire the approved templates to real
models + services under TDD. Detect which stage the chosen slice is in and follow the
matching step 4.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 5b sub-gate**
   ("project scaffolded") ✅. If it is open, STOP and tell the user to run `/build-setup`.
   For the **first Stage-B slice (B0)**, also require the **▲ UI review gate** to be marked
   passed in `STATUS.md` (the user approved the prototype) — if not, STOP and ask them to
   review the Stage-A prototype and confirm before backend work begins.
2. Read `docs/requirements/40-build-plan.md` and the **slice progress** log in `STATUS.md`.
   Pick the slice: the one named in `$ARGUMENTS`, else the next unbuilt slice in plan order.
   Announce which slice, its **stage**, and its scope (the `REQ-NNN` / screen / service).
3. Re-read the relevant parts of `DESIGN-v1.md` (the slice's screens/forms/fields/validation/
   states) and, for Stage B, `ARCHITECTURE-<version>.md` (the slice's models + service
   function + atomic/audited contract). Honour the architecture follow-ups in
   `20-architecture-decisions.md` and the edit/delete policy (SA-12).
4. Build the slice:
   - **Stage A (UI slice):** build the **static templates + components** per the design
     system, driven by **hardcoded mock context** that uses the **field/variable names from
     the `DESIGN-v1` DD specs** (so Stage B is a swap). **No models, migrations, or
     services.** Verify with a **page-render/smoke test** (each new URL returns 200 and
     renders) and a **visual check** on laptop + phone widths. Keep interactions (tally,
     price snapshot, Paid/Partial/Credit) working against stub endpoints/Alpine. Finding a
     missing/awkward field or flow is the **point** of this stage — **record it as a
     UI-review finding** (a running list in `STATUS.md` under the UI-review gate) and
     **continue**; do not stop, and do not edit the finalized docs mid-slice.
   - **Stage B (backend slice):** **reuse `superpowers:test-driven-development`** —
     red→green→refactor: write the failing behavioural test(s) first (service-layer
     behaviour, negative-stock-warns-not-blocks, payment ≤ outstanding, batch-number
     uniqueness, atomic correction/auditlog), then the model/migration + service, then wire
     the **existing** template to real context. Service layer is the only writer (SA-1);
     views stay thin.
5. Run the test suite; report pass/fail honestly with output. Do not mark a slice done if
   tests fail or are skipped — say so and stop.
6. If git is in use, commit the slice with a descriptive message ending in the session's
   required attribution line. Do not push unless the user asks.
7. Update the **slice progress** log in `STATUS.md` (slice ✅ with date + what landed). If the
   slice just finished is **A4** (last Stage-A slice), tell the user to **walk the whole
   prototype** and confirm the **▲ UI review gate**: then turn each UI-review finding into a
   **dated addendum** — UX/flow/label changes to `30-design-decisions.md` (+ `DESIGN-v1.md`
   if a finalized statement changes), and **any data-field/structure change to
   `20-architecture-decisions.md`** (so the model is fixed before B1 migrates) — and on their
   confirmation **log the UI-review sub-gate ✅** (gate log + its row in `## Slice progress`).
   B0 refuses until that gate is ✅. Otherwise tell them what was built, how it was verified,
   and to run `/build-next` for the next slice — or `/build-finalize` once every slice is ✅.

Build **one slice per invocation**. Do not scope-creep into other slices or v2 seams. In
**Stage A** do not create models/migrations/services, and record gaps as UI-review findings
rather than stopping. In **Stage B** do not rebuild approved templates from scratch (wire
them), and if a real gap in the finalized stack/model/design appears, surface it and stop.
