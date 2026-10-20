---
description: Phase 0 — capture the farmOS big picture (the story + how things are done today), verbatim and free-form. No interrogation.
argument-hint: (optional) paste your initial description, or just run it and talk
---

Invoke the `farm-requirements` skill and run **Phase 0: Discovery & Big Picture**.

This is **free capture**, NOT brainstorming. Rules:

1. Read `docs/requirements/STATUS.md` first to confirm we are at (or returning to) Phase 0.
2. Welcome the user and ask them, in their own words, for:
   - **The story / why** — what problem on the farm this system should solve, and what "good" looks like.
   - **The as-is** — how each farm activity is handled *today* (paper, registers, WhatsApp, memory, Excel, an existing app).
   Encourage a full brain-dump. Do **not** interrogate, do **not** ask one-at-a-time probing questions, do **not** propose solutions or architecture. Only light "anything else on that?" nudges.
3. Append everything the user says **verbatim** to `docs/requirements/00-big-picture.md` under the right heading. Preserve their wording — do not summarise or rewrite.
4. If `$ARGUMENTS` is non-empty, treat it as their first dump and record it immediately.
5. Also lightly check the non-functional prompts from the skill (connectivity, device, language, users/roles, hardware, existing records, budget) — but only to make sure they are *mentioned*, not to design anything.
6. When the user signals they are done, ask explicitly: **"Is the big picture complete enough to move to requirement gathering?"**
   - If **yes**: update `docs/requirements/STATUS.md` — mark the Phase 0 gate ✅ with today's date, set current phase to 1, and tell them to run `/req-ask`.
   - If **no**: leave the gate open and invite them to continue capturing later.

Do not advance past Phase 0 in this command under any circumstances.
