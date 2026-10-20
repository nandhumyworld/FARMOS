---
description: Phase 3a — choose the farmOS v1 tech stack (language, framework, DB, frontend/mobile, hosting), one decision at a time. Records decisions; does not write app code.
argument-hint: (optional) a stack preference to start from, e.g. "FastAPI + HTMX"
---

Invoke the `farm-requirements` skill and run **Phase 3a: Tech-Stack Selection**.

**Scope is v1 only** (per the skill's prime directive) — do not design for v2/later features.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 2 gate** ✅
   (version scope confirmed). If it is open, STOP and tell the user to run `/req-finalize`.
2. Read `docs/requirements/REQUIREMENTS-v1.md` (esp. the NFR section) and the register's
   NFR rows (REQ-021..026, 029, 030) so stack choices are driven by real constraints:
   self-hosted on owner's VPS + **Coolify**, **Coolify-bundled PostgreSQL**, responsive web,
   English, single-farm-per-install, no paid third-party services, no offline.
3. **Reuse `superpowers:brainstorming`** — walk the stack **one decision at a time**
   (backend language/framework, frontend approach, mobile path for REQ-022/Capacitor,
   ORM/DB access, auth, hosting/deploy on Coolify, background jobs if any). For each,
   present 2–3 concrete options with trade-offs and a recommendation; let the user choose.
   Honour the owner's stated lean to **Python + self-hosted** unless they want to revisit it.
4. Record each confirmed choice in **`docs/requirements/20-architecture-decisions.md`**
   under a `## Stack` section as dated decisions (what was chosen + the why + which NFR/REQ
   it satisfies). Create the file if absent.
5. When the user confirms the stack is settled, log a **Phase 3a sub-gate** ("stack confirmed")
   ✅ in `STATUS.md` with today's date, and tell them to run `/arch-model`.

Do not write application code, scaffold a project, or install anything in this command.
Do not proceed to the data model — that is `/arch-model`.
