---
description: Phase 5b — scaffold the farmOS v1 project skeleton (Django + HTMX/Alpine/Tailwind, Dockerfile for Coolify) after explicit consent for git and installs. First command that writes files to the repo root.
argument-hint: version to scaffold, e.g. "v1" (defaults to v1)
---

Invoke the `farm-requirements` skill and run **Phase 5b: Project Setup / Scaffold**.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 5a sub-gate**
   ("build plan confirmed") ✅. If it is open, STOP and tell the user to run `/build-plan`.
2. Determine the target version from `$ARGUMENTS` (default `v1`). Read
   `docs/requirements/40-build-plan.md` and `ARCHITECTURE-<version>.md` (SD-1/SD-2/SD-5:
   **Django 5.2 LTS + HTMX + Alpine + Tailwind**, session auth + custom user,
   django-auditlog, **Dockerfile + bundled PostgreSQL on Coolify**, no background jobs).
3. **Consent gate — prime directive 6 still binds.** `git init`, installs, and commits are
   NOT covered by "let's build". In **one batched question**, get explicit yes/no for:
   - initialise a **git repo** here (the first commit now **and** a commit after each slice
     in `/build-next` / at `/build-finalize`),
   - install **Python/Django deps** (virtualenv + pip/requirements),
   - install the **Tailwind standalone CLI binary** (SA-5: no Node runtime — do not install
     Node unless the user wants it),
   - the **dev/test database** to use (production is Coolify-bundled PostgreSQL, SD-5): local
     Postgres via Docker, a native Postgres install, or SQLite for dev/test only. **Note the
     UI-first plan:** Stage A (Slices A1–A4) has **no domain models** — only the empty custom
     user model is created here — so a zero-config **SQLite** dev DB is enough to start; the
     real Postgres dev/test DB and all domain migrations are deferred to **Stage B (B0/B1)**.
     Still settle the intended dev DB here so it is on record.
   Also **check availability first** on this Windows box (Python, pip, Node, Docker) and
   report what is present. Do only what the user approves; if they decline an item, note it
   and scaffold the files without running that install.
4. **Handle the stray `test` file.** Do not `git add` it blindly — if git is approved,
   exclude it via `.gitignore` or ask the user what to do with it. Never silently track it.
5. Scaffold the **skeleton only** (no feature logic — that is `/build-next`): Django project
   + core app layout, settings split, `requirements.txt`/`pyproject`, Tailwind config +
   base template (app shell per `DESIGN-v1.md` DS-5/DS-6), `Dockerfile` + `.dockerignore`
   for Coolify, `.gitignore`, and a README noting how to run it. Keep it to what the plan's
   first slice needs; honour the design system tokens (blue-600 primary, etc.). **For the
   UI-first plan, the only model is an empty custom user** (`User(AbstractUser)` +
   `AUTH_USER_MODEL`); run its **initial migration** so the prototype's `runserver` is
   warning-free. Create **NO domain models** here — those are Stage B. A plain SQLite dev DB
   serves the static prototype.
6. **Smoke check — 5b only closes on a working dev environment.** Run `python manage.py
   check`, **`migrate`** (the custom-user initial migration), and the test runner against the
   empty suite; all must pass green (Stage-A render tests and Stage-B TDD in `/build-next`
   depend on it). If the Python deps were declined or the environment can't
   run, **leave the 5b sub-gate ⬜**, record why in `STATUS.md`, and tell the user what to
   install/approve before the build can proceed — do not mark 5b done.
7. If git was approved, make the **initial commit** of the skeleton. End the commit message
   with the attribution line the session requires.
8. Only if step 6 is green: log a **Phase 5b sub-gate** ("project scaffolded") ✅ in
   `STATUS.md` with today's date (note what was/wasn't installed), and tell the user to run
   `/build-next` to build the first slice.

Do not implement feature slices (screens, services, forms, reports) in this command — that
is `/build-next`, one slice at a time (Stage A UI slices, then Stage B backend slices).
