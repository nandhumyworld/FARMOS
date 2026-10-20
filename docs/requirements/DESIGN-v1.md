# farmOS — Design, v1 (MVP)

> Finalized 2026-10-17 (Phase 4 gate confirmed). Consolidates the Phase 4 working log
> (`30-design-decisions.md`: `## UX & flows` UX-1..11, `## Design system` DS-1..6,
> `## Detailed data & forms` DD-0..9) against `REQUIREMENTS-v1.md` and `ARCHITECTURE-v1.md`.
> **Scope: v1 only.** v2/later items appear only as noted seams.
>
> Reads on the architecture it designs for: service layer `record_sale` / `record_harvest` /
> `run_production` / `procure` / edit-in-place corrections; roles **admin** vs
> **owner/family** (family = full operational access, views all P&L); routes **`/`** (web),
> **`/m/`** (phone-first family subset), **`/admin/`** (Django admin); stack = Django
> templates + HTMX + Alpine + Tailwind (SD-2), responsive (REQ-022), English-only (REQ-024a),
> browser-print reports (SD-7).

---

## 1. UX & flows (Phase 4a)

### 1.1 Screen inventory & navigation (UX-1) — action-first hub
The **Dashboard (`/`)** is the home hub: a row of **verb buttons** for the frequent
captures (**Sell · Record Expense/Income · Harvest · Produce · Procure**) above a **P&L /
turnover / outstanding** snapshot. Browse/registers sit in a secondary top nav.

**12-screen v1 set:** Dashboard/P&L home · Quick Sale · Record Expense/Income · Harvest ·
Production · Procurement · Inventory/Stock (incl. shortfall) · Batches (per-batch P&L) ·
Entities · Contacts · Reports · Admin (link to `/admin/`). Catalog, prices,
categories/stages/tags, users, FarmProfile, Recipe and **Entity/Item creation** live in
**Django `/admin/`** (no custom v1 screens).

### 1.2 `/m/` family subset (UX-2) — capture + customer
Phone-first subset exposes five things: **Sell · Record Expense/Income · Add Contact ·
Collect Payment · a read-only "Today" card** (P&L / turnover / outstanding). `/m/` is **UX
curation, not a permission boundary** (family has full access on `/`); same codebase/services
back both. It is the surface the v2 Capacitor APK (SD-3) will wrap. **Nav = hub-and-back**
(DS-6): home is the hub, an action opens a full-screen form, saving returns to the hub.

### 1.3 Global interaction patterns (UX-3)
- **Edit/correct on the record's detail page** (list row → read-only detail → Edit/Delete;
  Edit reopens the prefilled form). The only shape that fits multi-line records (a run).
- **After save: confirm, then "Add another" / "Done"** — tuned for catch-up data entry.

### 1.4 Core journey flows
| Journey | Shape | Service | Key points |
|---|---|---|---|
| **Harvest** (UX-4) | form → opens batch | `record_harvest` | batch no. auto **`<ITEMCODE><YYMMDD>`**, editable |
| **Production** (UX-5) | single-screen **input/output builder + live tally** | `run_production` | ≥1 in/≥1 out; recipe guides; tally = reconciliation, not qty-equality |
| **Procurement** (UX-6) | own screen; buy-in + vendor expense | `procure` | **new outsourced batch by default, mergeable**; vendor required |
| **Quick sale** (UX-7) | one line; price snapshot + **Paid/Partial/Credit** | `record_sale` | contact required; initial Payment on receipt |
| **Expense/Income** (UX-8) | one form, **all attribution visible** | `record_transaction`* | overhead toggle clears entity |
| **Contacts + payment** (UX-9) | contact detail (history/outstanding); **payment per-sale** | `record_payment`* | outstanding = sale total − Σ payments |
| **Reports** (UX-10) | **one screen**: period + whole-farm/per-batch toggle | — | **browser print / Save-as-PDF** (SD-7); price list on Inventory, order confirmation on sale |
| **Shortfall** (UX-11) | **inline red badges** on Inventory (+ sale batch picker) | — | no dashboard alert, no prefilled procure (v2) |

*`record_transaction` / `record_payment` are Build additions — see §5.

### 1.5 Diagrams
- **Navigation / flow map** — Excalidraw checkpoint **`e456b9e36d7b4b7d8a`**; file
  `farmOS-v1-ux-navigation.svg`.
- **Key screen wireframes** (Quick Sale · Production · `/m/` Home) — checkpoint
  **`ccf74978f59b4220ae`**; file `farmOS-v1-ux-wireframes.svg`.

---

## 2. Design system (Phase 4b)

**Direction (DS-1): Plain & System (low-build, utility-first)** — Tailwind defaults + system
font stack, fast, mobile/Capacitor-ready; speed and legibility over flourish (owner's steer).

- **Color (DS-2):** primary **`blue-600`** (interactive only). Money/status tokens →
  Tailwind shades: `income` green-600, `expense` red-600, `outstanding`/`partial` amber-500
  (fill + dark text), `shortfall` red-600, `in_house` slate chip, `outsourced` sky chip;
  neutrals slate. **Two hard rules:** (1) *usage rule* — blue only on interactive, green/red
  only on money; (2) *not-color-alone* — direction/negatives carry a non-color cue, badges
  always worded.
- **Typography (DS-3):** one **system sans** family; **tabular numerals** on values; scale
  16px body/inputs, `text-sm` tables, `text-3xl/4xl` P&L figure; 400/600 weights.
- **Amount format (DS-4):** **Indian lakh/crore grouping**; negatives in **accounting
  parentheses** (`(₹2,000)`, red); **positives unsigned**; 2 decimals; L/Cr only on KPI tiles.
- **Shape & components (DS-5):** soft-standard — `rounded-md`, 44px tap targets, borders
  over shadows; **Lucide** icons (always with a text label). Buttons (primary blue /
  secondary outline / destructive red), 44px labelled inputs, segmented Paid/Partial/Credit
  toggle, **tables→cards** on phone, KPI tiles, **worded light-tint badges**, empty + error
  states.
- **Responsive & print (DS-6):** mobile-first (`md` switch for table↔card, 1-col↔multi-col);
  laptop `/` top nav; phone `/m/` single column, bottom-pinned action clearing safe-area/
  keyboard; **hub-and-back** nav; Android back → history-back (APK). **Print:** black-on-white,
  no fills, header repeats farm name + report title + period + generated-on date, bold totals.
- **Specimen:** `farmOS-v1-design-system.svg`.

---

## 3. Detailed data & forms (Phase 4c)

### 3.1 Global conventions (DD-0)
Money `Decimal(12,2)`, quantity `Decimal(12,3)`; inputs positive (`inputmode="decimal"`);
units **display-only** from `Item.unit` (no conversion); dates default **today**
(Asia/Kolkata), back-dating allowed, **future blocked**; **negative stock warns inline, never
blocks** (no modal); **double-submit guard** (`hx-disabled-elt` + server one-time token);
validation re-renders the HTMX form partial with inline messages; **edit/delete visible only
to `created_by` or admin** (SA-3); correction **re-posts atomically** (auditlog), item/batch
**lock once downstream movements exist** (qty/price/date stay editable); deletes **PROTECT**ed
with a helpful message; lookups archive, never delete.

### 3.2 Per-form specs (field → model → req → default → validation → service)
Full field tables live in `30-design-decisions.md` `## Detailed data & forms`. Summary:

| DD | Form | Service | Required fields | Notable validation / defaults |
|---|---|---|---|---|
| DD-1 | Harvest | `record_harvest` | date, item, qty, batch no. | ≥1 of entity/plantation; batch auto `<ITEMCODE><YYMMDD>`, unique, `-2` on collision |
| DD-2 | Production | `run_production` | ≥1 input line, ≥1 output line, date, output origin | output item may = input (repack); **origin default-inherited, editable**; recipe guides not constrains; live tally |
| DD-3 | Procurement | `procure` | item, **vendor**, qty, cost, date, batch | vendor = vendor-contact (inline add); new or pick open outsourced batch |
| DD-4 | Quick sale | `record_sale` | item, batch, qty, price, **contact**, payment | price snapshot from catalog (editable); **contact required (inline add on sale page)**; `0 ≤ received ≤ total` |
| DD-5 | Expense/Income | `record_transaction`* | direction, amount, date | all attribution optional (all visible); **Overhead on → Entity cleared** |
| DD-6 | Collect payment | `record_payment`* | amount, date | `0 < amount ≤ outstanding`; per-sale |
| DD-7 | Contact | inline / `/admin/` | name, type | phone warn-on-duplicate (for REQ-015); notes optional |
| DD-8 | Reports filter | — | period, scope | This month default; custom range `from ≤ to` |
| DD-9 | Admin + **Adjust stock** | `adjust_stock`* | signed qty, reason/note | **admin-only** on Batch detail → audited `adjustment` movement |

---

## 4. Screen → requirement / architecture traceability (v1)

| Screen | Serves REQ | Service / tables touched |
|---|---|---|
| Dashboard / P&L home | REQ-016 | reads `Transaction` (P&L/turnover/outstanding) |
| Quick Sale | REQ-011/013/032 | `record_sale` → `Sale` + `StockMovement` + `Transaction` + `Payment` |
| Record Expense/Income | REQ-002/005/031/017 | `record_transaction`* → `Transaction` |
| Harvest | REQ-034/010/006 | `record_harvest` → `Harvest` + `Batch` + `StockMovement` |
| Production | REQ-007/008/009/010 | `run_production` → `ProductionRun`/`Line` + `StockMovement` + `Batch` |
| Procurement | REQ-036/033/002 | `procure` → `Procurement` + `Batch`(outsourced) + `StockMovement` + `Transaction` |
| Inventory / Stock (+shortfall) | REQ-006/032, UX-11 | reads `StockMovement` (stock = Σ), `Item` (price list) |
| Batches (per-batch P&L) | REQ-010 (OD-5) | reads `Batch` lineage + `Transaction`; **Adjust-stock** (`adjust_stock`*) |
| Entities | REQ-001/002 | reads `Entity` + `Transaction` (list/detail; not a per-entity P&L — v2) |
| Contacts (+ collect payment) | REQ-014/033/013 | reads `Contact`; `record_payment`* → `Payment` |
| Reports | REQ-016/015 | reads `Transaction` (whole-farm + per-batch; print SD-7) |
| Admin (`/admin/`) | REQ-004/032/021 | Django admin over lookups/catalog/prices/users/FarmProfile/Recipe |

---

## 5. Open questions / assumptions → Phase 5 (Build)

**Architecture follow-ups (surfaced in 4c; extend `ARCHITECTURE-v1.md`, not yet applied):**
- **New service functions** (each atomic + audited, SA-1 pattern): `record_transaction`
  (expense/income, DD-5), `record_payment` (collect payment, DD-6), `adjust_stock`
  (admin stock correction, DD-9).
- **`record_sale` extension:** accept the **received amount** and create the **initial
  `Payment` row** (DD-4/UX-7).
- **Model field additions:** `Item.code` (**required, unique, uppercase A–Z/0–9, 2–8 chars**;
  drives batch numbers), `Entity.code` (**optional**, no v1 function); `Contact.name` /
  `Contact.phone` / `Contact.notes`; `Transaction.note`; **`Batch.origin` editable on a
  production run** (default inherited, DD-2).
- **"Open outsourced batch"** (DD-3/UX-6) = *outsourced batches of the same item, most-recent
  first* — a query, no status field added.

**Policy to confirm at Build:**
- **Edit/delete is per-owner** (DD-0/SA-3): a family member cannot edit another's record;
  admin can edit anyone's. Confirm acceptable for the farm.
  - **Resolved 2026-10-17 (`/build-plan`) → SHARED FAMILY EDIT (SA-12).** Any owner/family
    user may edit/delete any operational record regardless of creator; admin edits anyone's.
    This **supersedes** the per-owner reading above and DD-0's "`created_by`/admin only"
    gating. `created_by`/`updated_by` are still audited but do not gate the controls.

**Carried from earlier phases (data captured; views are v2):** OD-5 cost-allocation; order
workflow (REQ-011b/012); report slices per-entity/product/plantation/contact (REQ-016
remaining); plantation rollup (REQ-019); visit/enquiry log (REQ-035); WeasyPrint upgrade path
(SD-7); Capacitor APK build (SD-3).

---

## 6. Diagrams index

| Diagram | Phase | Checkpoint | File |
|---|---|---|---|
| Navigation / flow map | 4a | `e456b9e36d7b4b7d8a` | `farmOS-v1-ux-navigation.svg` |
| Key screen wireframes | 4a | `ccf74978f59b4220ae` | `farmOS-v1-ux-wireframes.svg` |
| Design-system specimen | 4b | (static SVG) | `farmOS-v1-design-system.svg` |
