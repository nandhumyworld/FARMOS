# farmOS — Build Plan, v1 (MVP)

> **Phase 5a (Build Planning).** Drafted 2026-10-17 via `/build-plan`, using
> `superpowers:writing-plans` at **slice granularity**. Each slice below is a unit that
> `/build-next` expands at build time (this plan carries **no per-step code**).
> Revised 2026-10-18 to a **UI-first** build strategy at the user's direction.
>
> **Spec (the source of truth, do not re-derive):** `REQUIREMENTS-v1.md`,
> `ARCHITECTURE-v1.md` (+ the Phase-5 addendum SA-8..SA-12 in `20-architecture-decisions.md`),
> `DESIGN-v1.md`.
>
> **Execution method:** this project's **`/build-next`** command, one slice per invocation.
> No writing-plans execution handoff; scaffolding begins only at `/build-setup`.

**Goal:** Build the farmOS v1 single-farm operations app — capture harvests, production,
procurement and sales through an atomic, audited service layer, and read back P&L /
turnover / outstanding and per-batch economics.

**Architecture:** Django 5.2 LTS, layered **thin views → service layer (`transaction.atomic()`)
→ ORM/PostgreSQL** (SA-1). HTMX + Alpine + Tailwind templates serve a laptop hub (`/`) and a
phone-first family subset (`/m/`); Django `/admin/` owns lookups/catalog/prices/users. One
`StockMovement` ledger is the stock source of truth; income is accrual.

**Tech Stack:** Django 5.2 (Python 3.12+), PostgreSQL, HTMX, Alpine.js, Tailwind (standalone
CLI, build stage), gunicorn + WhiteNoise, django-auditlog, Docker on Coolify. No Celery/Redis,
no DRF, no server-side PDF (browser print, SD-7).

## Build strategy — UI-first (user direction, 2026-10-18)

Build the **cheap-to-change things first**: stand up every screen as a **static UI
prototype** (Django templates + Tailwind + HTMX/Alpine, fed by **hardcoded mock context** —
**no database, no models, no services**), click through it, and refine fields, flows, labels
and usability there. Only once the UI is approved do we build the **expensive-to-change**
layer — models, migrations and the service layer — **behind the already-approved screens**,
replacing mock context with real data. This surfaces missing fields/flows before they cost a
migration.

**The two stages:**
- **Stage A — UI prototype** (Slices A1–A4): static, no DB. Iterate freely; **UI review gate**
  at the end. Any field/flow change discovered here is folded back into `DESIGN-v1.md` /
  `30-design-decisions.md` before Stage B.
- **Stage B — Backend wiring** (Slices B0–B10): models + migrations + service layer + tests,
  wired behind the approved templates. **TDD applies here** (the behavioural tests live in
  Stage B).

**Contract between the stages:** Stage A templates use **context variable + form field names
that mirror the `DESIGN-v1` DD field specs**, so Stage B wiring is a swap (real context in,
mock context out), not a rewrite. Stage A commits no model, migration or service.

## Global Constraints (every slice inherits these)

- **Money = `Decimal(12,2)`, quantity = `Decimal(12,3)`** — never float (applies in Stage B).
- **Service layer is the only writer** of operational data; views stay thin (SA-1). Every
  operational write is one `transaction.atomic()` function; the acting user is passed in so
  **django-auditlog records who** (SA-3/SA-6). **No bulk writes** on audited models. (Stage B.)
- **Negative stock is ALLOWED** — warn inline, never block, never modal (SA-4, DD-0). The
  warning cue is prototyped in Stage A; enforced-as-non-blocking in Stage B.
- **`Transaction` and `StockMovement` are read-only in Django admin** (SA-1); the only admin
  write to stock is `adjust_stock` (SA-8). (Stage B.)
- **Edit-in-place corrections** re-post atomically (auditlog keeps before/after); deletes are
  **PROTECT**ed; lookups **archive** (`is_active=false`), never hard-delete (SA-4, DD-0).
- **Edit/delete policy = SHARED FAMILY EDIT (SA-12):** any owner/family user may edit/delete
  any operational record regardless of creator; admin edits anyone's. `created_by`/
  `updated_by` are recorded but **do not gate** the edit/delete controls for owner/family.
- **Dates:** default today (Asia/Kolkata), back-dating allowed, **future blocked** (DD-0).
- **Inputs positive** (`inputmode="decimal"`); units **display-only** from `Item.unit`; HTMX
  validation re-renders the form partial with inline messages; **double-submit guard**
  (`hx-disabled-elt` + server token) (DD-0).
- **English-only** (REQ-024a); responsive, design-system tokens per `DESIGN-v1.md` DS-1..6
  (blue-600 primary, tabular numerals, Indian grouping + accounting parentheses).
- **Model field additions (SA-10)** land in the Stage-B slice that first needs them:
  `Item.code` (required/unique/uppercase/2–8), optional `Entity.code`,
  `Contact.name`/`phone`/`notes`, `Transaction.note`, editable `Batch.origin`.

## Review Focus (Stage B — implied by the spec, exercised in the named slice's tests)

- **Negative-stock sale/production** — selling/consuming more than on hand must *warn and
  succeed*, leaving a negative batch balance, not raise. → Slices B6, B4.
- **Batch-number collision** — two harvests of the same item on the same day: second gets a
  `-2` suffix, uniqueness holds. → Slice B3.
- **Payment over-collection** — `record_payment` / initial sale payment must reject `amount >
  outstanding` and `amount ≤ 0`; outstanding = sale total − Σ payments. → Slice B6.
- **Edit-in-place re-post** — correcting a posted sale/harvest/run must atomically reverse and
  re-apply its movements + transaction. → Slices B3–B6.
- **Fiscal-year / future-date boundary** — a report period spanning the April FY start, and a
  future `txn_date`, behave per `FarmProfile.fiscal_year_start_month` and the future-block. →
  Slices B9, B2.

---

## Delivered by `/build-setup` (not a `/build-next` slice)

Project skeleton for the **UI prototype**: Django project + `core` app, split settings,
`requirements.txt`, Tailwind config + base template/app-shell (DS-5/DS-6), `Dockerfile` +
`.dockerignore` + `.gitignore`, `/healthz`, README. **The only model created here is an
empty custom user** (`User(AbstractUser)` + `AUTH_USER_MODEL`) — the one Django choice that
is cheap now and painful to change later, and no domain structure that UI feedback could
alter; its **initial migration is run** so the prototype's `runserver` is warning-free.
**No domain models** (those are Stage B). A **zero-config dev DB (SQLite)** serves the static
prototype, so the 5b smoke check (`manage.py check` + migrate + empty test run) passes
without installing Postgres; the **Postgres dev/test DB and all domain migrations are
deferred to Stage B** (B0/B1). The DB decision is part of `/build-setup`'s batched consent
question so it is on record early.

---

## STAGE A — UI prototype (static templates, mock context, no DB)

### Slice A1 — Design system + app shell
- **Delivers:** Tailwind token setup (DS-2 colors incl. money/status, DS-3 type scale +
  tabular numerals, DS-4 Indian grouping/parentheses helpers, DS-5 components, DS-6
  responsive + **print stylesheet**); the base layout, laptop top nav (`/`) and `/m/` shell;
  reusable component partials (buttons, 44px inputs, segmented Paid/Partial/Credit toggle,
  tables→cards, KPI tiles, worded light-tint badges, empty + error states); a static
  **login page** template (the family sees it on phone; real auth is wired in B0); a static
  **style-guide page** to eyeball the components.
- **Review:** matches the specimen (`farmOS-v1-design-system.svg`) and reads well on phone.
- **Serves:** DS-1..6, REQ-022/024a. **Depends on:** setup.

### Slice A2 — Capture screens (static, mock data)
- **Delivers:** **Quick Sale** (price snapshot fill, Paid/Partial/Credit toggle, contact +
  inline-add affordance), **Record Expense/Income** (all attribution visible, overhead
  toggle), **Harvest** (auto batch-no. field), **Production** (input/output builder + **live
  tally** via Alpine, mock), **Procurement** (vendor + new/pick-batch). HTMX/Alpine
  interactions mocked against stub endpoints; confirm → **Add another/Done** pattern (UX-3).
- **Review:** every field from `DESIGN-v1` DD-1..DD-5 present and named per spec; flows feel
  right for catch-up entry.
- **Serves:** UX-4..UX-8, DD-1..DD-5 (layout only). **Depends on:** A1.

### Slice A3 — Browse / read screens (static, mock data)
- **Delivers:** **Dashboard** action hub + P&L/turnover/outstanding snapshot (UX-1);
  **Inventory/Stock** with **inline red shortfall badges** + price list (UX-11); **Batches**
  with per-batch P&L layout; **Entities** list/detail; **Contacts** list/detail (history +
  outstanding + per-sale payment affordance, UX-9); **Reports** (period + whole-farm/per-batch
  toggle + **print preview**).
- **Review:** the numbers' placement, badges, and print layout read correctly with mock data.
- **Serves:** UX-1/UX-9/UX-10/UX-11, DD-8. **Depends on:** A1.

### Slice A4 — `/m/` family subset (static, mock data)
- **Delivers:** phone-first **Sell · Record Expense/Income · Add Contact · Collect Payment ·
  read-only "Today" card**; **hub-and-back** nav, bottom-pinned action clearing
  safe-area/keyboard (DS-6).
- **Review:** thumb-reachable, only the five flows, matches the wireframe.
- **Serves:** SD-3, UX-2. **Depends on:** A1 (and the A2/A3 partials it reuses).

> **▲ UI REVIEW GATE (logged in STATUS.md)** — walk the whole clickable prototype (`/` and
> `/m/`). This is the cheap place to change things. Capture every field/flow/label/usability
> change as a **dated addendum** (do not rewrite the finalized docs):
> - UX/flow/label/field-layout changes → a dated note in `30-design-decisions.md` (and, if it
>   alters a finalized screen/flow statement, a dated addendum line in `DESIGN-v1.md`);
> - **any new/changed data field or structure** (a field to add, rename, re-type) → a **dated
>   addendum to `20-architecture-decisions.md`** (the way SA-10 was added), so the model is
>   corrected **before B1 migrates**. This is the user's core reason for UI-first: add it in
>   front before it becomes an expensive migration.
>
> When the user confirms the prototype is good, the agent logs the **UI-review sub-gate** ✅
> in STATUS.md (gate log + its row in `## Slice progress`). B0 refuses until it is ✅.

---

## STAGE B — Backend wiring (after UI approved; TDD)

> Each Stage-B slice wires **already-built templates** to real models + services, replacing
> mock context. Views stay thin; services are the only writers (SA-1).

### Slice B0 — Backend foundation
- **Delivers:** **admin/owner-family groups** + real session login/logout **wired behind
  A1's login template**; switch dev/test DB to the chosen **Postgres** (the custom user model
  already exists from setup); **django-auditlog** base + audited abstract model
  (`created_by/at`, `updated_by/at`).
- **Tests:** role gating (family blocked from `/admin/`); login required on `/`; auditlog
  captures actor.
- **Serves:** REQ-021/027; SA-3/SA-5/SA-6. **Depends on:** Stage A approved (▲ UI review gate).

### Slice B1 — Lookups, profile & catalog (admin)
- **Delivers:** `FarmProfile` (single row, logo, `fiscal_year_start_month`),
  `EntityCategory`, `Stage` (seeded), `Plantation`, `Tag`, `Item` (**`code`**, unit,
  sale_price, vendors M:N), `Contact` (name/phone/notes, type), `Recipe` — in `/admin/`,
  auditlog registered, **archive-not-delete** + **PROTECT**.
- **Tests:** `Item.code` validation (required/unique/uppercase/2–8); single-FarmProfile guard;
  archive hides from pickers but preserves history.
- **Serves:** REQ-003/004/005/032/033/009/014/027; SA-10. **Depends on:** B0.

### Slice B2 — Entities, ledger & `record_transaction`
- **Delivers:** `Entity` (optional `code`, admin-creatable) + wire the **Entities** screen;
  `Transaction` (direction/amount/txn_date/is_overhead/**note**/attribution FKs/tags);
  `StockMovement` + `Batch` models; wire **Record Expense/Income** to **`record_transaction`**
  + edit-in-place.
- **Tests:** posts one audited row; overhead clears entity; future date blocked; edit re-posts.
- **Serves:** REQ-001/002/005/031/017; DD-5, SA-8. **Depends on:** B1.

### Slice B3 — Harvest & `record_harvest`
- **Delivers:** wire **Harvest** → **`record_harvest`** opens an `in_house` `Batch`
  (`<ITEMCODE><YYMMDD>`, editable, `-2` on collision) + positive `StockMovement`; edit-in-place.
- **Tests:** batch-no. auto + collision + uniqueness; movement sign; ≥1 of entity/plantation;
  edit re-posts.
- **Serves:** REQ-034/010/006; DD-1. **Depends on:** B2.

### Slice B4 — Production & `run_production`
- **Delivers:** wire **Production** → `ProductionRun`/`ProductionLine` + **`run_production`**
  (≥1 in/≥1 out; `Batch.origin` default-inherited, **editable**; recipe guides); live tally
  now real; edit-in-place.
- **Tests:** multi-in→multi-out lineage; repack allowed; **over-consume warns, not blocks**;
  edit re-posts.
- **Serves:** REQ-007/008/009/010; DD-2. **Depends on:** B3.

### Slice B5 — Procurement & `procure`
- **Delivers:** wire **Procurement** → `Procurement` + **`procure`** (outsourced `Batch`, new
  or **open-batch query** SA-11; `purchase` `StockMovement` + vendor **expense Transaction**;
  inline vendor add); edit-in-place.
- **Tests:** vendor required; purchase movement + expense txn atomic; open-batch query order.
- **Serves:** REQ-036/033/002; DD-3. **Depends on:** B2.

### Slice B6 — Quick sale, initial payment & `record_payment`
- **Delivers:** wire **Quick Sale** → **`record_sale`** (price snapshot; contact required +
  inline add; negative `StockMovement` + income `Transaction`; **initial `Payment`**, SA-9);
  `Payment` model + **`record_payment`** (per-sale collect, `0 < amount ≤ outstanding`);
  outstanding computed; edit-in-place.
- **Tests:** **over-sell warns, not blocks**; payment over-collection + non-positive rejected;
  accrual income at sale time; Paid/Partial/Credit from Σ payments; edit re-posts.
- **Serves:** REQ-011/013/032; DD-4/DD-6, SA-9. **Depends on:** B2.

### Slice B7 — Inventory, shortfall, batch P&L & `adjust_stock`
- **Delivers:** wire **Inventory/Stock** (stock = Σ movements; red shortfall badges real;
  price list) and **Batches** (per-batch P&L = **direct-tag + descendant roll-up**, OD-5);
  admin **Adjust stock** on Batch detail → **`adjust_stock`** (admin-only, audited
  `adjustment`).
- **Tests:** stock sums across reasons incl. negatives; roll-up aggregates descendants;
  `adjust_stock` admin-only + audited.
- **Serves:** REQ-006/032/010, UX-11; DD-9, SA-8. **Depends on:** B3,B4,B5,B6.

### Slice B8 — Dashboard & Contacts (real data)
- **Delivers:** wire **Dashboard** figures and **Contacts** list/detail (history + outstanding
  computed; per-sale payment entry) to the ledger/payments.
- **Tests:** dashboard figures match ledger; contact outstanding = Σ(sale totals) − Σ(payments).
- **Serves:** REQ-016/014; UX-1/UX-9. **Depends on:** B2,B6.

### Slice B9 — Reports & print (real data)
- **Delivers:** wire **Reports** over the `Transaction` ledger (period this-month/FY/custom
  `from ≤ to`; whole-farm ↔ per-batch); print/Save-as-PDF real (SD-7); order-confirmation
  document on sale. *(Price list lives on Inventory — B7.)*
- **Tests:** FY-boundary (April) sums correctly; custom-range validation; print stylesheet.
- **Serves:** REQ-016/015; SD-7, DD-8. **Depends on:** B2–B8.

### Slice B10 — `/m/` wiring
- **Delivers:** wire the `/m/` subset (Sell, Expense/Income, Add Contact, Collect Payment,
  Today card) to the same services — no new logic.
- **Tests:** `/m/` exposes only the five flows; actions round-trip through the same services
  as `/`.
- **Serves:** SD-3, UX-2; REQ-021/022. **Depends on:** B6,B8.

---

## Build-order summary
setup (static skeleton, SQLite dev DB) → **A1** design system/shell → **A2** capture screens →
**A3** browse screens → **A4** `/m/` → **▲ UI review gate** → **B0** backend foundation (user,
Postgres, auditlog) → **B1** lookups/catalog → **B2** ledger + `record_transaction` → **B3**
harvest → **B4** production → **B5** procurement → **B6** sale + payment → **B7**
inventory/shortfall/batch-P&L/adjust → **B8** dashboard/contacts → **B9** reports/print →
**B10** `/m/` wiring → `/build-finalize`.

v2 seams stay out of every slice: order workflow (REQ-011b/012), OD-5 cost-allocation,
report slices per entity/product/plantation/contact (REQ-016 remaining), plantation rollup
(REQ-019), visit/enquiry log (REQ-035), WeasyPrint (SD-7), Capacitor APK build (SD-3).
