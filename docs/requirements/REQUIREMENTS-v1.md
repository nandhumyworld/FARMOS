# farmOS — Requirements, v1 (MVP)

> Finalized 2026-10-14 (Phase 2 gate confirmed). Source of truth for what v1 builds.
> Derived from `00-big-picture.md` (verbatim story) and `10-requirements-register.md`
> (structured register with per-requirement sources). This document is the human-readable
> v1 scope; the register remains the traceable master.

---

## 1. Purpose & the "why"

The owner runs a **family-run natural-farming** operation (a coconut farm with a farmhouse,
livestock and employees) and today **cannot track money or activity** — income, expenses,
visitors, stock and value-add are all managed "manually and not able to track."

> *"current structure does not allow to note down all the income and expenses… I want
> that to be happen in order to check whether the farm is going on profit or loss…
> the numbers is important."* — Capture 1

> *"many people are coming into farm for visit for inquiry for buying product… we actually
> lose track of those people and also it's a potential customer."* — Capture 1

The intent is a **farm operating system** ("farmOS"): record every rupee in and out against
the thing that earned or cost it, turn raw harvest into value-add products, track each
**batch**'s profit/loss, keep every customer and sale, and know — at any moment —
**profit, loss and turnover**. It is designed **generically** so it can later be handed to
any farmer ("that's why I call this as a farm OS").

**v1 is the lean core that makes the farm genuinely trackable on day one:** entities &
ledgers → harvest → batches → value-add production → quick sale → contacts → whole-farm &
per-batch P&L.

---

## 2. In-scope requirements for v1 (grouped by area)

### 2.1 Farm identity
- **REQ-003** — Farm **portfolio**: name/label, logo, bio, land size, plot/area structure, tree/stock counts.

### 2.2 Entities & ledgers (the money foundation)
- **REQ-001** — Entities organised into **distinct categories** by economic role: living stock (trees, cows, poultry), buildings (farmhouse, godown, cow-shed), machinery/tools, land, and **employees** (employees are entities carrying salary/labour expense — not contacts). v1 entities are **group-level** (e.g. "Coconut trees — North plot ×500") with an optional count.
- **REQ-002** — **Every entity carries both an income and an expense ledger**, regardless of category. Category is a label only — money flows both directions on any entity.
- **REQ-031** — A **general "Farm / overhead" expense bucket** (not tied to an entity) for owner draw, farm maintenance, electricity and other shared cost.

### 2.3 Lifecycle & attribution
- **REQ-005** — **Free ledger with optional stage tags** (growing / production / marketing). Log income/expense whenever it happens; cost-by-stage is derived from tags. Not a forced workflow.
- **REQ-017** — **Every money transaction is richly attributable** — taggable to entity, batch, product, plantation/project, stage, contact and date. Full attribution is captured in v1 even where the matching report is v2, so no data is lost.
- **REQ-027** — **Audit logging**: every record timestamped (what/when; who where applicable).

### 2.4 Harvest, inventory & production (value-add)
- **REQ-034** — **Harvest event** (first-class): date, source entity/plantation, quantity + unit; adds raw-material stock and opens the batch.
- **REQ-006** — **Both raw materials and finished products are inventory** with stock counts; each item defines **its own unit** (count, kg, litres…).
- **REQ-007** — **Multi-level, branching transformation**: raw material → one or more products/byproducts (coconut → husk/shell/pulp), and any output can feed further value-add (pulp → oil → soap).
- **REQ-008** — **Production consumes input stock and yields output stock, reconciled ("tally")**.
- **REQ-009** — **Per-input recipes**: each raw material has its own configurable list of possible output products.
- **REQ-010** — **Batch numbering & traceability** with **per-batch profit/loss**. v1 P&L counts **only income/expense tagged directly to the batch** (cost allocation across outputs/overhead deferred — OD-5).
- **REQ-036** — **Outsourced goods & procurement** *(added in Phase 3, 2026-10-14; see `ARCHITECTURE-v1.md` §2.3)*. Bought-in goods are ordinary **Items** in a **Batch** flagged `origin=outsourced` (own produce = `in_house`), treated as raw materials (sellable or feedable into production). Items carry a **vendor link** (M:N to vendor Contacts). A lightweight **Procurement** event adds outsourced stock + posts a vendor expense. Enables in-house vs outsourced split in reports and resale margin. **Negative stock is allowed** as a procurement signal.

### 2.5 Sales, pricing & payments
- **REQ-032** — **Product pricing / price catalog**: each sellable item carries a current admin-editable sale price.
- **REQ-011** — **Quick sale** (v1 sale mode): one-line "sold X of product from batch B to contact for ₹Y"; inventory drops and income posts immediately; batch link feeds per-batch P&L.
- **REQ-013** — **Payment tracking**: paid-in-full, part-payment/installments, and credit (pay later); amount paid vs outstanding shown; outstanding reportable per contact. (v1 on quick sales.)

### 2.6 Contacts / CRM
- **REQ-014** — **One contact list** for customers/visitors; **auto-built purchase history per contact** and outstanding balance. (Employees are entities; owners/family are app users — not contacts.)
- **REQ-033** — **Vendors/suppliers as a tag/type** within the same contact list; expense entries can optionally link a supplier.

### 2.7 Communications
- **REQ-015** — **In-app compose** (no integration): app generates a formatted **price list** and **order confirmation** (and shows current stock); the user sends them **manually via WhatsApp**.

### 2.8 Reporting (the core benefit)
- **REQ-016 (v1 subset)** — **Profit/loss & turnover** at **whole-farm** and **per-batch** level, for **monthly / yearly-seasonal / custom date range**, **exportable / printable / shareable** as a document. *(Per-entity, per-product-type, per-plantation and per-contact slices are v2.)*

### 2.9 Admin & customization
- **REQ-004** — **Admin can add/edit/remove** categories, types, statuses, stages and tags at any time, so nothing goes uncaptured. (App-user roles are the fixed set in REQ-021.)

---

## 3. Non-functional requirements (v1)

- **REQ-021 — Users & roles:** accounts for **farm owners/family**; at least one **admin**. Employees do **not** log in (owners/family enter data for them). Fixed roles: admin vs owner/family.
- **REQ-022 — Platform:** **responsive web** (admin on laptop, family on phone browser). *(Installable APK via Capacitor is v2.)*
- **REQ-023 — Connectivity:** reliable internet; **cloud-hosted**; **offline not required**.
- **REQ-024a — Language:** **English-only UI**.
- **REQ-026 — Hosting & budget:** self-hosted on owner's **own VPS running Coolify**, own domain, **Coolify-bundled PostgreSQL**; **no paid third-party services in v1**.
- **REQ-030 — Productization:** **single-farm per install**, built generically so it can be handed to another farmer as a fresh install.
- **REQ-025 (v1 part) — Data start:** start **fresh**, no migration of historical operational data.
- **REQ-029 — Hardware:** **no hardware/IoT** integration in scope.

---

## 4. Explicitly out of scope for v1 (deferred — guard against scope creep)

**→ v2**
- **REQ-011b** — Formal **order workflow** with statuses (enquiry → confirmed → packed → delivered → paid).
- **REQ-012** — **Multi-product / multi-batch** orders.
- **REQ-016 (remaining)** — P&L slices **per-entity, per-product-type, per-plantation, per-contact**.
- **REQ-019** — **Plantation/project rollup** reporting.
- **REQ-022 (APK)** — **Capacitor → installable APK**.
- **REQ-025 (import)** — **One-time CSV contact import**.
- **REQ-035** — **Contact visit/enquiry log** for non-buyers.

**→ later**
- **REQ-020** — Tasks, scheduling, calendar, effort tracking.
- **REQ-024b** — Multi-language UI (Tamil, others).
- **REQ-028** — Integrations: Telegram/n8n chatbot, one-click send, public website + CMS, external API (incl. subdomain strategy).
- **REQ-030 (multi-tenant)** — True multi-tenancy (many farms, one deployment).

**n/a** — REQ-029 (hardware/IoT, out of scope); REQ-018 (merged into REQ-016).

---

## 5. Open questions & assumptions (carry into Phase 3 — Architecture)

- **OD-1** — Entities as one table with a `type` field, or separate tables per category — pure design choice; requirement only that categories exist and money flows both ways.
- **OD-3** — Inventory **deduction timing** (at which point stock is drawn down) — matters once the v2 order workflow lands; v1 quick sale deducts immediately.
- **OD-5** — **Batch P&L cost-allocation method** (splitting raw-material cost across branched outputs; allocating shared overhead). v1 = **direct-tag only**; allocation modelling deferred to Phase 3.
- **REQ-022 assumption** — responsive web is sufficient for the family on phones in v1; APK confirmed in Phase 3 before any v2 commitment.
- **REQ-010 assumption** — batch numbers may be user-defined (may encode product name + date); format not fixed.

---

## 6. Context / workflow diagram

An **Excalidraw end-to-end v1 workflow diagram** was generated on 2026-10-14 and rendered
inline in the finalization session. It shows the full flow:

**Operations:** Entities → Harvest → Raw inventory → Production (branching value-add) →
Finished-product inventory → Quick sale → Contact/CRM, with the **batch number propagating
end-to-end** for per-batch P&L, price catalog + payment feeding the sale, and the in-app
price-list → WhatsApp compose.
**Finance & reporting:** every sale/cost/overhead posts to the **Transaction Ledger**
(attributed to entity · batch · product · stage · contact · date), which drives the
**P&L & Turnover reports** (whole-farm + per-batch; month/year/custom; export/print/share).

> Excalidraw renders inline and does not emit a shareable public URL; the diagram's
> restore **checkpoint id is `c7c7a71619bc4e1783`**. Re-run `/req-finalize` (or an
> Excalidraw `restoreCheckpoint`) to redraw or edit it. If a persistent shareable link is
> wanted, say so and I'll reproduce it in Whimsical (which does provide a URL).

<!-- EXCALIDRAW_CHECKPOINT: c7c7a71619bc4e1783 -->
