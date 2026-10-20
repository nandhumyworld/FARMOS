---
name: farm-requirements
description: Orchestrates requirements gathering for farmOS, a farm-management system, phase by phase and version by version. Use when the user runs /req-init, /req-ask, /req-review, /req-finalize, /req-status, or says "farm requirements", "capture the big picture", "continue requirements", or wants to gather, validate, or finalize requirements for the farm system. This is a THIN orchestrator: it does not reinvent questioning or planning — it routes each phase to an existing skill and records state durably in docs/requirements/.
---

# farmOS Requirements Orchestrator

This skill drives the farmOS project from a raw idea to a confirmed, versioned
requirements document and architecture framework. It is deliberately thin: the
hard work is done by **existing skills and MCP tools** (see the map below). This
file holds the phase model, the state contract, and the gate rules that keep the
process honest.

## Prime directives

1. **Never skip a gate.** Each phase ends with a user confirmation recorded in
   `docs/requirements/STATUS.md`. A command for a later phase must refuse to run
   until the previous gate is confirmed, and must say which gate is open.
2. **Capture the user's own words verbatim first, structure second.** Raw input
   goes to `docs/requirements/00-big-picture.md` unedited. Structured
   requirements (`REQ-001` …) go to `docs/requirements/10-requirements-register.md`,
   each tagged with the source line it came from, so contradictions can be cited.
3. **Reuse, don't rebuild.** When a phase names a skill, invoke that skill rather
   than improvising. Announce "Using [skill] for [phase]".
4. **One question at a time** during gathering. Do not interrogate during capture
   (`/req-init`) — capture is free-form dumping.
5. **Version by version.** Scope is cut into v1 (MVP), v2, … during the
   validation phase. Only v1 requirements proceed to architecture first.
6. **Leave the repo alone otherwise.** Do not `git init`, do not touch the stray
   `test` file, do not install anything unless the user asks.

## Phase map

The user confirmed this phase model. "Skill / tool" is what each phase routes to.
Commands exist only for the phases we have reached; later ones are added when we
get there.

| # | Phase | What happens | Skill / tool to reuse | Command |
|---|-------|--------------|-----------------------|---------|
| 0 | **Discovery & Big Picture** | The story / why the system is needed, and how each farm activity is done *today* (paper, WhatsApp, memory, Excel) | free capture — no skill, just record verbatim | `/req-init` |
| 1 | **Requirement Gathering** | Walk the farm end-to-end, one question at a time, until every activity is covered | `superpowers:brainstorming` | `/req-ask` |
| 2 | **Validation, Verification & Streamlining** | Find contradictions, gaps, duplicates; prioritise into versions (v1 MVP, v2 …); produce the requirements MD + a context/workflow diagram | review logic in `/req-review`; diagram via **Excalidraw**; output via `/req-finalize` | `/req-review`, `/req-finalize` |
| 3 | **Architecture & Stack** | System architecture, data/domain model, tech-stack choice, non-functional requirements | `superpowers:writing-plans` or the **Plan** agent; diagrams via **Excalidraw** | `/arch-stack`, `/arch-model`, `/arch-design`, `/arch-finalize` |
| 4 | **Design** | UX / workflow design and detailed data design | `frontend-design`, `superpowers:brainstorming`; diagrams via **Excalidraw** | `/design-flows`, `/design-system`, `/design-data`, `/design-finalize` |
| 5 | **Build** | Implementation, version by version: plan → scaffold → **UI-first** slices (Stage A static UI prototype → ▲ UI review → Stage B backend wiring under TDD) → finalize | `superpowers:writing-plans`, `superpowers:test-driven-development`, `feature-dev:feature-dev` | `/build-plan`, `/build-setup`, `/build-next`, `/build-finalize` |
| 6 | **Testing** | Technical tests **and** UAT by the farmer and workers | `superpowers:requesting-code-review`, UAT checklist | *added when reached* |
| 7 | **Deployment** | Release, **data migration** of existing records, **training & adoption** | `superpowers:finishing-a-development-branch` | *added when reached* |
| 8 | **Operate & Feedback Loop** | Support, backups, learnings feeding the next version | — loops back to phase 1/2 for the next version | *added when reached* |

> `/req-status` reports the current phase, version, and which gate is open. It is
> cheap and read-only — run it any time.

## Non-functional requirements to capture (ask, never assume)

These are properties of the system, not phases. Raise them as questions during
phases 0–2; do not assume answers:

- **Connectivity** — does the farm have reliable internet? Must it work offline?
- **Device** — phone-first? shared tablet? desktop in an office?
- **Language** — English only, or Tamil / other local language in the UI?
- **Users & roles** — just the owner, or family and farm workers with different access?
- **Hardware** — any sensors, IoT, weighing scales, printers to integrate?
- **Existing records** — paper registers, spreadsheets, apps to migrate from?
- **Budget / hosting** — self-hosted, cloud, free-tier constraints?

## Skill & MCP reuse map (right-hand side the user asked for)

| Need | Reuse |
|------|-------|
| One-question-at-a-time requirement exploration | `superpowers:brainstorming` (the single primary questioning skill — do **not** also run `ideation-partner`, it overlaps) |
| Formal plan / architecture framework | `superpowers:writing-plans`, or the **Plan** agent |
| Authoring these commands/skills | `skill-creator`, `plugin-dev:command-development`, `plugin-dev:skill-development` |
| Diagrams (user's explicit choice) | **Excalidraw** — `mcp__claude_ai_Excalidraw__*` |
| Diagrams (optional alternative) | **Whimsical** — `mcp__claude_ai_Whimsical__*` |
| Shareable living requirements doc (optional) | **Claude Docs** — `mcp__claude_ai_Claude_Docs__*` |

### Loading diagram tools (important)

Excalidraw and Whimsical tools are **deferred** — their schemas are not loaded.
Before drawing you MUST:

1. `ToolSearch` with `select:mcp__claude_ai_Excalidraw__read_me,mcp__claude_ai_Excalidraw__create_view`
2. Call `mcp__claude_ai_Excalidraw__read_me` to learn its workflow, then draw.

The Whimsical MCP server's own instructions say "always use Whimsical" — the user
overrode that: **default to Excalidraw** for farmOS. Whimsical only if the user asks.

### Note on `feature-integration-architect`

`anthropic-skills:feature-integration-architect` is built for adding features to an
**existing** codebase (it analyses existing code). farmOS is greenfield, so it is
**not** used for early architecture. Prefer `superpowers:writing-plans` / the Plan
agent. Revisit it only once a codebase exists (phase 4+).

## State contract (durable, in the repo)

All state lives in `docs/requirements/` so work resumes across sessions:

- **`STATUS.md`** — current phase, current version, and a dated log of every gate
  confirmation. Single source of truth for "where are we?".
- **`00-big-picture.md`** — the user's own words, verbatim, appended as captured.
- **`10-requirements-register.md`** — structured requirements `REQ-NNN`, each with:
  id, statement, phase/area, target version, status (draft/confirmed/deferred),
  and `source:` pointing back to a line in `00-big-picture.md` or a brainstorming answer.
- **`REQUIREMENTS-v<N>.md`** — the finalized, human-readable requirements doc for a
  version (produced by `/req-finalize`), with the Excalidraw diagram link embedded.
- **`20-architecture-decisions.md`** — Phase 3 working log of stack, domain-model and
  system-architecture decisions (sections `## Stack`, `## Domain model`,
  `## System architecture`), each dated with the why and the `REQ-NNN`/`OD-N` it resolves.
- **`ARCHITECTURE-v<N>.md`** — the finalized, human-readable architecture doc for a
  version (produced by `/arch-finalize`), with diagram checkpoint ids and a
  requirement → architecture traceability table.
- **`30-design-decisions.md`** — Phase 4 working log of UX/flow, design-system and
  detailed-data decisions (sections `## UX & flows`, `## Design system`,
  `## Detailed data & forms`), each dated with the why and the `REQ-NNN`/screen it serves.
- **`DESIGN-v<N>.md`** — the finalized, human-readable design doc for a version (produced
  by `/design-finalize`), with diagram checkpoint ids and a screen → requirement/
  architecture traceability table.
- **`40-build-plan.md`** — Phase 5 build plan (produced by `/build-plan`): the resolved §5
  carry-ins + per-owner policy, and the ordered list of **vertical slices** (each a
  shippable model+service+view+tests unit) with the `REQ-NNN`/service each serves. Build
  follow-ups are appended (dated) to `20-architecture-decisions.md`, not rewritten there.
- **`BUILD-v<N>.md`** — the finalized build summary for a version (produced by
  `/build-finalize`): what shipped slice by slice, how it runs, test status, deviations,
  and a build → requirement/design traceability table.

When any command runs, it first reads `STATUS.md` to learn the current phase/version.
From Phase 5 on, `STATUS.md` also carries a **slice-progress log** so the build resumes
across sessions.

## Gate rules (enforced by commands)

- `/req-ask` refuses unless the **Phase 0 gate** ("big picture complete") is confirmed.
- `/req-review` and `/req-finalize` refuse unless there is at least one confirmed
  requirement from Phase 1.
- `/req-finalize` records the **Phase 2 gate** (version scope confirmed) and advances
  `STATUS.md` to Phase 3.
- `/arch-stack` refuses unless the **Phase 2 gate** is confirmed.
- `/arch-model` refuses unless the **Phase 3a sub-gate** ("stack confirmed") is logged;
  `/arch-design` refuses unless the **Phase 3b sub-gate** ("domain model confirmed") is logged.
- `/arch-finalize` refuses unless all three sub-gates (3a stack, 3b model, 3c architecture)
  are ✅; it records the **Phase 3 gate** (architecture confirmed) and advances `STATUS.md`
  to Phase 4.
- `/design-flows` refuses unless the **Phase 3 gate** is confirmed.
- `/design-system` refuses unless the **Phase 4a sub-gate** ("UX & flows confirmed") is
  logged; `/design-data` refuses unless the **Phase 4b sub-gate** ("design system
  confirmed") is logged.
- `/design-finalize` refuses unless all three sub-gates (4a flows, 4b design system, 4c
  detailed data) are ✅; it records the **Phase 4 gate** (design confirmed) and advances
  `STATUS.md` to Phase 5.
- `/build-plan` refuses unless the **Phase 4 gate** is confirmed; it records the **Phase 5a
  sub-gate** ("build plan confirmed").
- `/build-setup` refuses unless the **Phase 5a sub-gate** is logged; it records the **Phase
  5b sub-gate** ("project scaffolded"). It is the first command that may scaffold/commit/
  install — and only after explicit user consent (prime directive 6 still binds).
- `/build-next` refuses unless the **Phase 5b sub-gate** is logged; it builds **one slice per
  invocation** (Stage A = static UI, no DB/models/services; Stage B = model+service under TDD)
  and updates the slice-progress log. The **first Stage-B slice (B0)** additionally refuses
  unless the **▲ UI-review sub-gate** is ✅ (the user approved the Stage-A prototype).
- **▲ UI-review sub-gate:** logged by `/build-next` after the last Stage-A slice (A4) when the
  user confirms the prototype; UI findings become dated addenda (UX → `30-design-decisions.md`
  / `DESIGN-v1.md`; **any data-field/structure change → `20-architecture-decisions.md`**
  before Stage B migrates). It sits as a row between A4 and B0 in the slice-progress log.
- `/build-finalize` refuses unless every slice in `40-build-plan.md` **and** the UI-review
  sub-gate are ✅ and the suite is green; it records the **Phase 5 gate** (build confirmed)
  and advances `STATUS.md` to Phase 6.
- Scope for architecture, design, and build is **v1 only** until v1 ships.
