---
description: Phase 1 — gather requirements by walking the farm end-to-end, one question at a time (drives superpowers:brainstorming). Requires the Phase 0 gate.
argument-hint: (optional) an area to focus on, e.g. "irrigation", "livestock", "labour"
---

Invoke the `farm-requirements` skill and run **Phase 1: Requirement Gathering**.

1. **Gate check.** Read `docs/requirements/STATUS.md`. If the **Phase 0 gate**
   ("big picture complete") is NOT ✅, STOP and tell the user to finish `/req-init`
   first. Name the open gate. Do not proceed.
2. Read `docs/requirements/00-big-picture.md` so questions build on what they already said.
3. Announce "Using superpowers:brainstorming for requirement gathering" and invoke
   **`superpowers:brainstorming`** as the questioning engine. Scope it strictly to
   **requirements only** — if brainstorming tries to push into design, architecture,
   tech choices, or writing a plan, stop it there: Phase 1 is only about *what the
   farm needs*, not *how to build it*.
4. Ask **one question at a time**, walking the farm workflow end-to-end (e.g. land/plots →
   crops & seasons → inputs/inventory → irrigation → labour & tasks → livestock →
   harvest → sales/finance → records/compliance). If `$ARGUMENTS` names an area, start there.
5. After each answer, write a structured requirement to
   `docs/requirements/10-requirements-register.md`: assign the next `REQ-NNN`, fill
   area, set version = `unscoped` (versioning happens in Phase 2), status = `draft`,
   and set `source:` to the user's answer. Keep the user's intent faithfully.
6. Capture non-functional answers (connectivity, device, language, users/roles,
   hardware, existing records, budget) as requirements too, tagged area = NFR.
7. This is resumable — the user can stop and rerun `/req-ask` any time. When they feel
   every activity is covered, tell them to run `/req-review`. Do **not** set the Phase 1
   gate here; that is confirmed during review/finalize.

Never advance to architecture, design, or stack selection in this command.
