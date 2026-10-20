---
description: Phase 3c — design the farmOS v1 system architecture (components, layers, API seams, auth, deployment on Coolify). Produces an Excalidraw architecture diagram.
argument-hint: (optional) an architecture concern to start from
---

Invoke the `farm-requirements` skill and run **Phase 3c: System Architecture**.

**Scope is v1 only** — but note (do not build) the seams the deferred REQ-028 integrations
(Telegram/n8n, website + CMS, external API) will later plug into, so v1 doesn't paint them out.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 3b sub-gate**
   ("domain model confirmed") ✅. If open, STOP and tell the user to run `/arch-model`.
2. Read `docs/requirements/REQUIREMENTS-v1.md` and `20-architecture-decisions.md`
   (`## Stack` + `## Domain model`) so the architecture is consistent with both.
3. **Reuse `superpowers:writing-plans`** (or the **Plan** agent) to design:
   - Component/layer breakdown (web UI, app/service layer, data layer) and how it maps to the stack.
   - **API design** — internal API shape; keep it clean enough that the future external/customizable
     API (REQ-028) is an extension, not a rewrite.
   - **Auth & roles** (REQ-021: admin vs owner/family; employees don't log in).
   - **Deployment topology on Coolify** (REQ-026): app container(s) + bundled PostgreSQL, domain,
     backups, environment/secrets — v1, no paid services.
   - **Audit logging** approach (REQ-027) and **responsive-web / Capacitor-APK** decision (REQ-022).
4. **Diagram (Excalidraw).** Load tools: `ToolSearch` with
   `select:mcp__claude_ai_Excalidraw__read_me,mcp__claude_ai_Excalidraw__create_view`,
   call `read_me`, then draw a **system/context architecture diagram** (components, data store,
   deployment, and the dashed future-integration seams).
5. Record the architecture in `docs/requirements/20-architecture-decisions.md` under
   `## System architecture` (with the diagram checkpoint id). Then log a **Phase 3c sub-gate**
   ("architecture confirmed") ✅ in `STATUS.md` with today's date and tell them to run `/arch-finalize`.

Do not scaffold the project or write code. Do not finalize — that is `/arch-finalize`.
