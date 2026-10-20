# farmOS — Requirements Status

> Single source of truth for "where are we?". Every command reads this first.
> Updated only when a gate is confirmed by the user.

- **Current phase:** 5 — Build (**UI-first**; skeleton scaffolded 2026-10-20 + pushed to `github.com/nandhumyworld/FARMOS`; cloud Postgres connected + migrated; **next action: run `/build-next`** → Stage A Slice A1 (design system & app shell).)
- **Current version in scope:** v1 (MVP) — finalized in `REQUIREMENTS-v1.md`
- **Project started:** 2026-10-14

## Gate log

| Date | Gate | Confirmed? | Note |
|------|------|-----------|------|
| 2026-10-14 | Project initialised | ✅ | Orchestrator skill + commands created |
| 2026-10-14 | Phase 0 gate: big picture complete | ✅ | 3 verbatim captures in `00-big-picture.md`; user confirmed "complete" |
| 2026-10-14 | Phase 1 gate: all activities gathered | ✅ | 29 reqs gathered; `/req-review` resolved 18 findings, no re-gathering needed; checklist complete |
| 2026-10-14 | Phase 2 gate: version scope confirmed | ✅ | v1 scoped & finalized → `REQUIREMENTS-v1.md` + Excalidraw workflow diagram (checkpoint `c7c7a71619bc4e1783`) |
| 2026-10-14 | Phase 3a sub-gate: stack confirmed | ✅ | 7 decisions SD-1..SD-7 in `20-architecture-decisions.md` (Django 5.2 LTS + HTMX/Alpine, Capacitor `/m/` subset, Django ORM/session-auth/django-auditlog, Dockerfile on Coolify, no bg jobs, browser-print export); confirmed by advancing to `/arch-model` |
| 2026-10-14 | Phase 3b sub-gate: domain model confirmed | ✅ | 17 tables in `20-architecture-decisions.md` `## Domain model`; OD-1 (one Entity table), OD-3 (deduct-on-save + StockMovement ledger), OD-5 (direct-tag + descendant rollup) resolved; income=accrual; ER diagram (Excalidraw `7bfb393e3cc44189b2` + SVG file); confirmed by advancing to `/arch-design` |
| 2026-10-14 | Phase 3c sub-gate: architecture confirmed | ✅ | SA-1..SA-7 in `20-architecture-decisions.md` `## System architecture`; layered + service-layer seam, session auth/roles (family full access), edit-in-place + negative-stock-allowed, Coolify topology, audit; arch diagram (Excalidraw `fa240ccb76f143aa8b` + SVG/PNG); confirmed by advancing to `/arch-finalize` |
| 2026-10-14 | Phase 3 gate: architecture finalized | ✅ | All 3 sub-gates ✅; consolidated into `ARCHITECTURE-v1.md` (stack SD-1..7, domain model 18 tables + REQ-036, system arch SA-1..7, NFRs, REQ→arch traceability); advances to Phase 4 |
| 2026-10-16 | Phase 4a sub-gate: UX & flows confirmed | ✅ | UX-1..UX-11 in `30-design-decisions.md` `## UX & flows`: action-first hub + 12 screens; `/m/` capture+customer subset; global edit-on-detail + confirm/Add-another; flows for harvest (batch no. `<item-code><YYMMDD>`), production (builder+tally), procurement (new-batch-default mergeable), quick sale (snapshot + Paid/Partial/Credit), expense/income (all attribution visible), contacts (per-sale payment), reports (one screen + browser print), shortfall (inline red badges). Diagrams: nav/flow `e456b9e36d7b4b7d8a` + wireframes `ccf74978f59b4220ae`. Follow-ups flagged: `record_transaction` service, Entity/Item `code` field (touches Phase 3 model). Confirmed by user |
| 2026-10-17 | Phase 4b sub-gate: design system confirmed | ✅ | DS-1..DS-6 in `30-design-decisions.md` `## Design system`: Plain &amp; System (low-build) — Tailwind defaults + system fonts, utility-first, mobile/Capacitor-ready; blue-600 primary (interactive-only) + money green/red + amber/neutral tokens, usage-rule + not-color-alone; system sans + tabular numerals; Indian grouping + accounting parentheses (unsigned positives); soft-standard components (rounded-md, 44px, Lucide, tables→cards, worded light-tint badges, KPI tiles); mobile-first + hub-and-back phone nav + print black-on-white. Specimen `farmOS-v1-design-system.svg`. Confirmed by user |
| 2026-10-17 | Phase 4c sub-gate: detailed data confirmed | ✅ | DD-0..DD-9 in `30-design-decisions.md` `## Detailed data & forms`: global conventions (Decimal(12,2)/(12,3), positive inputs, units display-only, dates default-today/no-future, negative-stock warn, double-submit guard, created_by/admin edit gating, atomic correction + PROTECT); per-form field/validation/service specs for Harvest/Production/Procurement/Quick-sale/Expense-Income/Collect-payment/Contact/Reports/Admin+Adjust-stock. User decisions: contact required on every sale + inline add; admin Adjust-stock action; output-origin default-inherited-editable; Item.code required / Entity.code optional. Architecture follow-ups for Build: new services `record_transaction`/`record_payment`/`adjust_stock`, `record_sale` initial-Payment, model field additions. Confirmed by user |
| 2026-10-17 | Phase 4 gate: design finalized | ✅ | All 3 sub-gates ✅ (4a UX-1..11, 4b DS-1..6, 4c DD-0..9); consolidated into `DESIGN-v1.md` (UX & flows, design system, detailed data/forms, screen→REQ/arch traceability, Build follow-ups); diagrams nav `e456b9e36d7b4b7d8a` + wireframes `ccf74978f59b4220ae` + specimen svg. Advances to Phase 5 — Build |
| 2026-10-19 | Phase 5a sub-gate: build plan confirmed | ✅ | **UI-first** build plan → `40-build-plan.md`: Stage A static-UI prototype (A1–A4) → ▲ UI-review gate → Stage B backend wiring (B0–B10, TDD). Open policy resolved → **SA-12 shared family edit**; architecture follow-ups SA-8..SA-12 appended (dated) to `20-architecture-decisions.md`. Confirmed by user |
| 2026-10-20 | Phase 5b sub-gate: project scaffolded | ✅ | Skeleton scaffolded + smoke-green (`check` + `migrate` + 2 tests pass). Stack live: Django 5.2.18, HTMX/Alpine (CDN), **Tailwind v4.3.3** standalone CLI (no Node), WhiteNoise, gunicorn, django-auditlog, psycopg3 — venv on `py -3.13`. Empty custom `core.User` + initial migration. Config split (`config.settings.base/dev/prod`), `Dockerfile` + `.dockerignore` for Coolify, `/healthz`, base template + placeholder home. **DB:** `DATABASE_URL`-driven (Django migrations, **no Prisma**). **2026-10-20: cloud Postgres connected + initial migration applied** — PostgreSQL 17.6, db `farmos_test`, role `authenticator` (DDL ok; **no CREATEDB**, so the **test suite runs on in-memory SQLite** while dev/prod use cloud Postgres — revisit at B0 if same-engine tests wanted). Git: pushed to `github.com/nandhumyworld/FARMOS`. Next: `/build-next` → Slice A1 |

## Finalized versions

| Version | Document | Finalized | Notes |
|---------|----------|-----------|-------|
| v1 (MVP) | `REQUIREMENTS-v1.md` | 2026-10-14 | 27 in-scope reqs (+REQ-036 added in Phase 3 = 28); formal orders + multi-dim reports deferred to v2; integrations/tasks/multi-lang → later |
| v1 (MVP) | `ARCHITECTURE-v1.md` | 2026-10-14 | Django + HTMX on Coolify; 18-table domain model; service-layer architecture; diagrams: ER (`farmOS-v1-domain-ER.svg/.png`), system arch (`fa240ccb76f143aa8b` + svg/png) |
| v1 (MVP) | `DESIGN-v1.md` | 2026-10-17 | Plain & System Tailwind design; 12 screens + `/m/` subset; UX-1..11 / DS-1..6 / DD-0..9; screen→REQ/arch traceability; diagrams: nav (`e456b9e36d7b4b7d8a` + `farmOS-v1-ux-navigation.svg`), wireframes (`ccf74978f59b4220ae` + `farmOS-v1-ux-wireframes.svg`), specimen (`farmOS-v1-design-system.svg`). Build follow-ups: new services `record_transaction`/`record_payment`/`adjust_stock`, `record_sale` initial-Payment, model field additions |

## Slice progress (Phase 5 — Build)

> Set up at the Phase 5a gate (2026-10-19). `/build-next` flips a row to ✅ as each slice
> lands; `/build-finalize` requires every row (incl. the ▲ UI-review gate) ✅ + green suite.
> Plan: `40-build-plan.md`. Skeleton (project + empty custom user) is delivered by
> `/build-setup`, not a slice row.

| Slice | Stage | Status | Date | Note |
|-------|-------|--------|------|------|
| A1 — Design system + app shell | A (static UI) | ⬜ | | login + style-guide pages, components, print CSS |
| A2 — Capture screens | A (static UI) | ⬜ | | Quick Sale, Expense/Income, Harvest, Production, Procurement (mock) |
| A3 — Browse screens | A (static UI) | ⬜ | | Dashboard, Inventory+shortfall, Batches, Entities, Contacts, Reports (mock) |
| A4 — `/m/` family subset | A (static UI) | ⬜ | | Sell, Expense/Income, Add Contact, Collect Payment, Today (mock) |
| **▲ UI-review gate** | gate | ⬜ | | user walks prototype; findings → dated addenda; **B0 refuses until ✅** |
| B0 — Backend foundation | B (TDD) | ⬜ | | groups/auth behind A1 login, Postgres switch, auditlog |
| B1 — Lookups, profile & catalog (admin) | B (TDD) | ⬜ | | FarmProfile, Item(`code`), Contact, Recipe; archive/PROTECT |
| B2 — Entities, ledger & `record_transaction` | B (TDD) | ⬜ | | Transaction/StockMovement/Batch models; Expense/Income + Entities wired |
| B3 — Harvest & `record_harvest` | B (TDD) | ⬜ | | auto batch no., in-house batch + movement |
| B4 — Production & `run_production` | B (TDD) | ⬜ | | builder + real tally, editable origin |
| B5 — Procurement & `procure` | B (TDD) | ⬜ | | outsourced batch, vendor expense |
| B6 — Quick sale, payment & `record_payment` | B (TDD) | ⬜ | | `record_sale` + initial Payment; collect payment |
| B7 — Inventory, shortfall, batch P&L & `adjust_stock` | B (TDD) | ⬜ | | stock = Σ movements, badges, roll-up, admin adjust |
| B8 — Dashboard & Contacts (real data) | B (TDD) | ⬜ | | P&L snapshot, outstanding computed |
| B9 — Reports & print (real data) | B (TDD) | ⬜ | | period/scope, print CSS, order confirmation |
| B10 — `/m/` wiring | B (TDD) | ⬜ | | five flows wired to the same services |

## Phase model

0 Discovery · 1 Gathering · 2 Validation/Streamlining · 3 Architecture/Stack ·
4 Design · 5 Build · 6 Testing (+UAT) · 7 Deployment (+migration/training) ·
8 Operate & Feedback → loops to next version.

See `.claude/skills/farm-requirements/SKILL.md` for the full map.
