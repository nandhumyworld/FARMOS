---
description: Show where farmOS requirements stand — current phase, version in scope, open gates, and requirement counts. Read-only.
---

Invoke the `farm-requirements` skill in read-only mode.

1. Read `docs/requirements/STATUS.md`, `00-big-picture.md`, and `10-requirements-register.md`.
2. Report concisely:
   - Current **phase** and **version** in scope.
   - Which **gates** are ✅ and which are ⬜ open (and what to run to close the next one).
   - **Counts** from the register: total requirements, and how many are
     draft / confirmed / deferred, and per target version (v1 / v2 / later / unscoped).
   - Any obvious next action (e.g. "run `/req-ask` to continue gathering").
3. Do not modify any file. This command only reports.
