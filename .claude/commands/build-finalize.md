---
description: Phase 5 output — verify every v1 build slice is complete and green, consolidate the build into BUILD-v1.md, confirm the Phase 5 gate, and advance to Phase 6 (Testing + UAT).
argument-hint: version to finalize, e.g. "v1" (defaults to v1)
---

Invoke the `farm-requirements` skill and run **Phase 5 finalization**.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require **every slice** in
   `docs/requirements/40-build-plan.md` marked ✅ in the slice-progress log (i.e. the
   **Phase 5b sub-gate** closed and all slices built). If any slice is open, STOP and name
   which one `/build-next` should build next.
2. Determine the target version from `$ARGUMENTS` (default `v1`).
3. Run the **full test suite** once more and confirm it is green. Report the result with
   output. If anything fails or is skipped, STOP and say so — do not finalize a red build.
4. Generate **`docs/requirements/BUILD-<version>.md`** containing:
   - **What shipped** — the v1 screens, services, and models actually built, slice by slice.
   - **How it runs** — local run + the Coolify/Docker deploy shape (not a release; that is
     Phase 7).
   - **Test summary** — what is covered and the suite's status.
   - **Deviations from spec** — anything built differently from
     `REQUIREMENTS-/ARCHITECTURE-/DESIGN-<version>.md`, with the reason (surface, don't hide).
   - **Known gaps / carried to Phase 6 (Testing + UAT)** and v2 seams left out.
   - **Build → requirement/design traceability** (slice → `REQ-NNN` / screen / service).
5. Update `docs/requirements/STATUS.md`: mark the **Phase 5 gate** ✅ (build confirmed) with
   today's date, record `BUILD-<version>.md` under "Finalized versions", and set the current
   phase to **6 — Testing (+ UAT)**.
6. If git is in use, commit the finalization (docs + any final touches) with a message
   ending in the session's required attribution line.
7. Tell the user Phase 5 is done and that the Phase 6 (Testing + UAT) commands will be added
   when they confirm they are ready to start it.

Do not begin Phase 6 testing/UAT work or deployment in this command.
