---
description: Phase 2 — validate & verify the gathered requirements: find contradictions, gaps, duplicates, and prompt version scoping. Read-mostly.
argument-hint: (optional) an area to focus the review on
---

Invoke the `farm-requirements` skill and run **Phase 2: Validation & Verification**.

1. **Gate check.** Read `docs/requirements/STATUS.md` and `10-requirements-register.md`.
   If there are no requirements beyond the placeholder, STOP and tell the user to run
   `/req-ask` first.
2. Read `00-big-picture.md` and `10-requirements-register.md` in full.
3. Analyse and report (do not silently edit requirements) each of:
   - **Contradictions** — requirements that conflict. Cite both `REQ-NNN`s and quote
     the `source:` lines so the user sees where each came from.
   - **Gaps** — farm activities mentioned in the big picture but with no requirement,
     and missing non-functional answers (connectivity, device, language, users/roles,
     hardware, existing records, budget).
   - **Duplicates / overlaps** — requirements that say the same thing; propose a merge.
   - **Ambiguities** — vague requirements that need a sharper statement.
4. Present findings as a numbered list and ask the user to resolve each. Apply agreed
   fixes to `10-requirements-register.md` (merge, split, reword, or mark `deferred`).
5. **Version scoping prompt.** For each confirmed requirement, help the user tag a
   target version: `v1` (MVP — the smallest set that is genuinely useful on the farm),
   `v2`, or `later`. Update the Version column. Encourage a lean v1.
6. When the user is satisfied, tell them to run `/req-finalize` to produce the versioned
   requirements document and diagram. Do not set the Phase 2 gate here — `/req-finalize` does.
