---
description: Phase 3b — design the farmOS v1 data/domain model (entities, ledgers, inventory, batches, sales, contacts) and resolve the open modeling decisions. Produces an Excalidraw ER/domain diagram.
argument-hint: (optional) a modeling question to start from
---

Invoke the `farm-requirements` skill and run **Phase 3b: Data / Domain Model**.

**Scope is v1 only.** Model only the v1 in-scope requirements; leave v2/later seams as notes.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 3a sub-gate**
   ("stack confirmed") ✅. If open, STOP and tell the user to run `/arch-stack`.
2. Read `docs/requirements/REQUIREMENTS-v1.md`, the register `10-requirements-register.md`
   (esp. the **Open modeling decisions** OD-1, OD-3, OD-5), and the `## Stack` section of
   `20-architecture-decisions.md` (so the model fits the chosen ORM/DB).
3. **Reuse `superpowers:writing-plans`** (or the **Plan** agent) to design the domain model:
   entities & categories (REQ-001), dual income/expense ledger + rich attribution
   (REQ-002, 005, 017, 031), harvest → inventory → production/recipes → batches
   (REQ-006..010, 034), quick sale + pricing + payments (REQ-011, 013, 032), contacts +
   vendors + purchase history (REQ-014, 033), reporting needs (REQ-016). Call out keys,
   relationships, and where each `REQ-NNN` is satisfied.
4. **Resolve the open decisions** with the user and record the resolution:
   - **OD-1** — one entity table with a `type` field vs. separate tables per category.
   - **OD-3** — inventory deduction timing (v1 quick sale deducts immediately; note the v2 order hook).
   - **OD-5** — batch P&L = direct-tag only for v1 (confirm; defer allocation).
5. **Diagram (Excalidraw).** Load tools: `ToolSearch` with
   `select:mcp__claude_ai_Excalidraw__read_me,mcp__claude_ai_Excalidraw__create_view`,
   call `read_me`, then draw an **ER / domain-model diagram** of the v1 schema.
6. Record the model + resolved ODs in `docs/requirements/20-architecture-decisions.md`
   under `## Domain model` (with the diagram checkpoint id). Then log a **Phase 3b sub-gate**
   ("domain model confirmed") ✅ in `STATUS.md` with today's date and tell them to run `/arch-design`.

Do not write migrations, ORM models, or any code. Do not proceed to system architecture.
