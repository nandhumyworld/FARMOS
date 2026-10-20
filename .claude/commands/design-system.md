---
description: Phase 4b — design the farmOS v1 visual design system (typography, color, spacing, components, responsive rules) on Tailwind. Records the design language; writes no app code.
argument-hint: (optional) a direction to start from, e.g. "clean, earthy, high-contrast"
---

Invoke the `farm-requirements` skill and run **Phase 4b: Visual Design System**.

**Scope is v1 only** — a lean, consistent system for the v1 screens; no speculative
component library for v2 features.

1. **Gate check.** Read `docs/requirements/STATUS.md`. Require the **Phase 4a sub-gate**
   ("UX & flows confirmed") ✅. If it is open, STOP and tell the user to run `/design-flows`.
2. Read `docs/requirements/30-design-decisions.md` (`## UX & flows`) and the relevant parts
   of `ARCHITECTURE-v1.md` (SD-2: **Django templates + HTMX + Alpine + Tailwind**; REQ-022
   **responsive** laptop + phone; REQ-024a **English-only**) so the system fits the stack
   and the screen inventory it must style.
3. **Reuse `frontend-design`** — establish an intentional, non-templated visual language:
   - **Typography** (families, scale, weights), **color** (palette + semantic roles incl.
     income/expense/positive/negative and the **negative-stock / outstanding** states),
     **spacing/rhythm**, **iconography**.
   - **Core components** the v1 screens need: app shell/nav, data tables/lists, forms &
     inputs, the quick-sale/entry panels, stat/KPI tiles for P&L & turnover, badges
     (paid/part/credit, in_house/outsourced, shortfall), buttons, empty/error states.
   - **Responsive rules** for laptop (`/`) and phone (`/m/`), expressed as Tailwind
     conventions (tokens/utilities), and **print styling** for the exportable reports (SD-7).
   Present options with a recommendation; let the user choose. Keep choices concrete enough
   to implement in Tailwind, but write **no application code** — this is the design language,
   not components in the repo.
4. **(Optional) swatch/specimen.** If a visual reference helps, produce a small specimen
   (Excalidraw, or an SVG/PNG into `docs/requirements/`) showing type scale, palette and a
   couple of key components; record its checkpoint id / file path.
5. Record confirmed decisions in **`docs/requirements/30-design-decisions.md`** under the
   `## Design system` section as dated decisions (what + why + which screen/REQ it serves).
6. When the user confirms the design system is settled, log a **Phase 4b sub-gate**
   ("design system confirmed") ✅ in `STATUS.md` with today's date, and tell them to run
   `/design-data`.

Do not redesign flows/navigation (that was `/design-flows`), specify field-level
forms/validation (that is `/design-data`), scaffold the project, or write app/template code.
