# farmOS — Design Decisions (Phase 4 working log)

> Dated decisions for Phase 4 (Design). Each entry records **what** was chosen,
> **why**, the **REQ-NNN / screen** it serves, and (where relevant) the Excalidraw
> **diagram checkpoint id**. Scope is **v1 only**; v2/later flows are notes only.
> This is the working log; `/design-finalize` consolidates it into `DESIGN-v1.md`.
>
> Sections: `## UX & flows` (4a), `## Design system` (4b), `## Detailed data & forms` (4c).
> Decision IDs: **UX-n** (4a). Builds on Phase 3 (`ARCHITECTURE-v1.md`: service layer
> `record_sale` / `record_harvest` / `run_production` / `procure` / corrections; roles
> admin vs owner/family; routes `/`, `/m/`, `/admin/`).

---

## UX & flows

> Phase 4a (`/design-flows`) — structure/flow only (no fonts/colors/components = 4b;
> no field-level validation/defaults = 4c). **Confirmed 2026-10-16** (UX-1..UX-11 +
> nav/flow map `e456b9e36d7b4b7d8a` + wireframes `ccf74978f59b4220ae`; Phase 4a sub-gate ✅).

### UX-1 — Screen inventory & navigation: action-first hub · 2026-10-16

- **Chosen:** A **12-screen v1 set** reached via an **action-first hub**. The Dashboard
  (`/`) is home: a row of **verb buttons** for the frequent captures — **Sell, Record
  Expense/Income, Harvest, Produce, Procure** — above a **P&L / turnover / outstanding**
  snapshot. *(An earlier draft also showed a dashboard "shortfall alert"; **superseded by
  UX-11** — shortfall is surfaced inline on Inventory, not on the dashboard.)*
  Browse/registers sit in a secondary nav bar:
  **Dashboard · Inventory · Batches · Entities · Contacts · Reports · Admin**.
- **Screen set:** Dashboard/P&L home; Quick Sale; Record Expense/Income; Harvest;
  Production; Procurement; Inventory/Stock (incl. shortfall surface + price list); Batches
  (per-batch P&L); Entities; Contacts (history/outstanding/collect payment); Reports;
  Admin (link out to Django `/admin/`).
- **Why:** The app's whole point is *fast capture* (REQ-011 quick sale, REQ-005/031
  expense). Leading with verbs puts the highest-frequency tasks one tap from home, and the
  same verb set maps 1:1 onto the `/m/` phone subset (UX-2). Registers/reports are
  lower-frequency browse, so they live one level down.
- **Serves:** REQ-011/013/032 (sale), REQ-002/005/031/017 (ledger), REQ-034 (harvest),
  REQ-007/008/009 (production), REQ-036 (procurement), REQ-006 (stock), REQ-010 (batch
  P&L), REQ-001 (entities), REQ-014/033 (contacts), REQ-016/015 (reports), REQ-004/032/021
  (admin via `/admin/`).
- **Rejected:** **Flat nav** (every screen an equal top-level item — frequent captures get
  no priority over rare browse); **grouped-by-domain nav** (tidy taxonomy but buries the
  common "sell / log expense" verbs behind a group click).
- **Note:** Catalog, prices, categories/stages/tags, users and FarmProfile are **Django
  `/admin/`** (SA-1/SA-3) — no custom v1 screens; the "Admin" nav item is just a link out.
- **Creation default (stated, correctable):** **creating** Entities and Items (incl. a new
  bought-in product before you can procure it) happens in **`/admin/`** (the owner is
  admin, SA-3). The app's **Entities** and **Inventory** screens are **list + detail**
  (browse/view), not create forms, in v1. Flag for 4c if quick in-app create is wanted.
- **Architecture follow-up:** plain **expense/income** entry (REQ-002/005/031) has **no
  named service** in `ARCHITECTURE-v1.md` (only `record_sale`/`record_harvest`/
  `run_production`/`procure`). The Record Expense/Income screen maps to a plain
  `Transaction` create; recommend adding a `record_transaction` service (same atomic/audited
  pattern) when Build starts. Flagged, not invented here.

### UX-2 — `/m/` family subset: capture + customer · 2026-10-16

- **Chosen:** The `/m/` phone-first subset exposes five things: **Sell, Record
  Expense/Income, Add Contact/Visitor, Collect Payment**, and a read-only **"Today" card**
  (P&L / turnover / outstanding). Nothing else — production, procurement, batches, stock,
  catalog, reports and `/admin/` are full-site (laptop) only.
- **Why:** This is everything family does day-to-day with money and customers, matching
  SD-3's "most-used family tasks" while deliberately keeping the heavier operational
  surface off the phone. Collect-payment is included because credit sales (REQ-013) are
  common and family handles customers, so chasing a later payment shouldn't force a laptop.
- **Clarification:** `/m/` is **UX curation, not a permission boundary** (SA-3) — the
  owner/family role has full operational access; `/m/` just presents a curated entry point.
  The same underlying screens/services back `/` and `/m/` (SD-2/SD-3: one Django codebase).
- **Serves:** REQ-022 (phone), REQ-011 (sell), REQ-005/031 (expense), REQ-014 (contact),
  REQ-013 (collect payment), REQ-016 (today's P&L/turnover).
- **Rejected:** **Minimal capture-only** (drops collect-payment — forces a laptop for a
  routine credit follow-up); **capture + field work** (adds Harvest — pulls batch-numbering
  onto the phone and creeps toward the full operational surface SD-3 wanted off `/m/`).
- **v2 note:** `/m/` is the surface the Capacitor APK (SD-3) will wrap; harvest/other flows
  are an easy later add if family field-use demands it.

### UX-3 — Global interaction patterns (edit location + post-save landing) · 2026-10-16

Decided once, globally; the per-flow wireframes (UX-4..UX-11) inherit these.

- **(a) Edit/correct lives on the record's detail page.** Every list (sales, transactions,
  batches, harvests, runs, procurements) opens a **read-only detail page** per row; that
  page carries **Edit** and **Delete**. Edit reopens the same capture form, prefilled;
  Delete confirms first. This is the single canonical place to view and correct an audited
  posting, and it's the only shape that fits complex records (a production run's many
  lines) — which an inline row editor can't hold.
  - **Why:** SA-4 corrections re-post stock+ledger atomically with audit history (REQ-027);
    a deliberate detail→edit path suits audited money/stock far better than easy-mistap
    inline edits.
  - **Rejected:** inline-in-row HTMX edit (riskier for financial rows; can't represent
    multi-line runs).
- **(b) After saving a capture: confirm, then "Add another" or "Done".** On save, show a
  success confirmation naming the effect ("Sale recorded ₹450 — stock updated") with
  **"Add another"** (reopens a cleared form for fast repeat entry) and **"Done"** (back to
  dashboard / `/m/` home).
  - **Why:** Farm data entry is often **catch-up** — several sales/expenses logged in one
    sitting; "Add another" removes a round-trip per entry while the confirmation still
    reassures. Applies on `/` and `/m/`.
  - **Rejected:** always-return-to-dashboard (re-opening the form each time is slow for
    batch entry); go-to-new-record (adds a step before the next entry).

### UX-4 — Harvest flow + batch-number convention · 2026-10-16

- **Flow:** `Dashboard ▸ + Harvest` → form: **Date** (default today) · **Source**
  (Entity or Plantation) · **Item** (raw material) · **Qty + unit** · **Batch no.**
  (auto-generated, editable) → Save → service **`record_harvest`** (atomic: opens `Batch` +
  posts positive `StockMovement`, reason=harvest) → confirmation naming the effect
  ("Harvest recorded · Batch COCO-261016 opened · +500 nuts in stock") → Add another / Done
  (UX-3b). Edit/delete via the harvest detail page (UX-3a).
- **Batch-number convention (user-confirmed):** **auto-generated, editable**, format
  **`<code><YYMMDD>`** where `<code>` is the **product/item code** (user-confirmed: the
  **item** code, not the source entity — one rule across harvest, production and
  procurement) and `<YYMMDD>` is the event date (e.g. `COCO-261016`). Same-item-same-day
  collision → append a numeric suffix (`-2`). Stays fully user-editable (REQ-010).
- **Why:** Low-friction and naturally consistent (readable, sortable, meaningful) while
  honouring REQ-010's "user-defined, may encode name+date". The code+date scheme makes a
  batch id self-describing at a glance across a busy season.
- **Serves:** REQ-034 (harvest event), REQ-010 (batch numbering), REQ-006 (raw stock).
- **Rejected:** **fully manual** (inconsistent formats, typos, accidental dupes);
  **auto-sequential** `BATCH-0001` (unique + zero typing but opaque — no meaning in the id).
- **Data follow-up (flag for 4c / Build):** `Entity` and `Item` need a short **`code`**
  field — not explicit in `ARCHITECTURE-v1.md`'s domain model. It drives the batch-number
  generator (and is reusable elsewhere). Field-level rules (length, uniqueness, separator
  char `-`) are a Phase 4c detail.

### UX-5 — Production run flow: single-screen builder + live tally · 2026-10-16

- **Flow:** `Dashboard ▸ + Produce` → one screen, two stacked panels: **Inputs (consume)**
  and **Outputs (produce)**, each an **add-as-many** line (Item · Batch · Qty), rows added
  via HTMX. Choosing an input **filters the output Item choices to that input's `Recipe`**
  (REQ-009). Output lines open/assign an output `Batch` (same `<code><YYMMDD>` convention,
  UX-4), **linking lineage** (REQ-010 descendant roll-up). A **live tally bar** summarises
  total consumed vs produced. One **Save** → service **`run_production`** (atomic: one
  `StockMovement` per line — production-in for inputs, production-out for outputs) →
  confirm → Done. Edit/delete via the run detail page (UX-3a), which re-posts all lines
  atomically.
- **"Tally" clarified:** value-add transforms units, so tally is **not** input-qty =
  output-qty; it is a **reconciliation summary** (everything consumed, with resulting
  stock, vs everything produced) the user eye-checks before posting. No forced equality.
- **Why:** The whole run is visible at once — the right shape for reconciliation and for
  branching runs that mix input batches and yield byproducts. Plays to HTMX partial-update
  strengths (SD-2). Recipe filtering guides output choice without constraining ad-hoc runs.
- **Serves:** REQ-007 (branching transformation), REQ-008 (consume/yield + tally),
  REQ-009 (per-input recipes), REQ-010 (batch lineage).
- **Rejected:** **two-step stepper** (more clicks; can't see inputs+outputs together while
  entering); **recipe-first** (fast for standard recipes but awkward for ad-hoc runs mixing
  inputs or producing an unplanned byproduct).

### UX-6 — Procurement flow: new batch by default, mergeable · 2026-10-16

- **Flow:** `Dashboard ▸ + Procure` — its **own screen** (parallel to Harvest, but it
  additionally posts a vendor expense). Form: **Item** · **Vendor** (Contact type=vendor) ·
  **Qty + unit** · **Cost ₹** · **Date** · **Batch** → Save → service **`procure`** (atomic:
  `origin=outsourced` `Batch` + positive `StockMovement` reason=`purchase` + **expense
  `Transaction`** linked to the vendor) → confirm → Done. Editable via the procurement
  detail page (UX-3a). Procurement is started from **`Dashboard ▸ + Procure`** only;
  there is **no** prefilled-from-shortfall launch in v1 (consistent with UX-11 — a
  prefilled "Procure from shortfall" shortcut is a v2 note).
- **Batch granularity (user-confirmed, after a worked honey example):** the Batch field
  **defaults to a new outsourced batch** (clean per-lot cost + resale margin — REQ-036
  intent) **but lets the user pick an existing open outsourced batch to merge into** when
  they want fewer lots. New-by-default gives exact per-lot margin; merging is a deliberate
  on-demand choice. Either way each purchase remains its own editable `Procurement` record.
- **Why:** REQ-036's purpose is knowing resale margin per bought-in lot; a new batch per buy
  keeps that exact, while the "pick existing" escape hatch avoids forcing lots the owner
  doesn't want. Mirrors the Harvest batch convention (UX-4).
- **Serves:** REQ-036 (outsourced goods/procurement + vendor expense), REQ-033 (vendor
  contact), REQ-010 (batch), REQ-006 (stock), REQ-002 (expense ledger).
- **Rejected:** **always-new** (can never merge even when wanted); **always-append**
  (per-lot margin always blended — the ₹107.50 case).
- **Data follow-up (flag for 4c):** optionally offer, on save, to add the chosen vendor to
  `Item.vendors` (the standing supplier list) if not already linked — small convenience,
  field-level detail for 4c.

### UX-7 — Quick sale flow: price snapshot + payment toggle · 2026-10-16

- **Flow:** `Dashboard ▸ + Sell` → one line: **Item** → **Batch** (lot picker showing
  stock-on-hand; **negative allowed** — shortfall signal, UX-11) → **Qty** → **Price**
  (auto-filled snapshot from `Item.sale_price`, editable — REQ-032) → **Contact** →
  **payment**. Save → service **`record_sale`** (atomic: `Sale` with price snapshot +
  negative `StockMovement` reason=sale + income `Transaction`, **accrual** — income counts
  now regardless of cash). Confirm ("Sale recorded ₹450 — stock updated") → Add another /
  Done (UX-3b); confirm screen also offers **order-confirmation share** (UX cross-ref to
  REQ-015, handled in Reports/compose). Edit/delete via sale detail page (UX-3a).
- **Payment capture (user-confirmed):** a **Paid / Partial / Credit toggle** driving an
  editable **Received** amount. *Paid* → Received = total; *Partial* → reveals Received
  field + shows **Outstanding** live; *Credit* → Received = 0, full outstanding. Each
  payment is a `Payment` row; outstanding = sale total − Σ payments (REQ-013). Later
  payments collected via the contact flow (UX-10).
- **Why:** The toggle is explicit about intent ("this is on credit") yet one tap for the
  common paid-in-full case; avoids the silent-credit risk of a bare amount field.
- **Serves:** REQ-011 (quick sale), REQ-032 (price catalog snapshot), REQ-013 (payment
  tracking), REQ-010 (batch link → per-batch P&L), REQ-014 (contact history).
- **Rejected:** **single Received amount** (fastest but silently creates credit when
  lowered); **sale-now-payment-later** (splits one natural action; adds a step to the
  common paid-in-full case).
- **Scope guard:** one item · one batch · one contact per sale (v1). Cart / multi-product /
  multi-batch orders and the formal order workflow are **v2** (REQ-011b/012).

### UX-8 — Record Expense/Income flow: all attribution visible · 2026-10-16

- **Flow:** `Dashboard ▸ + Expense` (Income = same form, direction toggle; default
  Expense) → Save → creates a `Transaction` (see architecture follow-up in UX-1: recommend
  a `record_transaction` service) → confirm → Add another / Done (UX-3b). Edit/delete via
  transaction detail page (UX-3a). Also reachable on `/m/` (UX-2).
- **Attribution (user-confirmed):** **all attribution fields shown on one screen** — no
  progressive disclosure. Fields: Amount, Date, and the full REQ-017 attribution set —
  **Entity, Batch, Item, Stage, Plantation, Contact, Tags**, an **Overhead** flag
  (REQ-031, `is_overhead`), and a Note. All attribution is optional (REQ-005 free ledger),
  but always in view so nothing gets skipped for being hidden.
- **Why (owner's choice):** the owner wants every entry fully attributable in one pass and
  prefers all tags visible over a shorter default form; the point of the system is capturing
  rich attribution so no data is lost (REQ-017). Accepted trade-off: a longer form even for
  small everyday expenses.
- **Examples:** salary = expense attributed to the **employee `Entity`**; electricity =
  expense with **Overhead** on; feed = expense attributed to the "Cows" `Entity`.
- **Serves:** REQ-002 (dual ledger), REQ-005 (free ledger + stage), REQ-031 (overhead),
  REQ-017 (rich attribution), REQ-033 (vendor contact on expense).
- **Rejected:** **core + expandable** (shorter common case, but owner wants all tags in
  view); **category-driven** (relies on admin-maintained types; adds a step per entry).
- **Layout follow-up (flag for 4c / design-system):** with all fields on one screen,
  grouping/ordering (money first, then attribution, logical visual grouping) and
  responsive stacking on `/m/` matter so the single form doesn't overwhelm — a 4b/4c
  layout concern, not a change to this flow decision.

### UX-9 — Contacts + collect-payment flow: payment is per-sale · 2026-10-16

- **Contacts:** `Contacts` list (filter by type customer | visitor | vendor, REQ-033) →
  **contact detail**: type/tags, **auto-built purchase history** (computed, REQ-014),
  **outstanding balance** (computed = Σ unpaid sale balances), and the contact's **unpaid
  sales listed with outstanding badges**, each a **link into that sale's detail**. Add
  contact from the list, from `/m/` (UX-2), and inline during a sale (UX-7).
- **Collect payment (user-confirmed): per-sale only.** A `Payment` is always added on the
  **sale's detail page** ("Add payment ₹___ on date"), creating a `Payment` row linked to
  that `Sale`; outstanding = sale total − Σ payments (REQ-013). No contact-level batch
  settle screen in v1. To pay down a multi-sale tab, open each unpaid sale (reached via the
  contact detail's unpaid-sales list) and add a payment.
- **`/m/` reconciliation:** the `/m/` "Collect pay" action (UX-2) is an **entry list of
  outstanding sales** (optionally filtered by contact); tapping one opens that sale's
  detail where the payment is added — consistent with per-sale-only.
- **Why (owner's choice):** simplest to build and reason about; each payment is
  unambiguously tied to one sale, matching the `Payment → Sale` data model directly with no
  allocation rule to design.
- **Serves:** REQ-014 (contacts + history + outstanding), REQ-033 (vendor type),
  REQ-013 (payment tracking).
- **Rejected:** **itemised collect screen with 'Settle all'** (nicer for paying a whole
  tab at once, but more to build); **lump-sum auto oldest-first** (fastest but app chooses
  allocation + needs an allocation rule).
- **v2 note:** a contact-level "settle all / lump payment" screen is an easy later add if
  paying multi-sale tabs one-by-one proves tedious.

### UX-10 — Reports: one screen (period + scope) + browser print · 2026-10-16

- **Report structure (user-confirmed):** a **single Reports screen** with a **period
  picker** (This month / This FY-season / Custom range — filters `Transaction.txn_date`,
  respects `FarmProfile.fiscal_year_start_month`) and a **Whole-farm / Per-batch scope
  toggle**. Whole-farm = income / expense / net P&L + turnover + outstanding (reads the
  `Transaction` ledger). Per-batch = the batch's **direct-tagged** P&L **+ descendant-batch
  roll-up** (OD-5); per-batch is **also linked from each Batch detail page** (you're already
  looking at the batch).
- **Export (user-confirmed):** **browser print / Save-as-PDF** with print-optimised CSS
  (SD-7) — no new dependencies (REQ-026). Phone sharing = Save-as-PDF then attach in
  WhatsApp. **WeasyPrint stays the documented upgrade** if phone save-then-attach proves
  clunky for the family.
- **REQ-015 compose (stated design, no new screen):** the **price list** is generated from
  the `Item` catalog via a **"Share price list"** action on the **Inventory** screen; the
  **order confirmation** is generated from a `Sale` (offered on the sale confirmation,
  UX-7). Both are print/Save-as-PDF documents shared manually via WhatsApp.
- **Why:** one Reports screen = one place to learn, consistent controls, batch view where
  you already are; browser print keeps v1 dependency-free per SD-7.
- **Serves:** REQ-016 (whole-farm + per-batch P&L/turnover; month/year/custom;
  print/share), REQ-015 (price list / order confirmation), OD-5 (descendant roll-up).
- **Rejected:** **separate report pages** (two places + duplicated period picker);
  **dashboard-embedded** (heavy dashboard, harder to print cleanly); **WeasyPrint now**
  (adds server PDF lib + system libs to the image — deferred per SD-7).
- **Scope guard:** v1 slices are **whole-farm + per-batch only**. Per-entity /
  per-product-type / per-plantation / per-contact report slices are **v2** (REQ-016
  remaining); Entity/Contact detail pages may *list* their transactions but are **not**
  per-entity/contact P&L report views.

### UX-11 — Negative-stock shortfall surface: inline red badges · 2026-10-16

- **Chosen (user-confirmed):** negative stock is surfaced as **inline red badges** wherever
  an item/batch appears — primarily the **Inventory/Stock list** (and the **sale batch
  picker**, UX-7) — showing the negative balance (e.g. `Coconut −120 nut 🔴`). **No**
  dedicated shortfall list, **no** dashboard alert, **no** prefilled "Procure" shortcut in
  v1.
- **Why (owner's choice):** lightweight; the owner reads stock status on the Inventory
  screen (the "ultimate product list", per domain-model §2.3) and a red negative balance
  there is a sufficient "buy this in" signal. Procurement is started normally from
  `Dashboard ▸ + Procure` (UX-6).
- **Serves:** SA-4 (negative stock allowed), REQ-036 (shortfall-to-procure signal), REQ-006
  (stock status per item/batch).
- **Rejected:** **dashboard alert + shortfall list + prefilled Procure** (more to build;
  owner wanted it lighter); **shortfall report** (out of the daily path, not glanceable).
- **Supersedes:** the "⚠ N items short to procure" line shown in the UX-1 dashboard
  mock-up. Dashboard retains the verb buttons + P&L / turnover / outstanding snapshot but
  **drops the shortfall alert**; shortfall lives inline on Inventory instead.
- **v2 note:** a dashboard shortfall badge and a one-tap "Procure prefilled from shortfall"
  shortcut are easy later adds if the inline badge proves too passive.

### UX diagrams (Excalidraw) · 2026-10-16

Excalidraw renders inline and emits no public URL; restore via the **checkpoint id**
(`restoreCheckpoint`) or re-run `/design-flows`.

| Diagram | What it shows | Checkpoint | File |
|---|---|---|---|
| Navigation / flow map | action-first Dashboard hub + `/m/` subset + top nav → 5 capture screens → service layer (`record_sale`/`record_harvest`/`run_production`/`procure`/`record_transaction*`/corrections) → data ledgers (StockMovement / Transaction / Batch) → Browse/Reports (Inventory+shortfall, Batches, Contacts, Reports) | **`e456b9e36d7b4b7d8a`** | `farmOS-v1-ux-navigation.svg` |
| Key screen wireframes | low-fi Quick Sale (price snapshot + Paid/Partial/Credit), Run Production (input/output builder + tally), `/m/` Home (curated subset) | **`ccf74978f59b4220ae`** | `farmOS-v1-ux-wireframes.svg` |

> Checkpoints restore the live Excalidraw scene; the SVG files are the shareable canonical
> copies in `docs/requirements/` (matching the Phase 2/3 convention).

<!-- EXCALIDRAW_CHECKPOINT_NAV: e456b9e36d7b4b7d8a -->
<!-- EXCALIDRAW_CHECKPOINT_WIREFRAMES: ccf74978f59b4220ae -->


---

## Design system

> Phase 4b (`/design-system`) — **confirmed 2026-10-17** (DS-1..DS-6 + specimen
> `farmOS-v1-design-system.svg`; Phase 4b sub-gate ✅). Visual language for the v1 screens on
> the SD-2 stack (Django templates + HTMX + Alpine + **Tailwind**); REQ-022 responsive
> (laptop `/` + phone `/m/`); REQ-024a English-only. Decision IDs **DS-n**. Design language
> only — no app/template code (that is Build), no field-level forms (that is 4c).

### DS-1 — Direction: Plain & System (low-build, utility-first) · 2026-10-17

- **Chosen (user-confirmed):** a **plain, utility-first** system — **Tailwind's default
  palette** + a **system font stack** (no font hosting) + a small set of **semantic money
  tokens**. No custom display face, no hero flourish, no decorative motion. It should look
  like a clean, fast default admin app.
- **Why (owner's words):** "for internal use purpose… should serve the purpose and speed
  matters than fancy here… utility based," and it "must be suitable for mobile view when
  converting to [a] Capacitor-based app." Fast to build and load, reliable, phone-first.
- **Consequences for 4b:** later decisions default to Tailwind/system values rather than
  bespoke design; personality is intentionally minimal; effort goes to legibility, number
  clarity, speed and tap targets. The distinctive "Field Ledger" / "Register Book"
  directions were **rejected** per the owner's steer.
- **Serves:** REQ-022 (responsive, laptop + phone + APK path), REQ-026 (no paid/hosted
  dependencies — system fonts, no webfont service), SD-2 (Tailwind), SD-3 (`/m/` → APK).

### DS-2 — Color & semantic roles (Tailwind defaults) · 2026-10-17

- **Primary (interactive) = Tailwind `blue-600`** (hover `blue-700`, focus ring `blue-500`).
  White text on it passes contrast. Chosen for maximum "this is clickable" familiarity for
  a non-technical farmer/family and clear separation from money colors. (Rejected: teal-600
  — more character but closer to income green; slate monochrome — a grey button reads less
  obviously clickable.)
- **Semantic money/status tokens** (named tokens → Tailwind default shades):
  | Token | Tailwind | Used for |
  |---|---|---|
  | `income` / positive | `green-600` | income amounts, positive net P&L, Paid |
  | `expense` / negative | `red-600` | expense amounts, negative net P&L |
  | `outstanding` / partial | `amber-500` | credit owed, Partial — **as a fill with dark text** (amber fails contrast as text on white) |
  | `shortfall` | `red-600` | negative stock badge (UX-11) |
  | `in_house` | slate chip | own-produce batches (categorical) |
  | `outsourced` | sky chip | bought-in batches (categorical) |
  | neutrals | `slate-*` | text (`slate-800`), muted (`slate-500`), lines (`slate-200`), bg (`slate-50`), surface white |
- **Two hard rules (for colorblindness + grayscale farm printouts):**
  1. **Usage rule** — `blue` only on interactive elements (buttons/links/active nav/focus);
     `green`/`red` only on money direction & status. They never swap roles, so the blue↔green
     hue proximity never matters.
  2. **Not-color-alone** — money direction/negatives always carry a **non-color cue** (an
     Income/Expense column or label, or accounting parentheses for negative/loss values per
     DS-4); badges always carry **text** ("Paid" / "Partial" / "Credit" / "Short 120 nut"),
     never a bare colored dot. The UX-11 shortfall badge states the shortfall in words/number.
- **Why:** stock Tailwind shades = zero palette work (DS-1), all AA-contrast on white, and
  the rules keep meaning legible without relying on hue.
- **Serves:** REQ-016 (P&L readability), REQ-013 (payment status), REQ-036 (in_house vs
  outsourced), UX-7/UX-9/UX-11, REQ-024a, SD-7 (print).
- **Contrast notes (verify in Build):** `green-600`/`red-600`/`blue-600` all ≥4.5:1 as text
  on white/`slate-50`; `amber-500` is fill-only with `slate-900` text.

### DS-3 — Typography & scale (system stack) · 2026-10-17

- **Family:** one **system font stack** for everything (Tailwind `font-sans`:
  `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, …`). No hosted webfont
  (REQ-026); ₹ (U+20B9) renders natively on Android/Windows/iOS fallbacks.
- **Numerals:** money & quantity values use **tabular numerals** (Tailwind `tabular-nums`)
  so digits align in columns and totals line up. (Rejected: system monospace figures — a
  touch too technical beside the plain sans; proportional figures — ragged columns.)
- **Scale (Tailwind tokens):** body & **inputs 16px** (`text-base`, keeps forms legible and
  avoids iOS zoom-on-focus); dense table cells & meta **14px** (`text-sm`); section/page
  headings `text-lg`→`text-2xl`; the dashboard **P&L figure `text-3xl`/`text-4xl`** (the one
  size emphasis in an otherwise flat scale). Secondary labels `text-xs` (12px) sparingly.
- **Weights:** 400 body; **600** for headings, KPI figures and table totals; 500 for subtle
  emphasis. No italics for data.
- **Line length:** body/help text capped ~70ch (`max-w-prose`); most of the app is tabular,
  not prose.
- **Why:** zero hosting + fast load (DS-1); tabular figures are the single typographic move
  that makes a money app readable.
- **Serves:** REQ-016 (readable P&L/tables), REQ-024a (English-only, no non-Latin shaping
  needed), REQ-022/REQ-026.

### DS-4 — Amount display convention · 2026-10-17

- **Grouping (user-confirmed):** **Indian lakh/crore grouping** — `₹1,25,000`, `₹1,24,500`
  — matching how the farm reads numbers locally.
- **Negatives:** **accounting parentheses**, `(₹2,000)`, rendered in `expense` red. The
  parentheses are a non-color cue, so the sign survives grayscale printing (DS-2 rule 2).
  (Rejected: international grouping — not how local records are written; minus-sign
  negatives — owner preferred parentheses.)
- **Positives are unsigned:** positive values show **no `+` sign** (`₹1,24,500`); only
  negatives are marked, by parentheses. (The parentheses + Income/Expense labels still satisfy
  the not-color-alone rule.)
- **Decimals:** **2 decimals** (paise) in amounts, table cells and totals; the large
  dashboard **KPI figure may round to whole** rupees.
- **Abbreviation:** **lakh/crore short form (₹3.1L, ₹2.4Cr) only on compact KPI tiles** where
  space is tight; the **full grouped value** is used everywhere else (tables, detail, print)
  and should remain available (e.g. tooltip/title) on abbreviated tiles.
- **Scope of parentheses:** applies to **signed/net money values** (e.g. a net-P&L loss
  `(₹2,000)`). In ledgers the **Income/Expense column or label** carries direction, so line
  items need not be parenthesised. **Stock shortfall** (UX-11) is shown in **words/number**
  ("Short 120 nut"), not money parentheses.
- **Why:** local number habits reduce misreads for the farmer/family; parentheses + labels
  keep meaning legible without color (DS-2).
- **Serves:** REQ-016 (P&L/turnover figures), SD-7 (printed reports), REQ-013, UX-11.

### DS-5 — Shape, density & components · 2026-10-17

- **Baseline (user-confirmed): soft-standard, comfortable** — `rounded-md` (~6px) corners,
  subtle `slate-200` borders, white surfaces on a `slate-50` background, roomy-but-efficient
  padding, **44px minimum tap targets**, **borders over shadows** (one soft shadow reserved
  for menus/overlays). Friendly on a phone for non-technical users, dense enough for laptop
  tables. (Rejected: compact/dense — cramped tap targets on phone; boxy/flat — square
  controls feel harsh and less tappable on mobile.)
- **Icons: Lucide** (MIT, self-hostable line set), ~20px, **always paired with a text
  label** (no icon-only controls except the few that are unambiguous, e.g. close "×").
- **Core components (conventions, Tailwind — not code):**
  - **Buttons** — primary `bg-blue-600 text-white rounded-md`, 44px tall, `px-4`,
    full-width on phone; **secondary** white + `slate-300` border; **ghost** text-only;
    **destructive** `red-600`. One primary action per screen.
  - **Inputs** — 44px tall, `rounded-md border-slate-300`, **16px** text, `blue-500` focus
    ring, **label above** the field. (Field-level rules/validation = 4c.)
  - **Payment toggle (UX-7)** — a **segmented control** Paid / Partial / Credit; selected =
    filled blue, rest outline.
  - **Tables → cards (key responsive move, DS-6)** — **laptop:** ruled table (`slate-200`
    row dividers, `slate-50` sticky header, **bold totals row**, amounts right-aligned
    `tabular-nums`); **phone:** each row collapses to a **stacked card** (primary fields +
    the amount prominent). Same data, two layouts.
  - **KPI / stat tiles (dashboard, UX-1)** — white card: `slate-500` `text-sm` label +
    big `text-3xl/4xl` `tabular-nums` figure; net P&L figure colored `income`/`expense`;
    may abbreviate per DS-4.
  - **Badges / pills** — `rounded-full`, `text-xs`, **always worded**; each pill = the
    token's **light tint background + dark shade text** (Paid green-100/green-700 · Partial
    amber-200/amber-900 · Credit red-100/red-700 · In-house slate-100/slate-700 · Outsourced
    sky-100/sky-700 · Short 120 nut red-100/red-700). Never a bare colored dot. (The
    `amber-500` in DS-2 is the token's base color; the Partial pill uses its light tint.)
  - **Entry panels (UX-5/7)** — repeatable input/output rows add via HTMX; a sticky
    summary/tally and the primary action pinned at the bottom (reachable on phone).
  - **Empty states** — Lucide icon + one plain line + the primary action
    ("No sales yet. Record your first sale.").
  - **Error states** — inline `red-600` text that says what went wrong and how to fix it;
    field errors below the field; a simple retry for load failures. Interface voice, not an
    apology (per frontend-design writing guidance).
- **Why:** stock Tailwind utilities + one comfortable baseline = fast to build (DS-1),
  consistent, and legible/tappable on phone and laptop alike.
- **Serves:** every v1 screen (UX-1..UX-11); REQ-022 (responsive), REQ-011/008 (entry
  panels), REQ-016 (tables/tiles), REQ-013/036/UX-11 (badges).

### DS-6 — Responsive & print conventions · 2026-10-17

- **Mobile-first Tailwind.** Breakpoints `sm/md/lg`; **`md` (~768px)** is the switch point
  for table↔card and 1-col↔multi-col.
- **Laptop `/`** — top nav bar (UX-1), multi-column where useful, ruled tables; collapses to
  a stacked/hamburger nav below `md`.
- **Phone `/m/`** — single column, 16px inputs, 44px targets, tables as **stacked cards**
  (DS-5), primary action **pinned at the bottom**.
- **Phone navigation (user-confirmed): hub-and-back.** The `/m/` home **is** the hub (big
  action buttons + Today card, UX-2); tapping an action opens a **full-screen form**, saving
  **returns to the hub** (UX-3); the back button navigates. **No persistent tab bar** —
  least chrome, fastest, matches the 5-item subset and the Capacitor APK wrapper (SD-3).
  (Rejected: bottom tab bar — more native-app chrome than the small subset needs; duplicates
  the hub.)
- **Print (SD-7, `@media print`):** hide nav/buttons/chrome; **black-on-white, no background
  fills** (ink-saving); header repeats **farm name + report title + period +
  generated-on date**; **bold totals**; repeat table headers; avoid page-breaks inside rows;
  negatives read via **parentheses** (DS-4), so grayscale print stays unambiguous.
- **Capacitor/APK fit (owner's steer):** the pinned bottom primary action must clear the
  device **safe-area inset** (`viewport-fit=cover` + `env(safe-area-inset-bottom)`) and stay
  **above the on-screen keyboard**; v2 APK maps the **Android hardware back button to
  history-back** (consistent with hub-and-back). Lucide is used as **inline SVG / sprite**,
  **not** its JS runtime (speed, DS-1).
- **Quality floor:** visible keyboard focus (`blue-500` ring), `prefers-reduced-motion`
  respected (motion is minimal anyway, DS-1), AA contrast (DS-2).
- **Why:** one mobile-first system serves `/`, `/m/` and the APK from the same templates
  (SD-2/SD-3); print rules make the browser-Save-as-PDF reports (SD-7) clean and shareable.
- **Serves:** REQ-022 (laptop + phone + APK), SD-3 (`/m/`/APK), SD-7 (printable reports),
  REQ-016 (reports), REQ-024a.

### DS specimen · 2026-10-17

Build reference showing the palette tokens, type scale, KPI tiles, buttons, worded badges
and a ruled ledger table (with a parenthesised negative + Net):
**`docs/requirements/farmOS-v1-design-system.svg`**. (Plain/Tailwind-default direction per
DS-1 — no Excalidraw checkpoint needed; authored as a static SVG.)

---

## Detailed data & forms

> Phase 4c (`/design-data`) — **confirmed 2026-10-17** (DD-0..DD-9; Phase 4c sub-gate ✅).
> Field-level design for the v1 screens on the
> finalized domain model (`ARCHITECTURE-v1.md` §2) and service layer. Decision IDs **DD-n**.
> No stack/domain-model redesign (gaps are surfaced under *Architecture follow-ups*, not
> silently changed); no component build or app code.

### DD-0 — Global form conventions (every form inherits) · 2026-10-17

- **Precision:** money `Decimal(12,2)`; quantity `Decimal(12,3)` (fractional kg/L). Never float.
- **Number inputs:** entered **positive**; direction comes from the toggle / movement reason,
  never a typed sign. `inputmode="decimal"`, accept typing without grouping commas; **display**
  per DS-4 (Indian grouping, parentheses for negatives, unsigned positives, 2dp money).
- **Units:** **display-only**, read from `Item.unit`, shown beside every quantity field. No
  unit conversion in v1; the quantity field is never free-text unit.
- **Dates:** default **today** (Asia/Kolkata, `USE_TZ`); **back-dating allowed** (catch-up
  entry); **future dates blocked**.
- **Negative stock:** **warn, don't block** (SA-4/UX-11) — an **inline warning** on the line
  before save ("This takes OIL-261016 to (8 L) short"); the posting proceeds. **No confirm modal.**
- **Double-submit guard:** `hx-disabled-elt` on the submit control + a **server-side one-time
  token**, so a double-tap on a phone can't record two sales/postings.
- **Errors:** a validation failure **re-renders the form partial (HTMX)** with messages
  beside each field; a failed request shows "Couldn't save — check your connection and try
  again." (interface voice, per DS-5).
- **Edit/delete visibility (SA-3):** a record's **Edit/Delete shows only if `created_by` ==
  current user, or the user is admin.** *Consequence (surfaced): one family member cannot
  edit another's record; admin can edit anyone's.*
- **Correction policy (SA-4):** editing a record **atomically re-posts** its linked
  `StockMovement` + `Transaction` (auditlog keeps before/after). Once a batch has **downstream
  movements**, its **item & batch are locked** on the source event; **quantity / price / date
  stay editable**. Deletes are **PROTECT**ed → message: "Can't delete — COCO-261016 is used in
  3 sales and 1 run. Edit the quantity instead." Lookups archive (`is_active=false`), never delete.

### DD-1 — Harvest form → `record_harvest` · 2026-10-17 (REQ-034)

| Field | Model attr | Req | Default | Validation |
|---|---|---|---|---|
| Date | `Harvest.date` | req | today | ≤ today |
| Source entity | `Harvest.entity` FK | opt* | — | *at least one of entity / plantation |
| Source plantation | `Harvest.plantation` FK | opt* | — | *(see above) |
| Item (raw) | `Harvest.item` FK | req | — | active `Item` |
| Quantity | `Harvest.quantity` | req | — | > 0; `Decimal(12,3)`; unit from `Item.unit` |
| Batch no. | `Batch.number` | req | auto `<ITEMCODE><YYMMDD>` (UX-4) | unique; editable; `-2` suffix on same-item-same-day collision |

- **Service:** `record_harvest` (atomic: opens `Batch` `origin=in_house` + positive
  `StockMovement` reason=harvest). **HTMX:** batch-no regenerates when item/date change.
  **Empty state** (no items): "Add items in Admin first."

### DD-2 — Production run form → `run_production` · 2026-10-17 (REQ-007/008/009)

Repeatable **Input lines (≥1)** and **Output lines (≥1)**; each line:

| Line field | Model attr | Req | Validation |
|---|---|---|---|
| Item | `ProductionLine.item` FK | req | input: any active item; output: **recipe outputs listed first, but any item allowed** (UX-5) |
| Batch | `ProductionLine.batch` FK | req | input: existing batch of that item (shows stock; negative warns); output: new auto `<ITEMCODE><YYMMDD>` or pick existing |
| Quantity | `ProductionLine.quantity` | req | > 0; `Decimal(12,3)` |

Run-level: **Date** (`ProductionRun.date`, req, today, ≤ today); **Output origin**
(`Batch.origin`, req, **default inherited** = outsourced if any input batch outsourced else
in_house, **user-editable**).

- **Rules:** ≥1 input & ≥1 output; **output item may equal input item** (= repack); **tally
  is a reconciliation summary, not quantity-equality** (UX-5). **Service:** `run_production`
  (atomic: one `StockMovement` per line, production-in / production-out). **HTMX:** add/remove
  rows; recipe filter on input choice; **live tally**; output batch-no regenerates.

### DD-3 — Procurement form → `procure` · 2026-10-17 (REQ-036)

| Field | Model attr | Req | Default | Validation |
|---|---|---|---|---|
| Item | `Procurement.item` FK | req | — | active |
| Vendor | `Procurement.vendor` (Contact type=vendor) | **req** | — | must be a vendor contact; **inline add-vendor** |
| Quantity | `Procurement.quantity` | req | — | > 0; `Decimal(12,3)`; unit from `Item.unit` |
| Cost (₹) | expense `Transaction.amount` | req | — | ≥ 0; `Decimal(12,2)` |
| Date | `Procurement.date` | req | today | ≤ today |
| Batch | `Batch` (`origin=outsourced`) | req | **new** auto `<ITEMCODE><YYMMDD>`, or **pick existing open outsourced batch** (UX-6) | "open" = outsourced batches of same item, most-recent first |

- **Service:** `procure` (atomic: outsourced `Batch` + positive `StockMovement`
  reason=purchase + **expense `Transaction`** linked to vendor). On save, optionally add the
  vendor to `Item.vendors` if not linked (UX-6).

### DD-4 — Quick sale form → `record_sale` · 2026-10-17 (REQ-011/013/032)

| Field | Model attr | Req | Default | Validation |
|---|---|---|---|---|
| Item | `Sale.item` FK | req | — | active, sellable |
| Batch | `Sale.batch` FK | req | — | existing batch of item; shows stock (negative warns); **empty state** "Record a harvest or procurement first" |
| Quantity | `Sale.quantity` | req | — | > 0; `Decimal(12,3)` |
| Price (₹/unit) | `Sale.unit_price` (snapshot) | req | from `Item.sale_price`, editable | ≥ 0; `Decimal(12,2)` |
| Contact | `Sale.contact` FK | **req — all sales** (user choice) | — | **inline add-contact from the sale page** (user note) |
| Payment | Paid / Partial / Credit toggle (UX-7) | req | Paid | — |
| Received (₹) | initial `Payment.amount` | cond | Paid→total · Credit→0 · Partial→enter | **0 ≤ received ≤ total (no overpay)** |

- **Service:** `record_sale` (atomic: `Sale` + price snapshot + negative `StockMovement`
  reason=sale + income `Transaction` **accrual** + **initial `Payment` row** when received > 0).
  **HTMX:** price autofills on item; line total computes live; Received field reveals on
  Partial; Outstanding shows live. **Scope guard:** one item · one batch · one contact (v1).

### DD-5 — Expense / Income form → `record_transaction`* · 2026-10-17 (REQ-002/005/031/017)

| Field | Model attr | Req | Default | Validation |
|---|---|---|---|---|
| Direction | `Transaction.direction` | req | Expense | income \| expense |
| Amount (₹) | `Transaction.amount` | req | — | > 0; `Decimal(12,2)` |
| Date | `Transaction.txn_date` | req | today | ≤ today |
| Overhead | `Transaction.is_overhead` | opt | off | **on → Entity disabled/cleared** (REQ-031) |
| Entity | `Transaction.entity` FK | opt | — | disabled when Overhead on |
| Batch / Item / Stage / Plantation / Contact | FKs | opt | — | all optional (UX-8: all visible) |
| Tags | `Transaction.tags` M:N | opt | — | — |
| Note | `Transaction.note`† | opt | — | — |

- **Service:** `record_transaction`* (**to add — flagged**; atomic single-row audited create,
  same pattern as the others). Reachable on `/m/` (UX-2).

### DD-6 — Collect payment (on Sale detail) → `record_payment`* · 2026-10-17 (REQ-013)

| Field | Model attr | Req | Default | Validation |
|---|---|---|---|---|
| Amount (₹) | `Payment.amount` | req | current outstanding | **0 < amount ≤ outstanding (capped)** |
| Date | `Payment.date` | req | today | ≤ today |

- **Service:** `record_payment`* (**to add — flagged**; atomic `Payment` insert; outstanding
  recomputed). Per-sale (UX-9); `/m/` "Collect pay" lists outstanding sales → opens the sale → add payment.

### DD-7 — Contact form (inline / `/admin/`) · 2026-10-17 (REQ-014/033)

| Field | Model attr | Req | Default | Validation |
|---|---|---|---|---|
| Name | `Contact.name`† | req | — | — |
| Type | `Contact.type` | req | customer | customer \| visitor \| vendor |
| Phone | `Contact.phone`† | opt (recommended) | — | **warn on duplicate phone**; needed for REQ-015 WhatsApp |
| Tags | `Contact.tags` M:N | opt | — | — |
| Notes | `Contact.notes`† | opt | — | — |

### DD-8 — Reports filter · 2026-10-17 (REQ-016)

| Field | Req | Default | Validation |
|---|---|---|---|
| Period | req | This month | This month / This FY-season / Custom |
| Custom from–to | cond | — | required if Custom; **from ≤ to** |
| Scope | req | Whole-farm | Whole-farm / Per-batch |

- Reads the `Transaction` ledger (filter `txn_date`); per-batch adds descendant roll-up
  (OD-5); print per DS-6 (SD-7).

### DD-9 — Admin forms + Stock adjustment · 2026-10-17 (REQ-004, SA-4)

- **`/admin/` (Django admin):** EntityCategory, Stage, Plantation, Tag, **Item** (incl.
  `code`, `unit`, `sale_price`, `vendors`), **Entity** (incl. optional `code`, `count`),
  Contact, FarmProfile, Users/roles, **Recipe** config. `Transaction` & `StockMovement`
  **read-only** (SA-1).
- **Stock adjustment (user-confirmed):** an **admin-only "Adjust stock" action on the Batch
  detail page** → `adjust_stock(batch, ±qty, note)`* service posting an audited `adjustment`
  `StockMovement`. Fields: **signed quantity** (req), **note/reason** (req). Records
  spoilage / breakage / count corrections cleanly.

### Architecture follow-ups (Phase 5 / Build) — surfaced, not changed here

> These extend the finalized `ARCHITECTURE-v1.md` (not edited per command). Carry into
> `DESIGN-v1.md` open questions and resolve at Build.

- **New service functions:** `record_transaction` (expense/income, DD-5), `record_payment`
  (collect payment, DD-6), `adjust_stock` (admin stock correction, DD-9) — each atomic +
  audited (SA-1 pattern).
- **`record_sale` extension:** accept the **received amount** and create the **initial
  `Payment` row** (DD-4/UX-7) — current spec lists only Sale+StockMovement+Transaction.
- **Model field additions:** `Item.code` (**req, unique, uppercase A–Z/0–9, 2–8 chars**),
  `Entity.code` (**optional**, no v1 function); `Contact.name` / `Contact.phone` /
  `Contact.notes`; `Transaction.note`; `Batch.origin` **editable on a production run**
  (default inherited, DD-2). († marks fields not explicit in the current domain model.)
- **"Open outsourced batch"** (UX-6/DD-3) defined as *outsourced batches of the same item,
  most-recent first* — a query, **no status field added**.
- **Edit/delete gating** by `created_by`/admin (DD-0) — family members can't edit each
  other's records; confirm this is acceptable at Build.
