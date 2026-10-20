# farmOS — Architecture Decisions (Phase 3 working log)

> Dated decisions for Phase 3. Each entry records **what** was chosen, **why**, the
> **REQ/OD** it satisfies, and the **alternatives rejected**. Scope is **v1 only**.
> This is the working log; `/arch-finalize` consolidates it into `ARCHITECTURE-v1.md`.
>
> Sections: `## Stack` (3a), `## Domain model` (3b), `## System architecture` (3c).

---

## Stack

> Phase 3a — tech-stack selection. Driven by the v1 NFRs: self-hosted on the owner's
> VPS + **Coolify**, **Coolify-bundled PostgreSQL**, responsive web, English-only,
> single-farm-per-install, no paid third-party services, no offline, no hardware/IoT.

### SD-1 — Backend framework: **Django (5.2 LTS line)** · 2026-10-14

- **Chosen:** Python + **Django**, on the **5.2 LTS** release line (LTS supported to ~2028),
  Python 3.12+. (Version to be pinned at build time.)
- **Why:** For a solo owner maintaining a data-heavy CRUD app, Django's batteries-included
  design removes the most code:
  - **REQ-004** (admin edits categories/types/statuses/stages/tags) — Django's built-in
    admin covers most of this out of the box.
  - **REQ-032** (admin-editable price catalog) — admin again.
  - **REQ-021** (fixed roles: admin vs owner/family) — Django auth + groups/permissions.
  - **REQ-027** (audit logging, timestamps, who) — mature package (django-auditlog or
    django-simple-history) rather than hand-rolled.
  - First-class **PostgreSQL** support (REQ-026).
  - Honours the owner's stated lean to **Python + self-hosted**.
- **Satisfies:** REQ-004, REQ-021, REQ-027, REQ-032, REQ-026 (Python/self-hosted lean).
- **Rejected:** **FastAPI** — API-only; no built-in admin/auth/ORM, so REQ-004/021/027
  would all be hand-assembled plus a separate frontend = more to build/maintain for one
  owner. **Flask** — micro-framework; the most custom plumbing (ORM, admin, auth,
  migrations) of the three, little of REQ-004/021/027 for free.

### SD-2 — Frontend approach: **Django templates + HTMX + Alpine.js** · 2026-10-14

- **Chosen:** Server-rendered **Django templates**, with **HTMX** for dynamic partial
  updates (inline edits, live P&L/turnover totals, inventory tally, quick-sale entry) and
  **Alpine.js** for small client-side interactions. Responsive layout via CSS utility
  framework (**Tailwind** as the working default — a minor sub-choice, flag if you'd
  rather use plain CSS). No separate SPA, no JS build pipeline beyond CSS tooling, no API
  contract to keep in sync.
- **Why:** One owner maintains the app; a single Django deployable in mostly one language
  is the lowest-maintenance way to meet **REQ-022** (responsive web, laptop + phone
  browser). HTMX gives the "app-like" partial-update feel the data-entry flows (REQ-011
  quick sale, REQ-008 production tally, REQ-016 live reports) benefit from, without a
  second codebase.
- **Satisfies:** REQ-022 (responsive web); supports REQ-011/008/016 interactivity.
- **Rejected:** **SPA (React/Vue) + DRF API** — richest interactivity but two codebases,
  JS build pipeline, API contract and cross-boundary auth = far more surface area for a
  solo owner in v1 (revisit only if a native app sharing the API is committed).
  **Templates only, no JS** — fewest parts but clunky full-page reloads for quick-sale /
  live-totals / tally flows; HTMX can always be dropped in later, so no reason not to
  start with it.

### SD-3 — Mobile/APK path: **Capacitor WebView over a curated `/m/` family subset** · 2026-10-14

- **Chosen:** The future APK (v2) is a thin **Capacitor remote-URL WebView wrapper** that
  loads a **curated, phone-first subset of flows served by the same Django app** — a
  dedicated `/m/` route group aimed at the owner/family role (REQ-021), exposing only the
  family's most-used tasks (e.g. log a quick sale, record income/expense, add a
  visitor/contact, check today's P&L/turnover) — **not** the full web surface (no admin,
  catalog editing, production/tally, full reports) and **not** a separate codebase.
- **Why:** The owner wants the family app to carry only a few key features, not the whole
  web app. With the SD-2 server-rendered + HTMX stack, a `/m/` subset lives in the one
  Django codebase (single source of truth) and the APK simply packages that entry point.
  This confirms the v1 responsive-web choice keeps the APK path open (what REQ-022 asked
  Phase 3 to settle) at zero extra v1 cost beyond keeping the mobile subset in mind.
- **Scope:** Actual APK build remains **v2**. v1 only keeps the path open; the `/m/`
  subset need not be built in v1 but the frontend is structured so it can be.
- **Satisfies:** REQ-022 (confirms APK approach), aligned with REQ-021 (owner/family role),
  REQ-023 (no offline — WebView loads the live app).
- **Rejected:** **Bundled-assets Capacitor/SPA app** — could show a few screens but is a
  second codebase to maintain = rejected for a solo owner. **WebView over the full web
  app** — dumps the entire surface onto the phone, opposite of the owner's goal.
  **Defer entirely** — REQ-022 explicitly asked to confirm the approach now.

### SD-4 — Data access, auth & audit logging (Django defaults) · 2026-10-14

- **Chosen (three, all following from SD-1):**
  1. **Data access:** Django **ORM** + built-in **migrations**.
  2. **Auth:** Django's built-in **session authentication** with **groups/permissions**
     for the fixed role set (admin vs owner/family). Self-hosted, no paid service.
  3. **Audit logging:** **django-auditlog** for automatic per-record change history
     (what/when/who).
- **Why:** All first-party or mature Django packages, lowest-maintenance for a solo owner,
  zero third-party cost. Session auth suits a server-rendered app (SD-2); JWT/token auth
  would only be warranted by a separate SPA/mobile client, which SD-2/SD-3 avoid.
- **Satisfies:** REQ-021 (fixed roles via groups), REQ-027 (audit trail),
  REQ-026 (no paid third-party auth — rules out Auth0/Clerk etc.).
- **Rejected:** Token/JWT auth (no SPA to justify the boundary); django-simple-history
  (full-row versioning is heavier than the change-event log REQ-027 calls for — revisit
  only if full point-in-time row history is later required); any paid/hosted auth
  (violates REQ-026).

### SD-5 — Deployment on Coolify: **committed Dockerfile** · 2026-10-14

- **Chosen:** A **committed Dockerfile** that Coolify builds, with the standard production
  setup:
  - **gunicorn** as the WSGI app server.
  - **WhiteNoise** for serving static/CSS assets (no separate nginx/web server to run).
  - The app gets its **own database + user** on the **Coolify-bundled PostgreSQL**
    instance (the instance is shared "for now" per REQ-026, but farmOS owns a dedicated
    db/user within it).
  - Env vars / secrets managed via Coolify.
  - **Backups:** Coolify's PostgreSQL backups to a **local/VPS (owner-owned) destination**
    by default to stay within REQ-026 (no paid third-party). S3-compatible off-site backup
    is optional later only if it uses the owner's own/free storage.
- **Why:** An explicit Dockerfile is reproducible and fully under the owner's control, and
  is needed anyway if a system library is added later (e.g. PDF export deps — see SD-7).
  Satisfies the self-hosted-on-Coolify + bundled-PostgreSQL constraint directly.
- **Satisfies:** REQ-026 (self-hosted on owner's VPS + Coolify, bundled PostgreSQL, own
  domain, no paid third-party), REQ-023 (cloud-hosted), REQ-030 (single-farm install).
- **Rejected:** **Nixpacks auto-build** — less image control and awkward to add OS-level
  system libraries (would likely force a Dockerfile switch later anyway, e.g. for PDF).

### SD-6 — Background jobs: **none in v1** · 2026-10-14

- **Chosen:** **No Celery, no Redis.** Everything runs synchronously within the request
  cycle (reports/exports generated on demand).
- **Why:** Nothing in v1 scope needs to run outside the request: single farm, manual data
  entry, on-request reports, manual WhatsApp send (REQ-015), integrations deferred
  (REQ-028), scheduled tasks deferred (REQ-020). Avoids an extra service + broker to
  deploy/maintain on Coolify and the associated cost/complexity.
- **Satisfies:** keeps v1 within REQ-026 (minimal infra, no paid services) and simplifies
  SD-5 deployment.
- **Rejected:** **Celery + Redis now** — no v1 workload justifies it; add a worker later
  only when v2 integrations (REQ-028), scheduling (REQ-020), or heavy async exports arrive.

### SD-7 — Report/document export: **browser print / Save-as-PDF** · 2026-10-14

- **Chosen:** **Print-optimized CSS**; the user prints or uses the browser's own
  **Save-as-PDF** for the P&L/turnover report (REQ-016) and the price list / order
  confirmation (REQ-015). **No server-side PDF library in v1** — nothing extra added to
  the Docker image.
- **Why:** Lightest option, zero new dependencies or system libraries, no paid services —
  fully within REQ-026. Meets REQ-016's printable/exportable intent with client-side
  tooling at single-farm scale.
- **Satisfies:** REQ-016 (printable/exportable/shareable), REQ-015 (price list / order
  confirmation document), REQ-026 (no added cost/dependency).
- **Note / upgrade path:** The SD-5 Dockerfile makes it easy to add **WeasyPrint**
  (server-side HTML→PDF) later if the browser-save flow proves clunky on phones for the
  family, or when a more controlled, uniform shareable document is wanted.
- **Rejected (for v1):** **WeasyPrint server-side PDF** — cleaner/uniform output and easier
  phone sharing, but adds system libraries now; deferred as the upgrade path above.
  **PDF + XLSX export** — raw-data spreadsheet export is beyond REQ-016's v1 ask; revisit
  if raw-data export is wanted later.

---

## Domain model

> Phase 3b (`/arch-model`) — confirmed 2026-10-14. v1-only data/domain model for the
> Django ORM + PostgreSQL stack (SD-1/SD-4). Entities below are described as tables +
> fields + relationships; no ORM classes or migrations (those are Build phase).
> **ER diagram:** Excalidraw checkpoint `6a28140651434bf696` (current, incl. REQ-036);
> canonical image files `docs/requirements/farmOS-v1-domain-ER.svg` + `.png` (Procurement,
> Batch.origin, Item–vendors, `purchase` stock reason). Prior checkpoint
> `7bfb393e3cc44189b2` = pre-REQ-036 sketch (superseded).

### Resolved open decisions

- **OD-1 — RESOLVED:** **One `Entity` table** with an FK to an admin-editable
  `EntityCategory` lookup, plus an optional `count`. **Not** table-per-category — new
  categories must be addable at runtime (REQ-004) and DB tables can't be created at
  runtime.
- **OD-3 — RESOLVED (confirmed):** Quick sale **deducts stock on save** (immediate).
  Inventory is a **`StockMovement` ledger** (source of truth); current stock = sum of
  movements per item per batch. v2 order workflow hook: orders will simply post a stock
  movement at whatever status is chosen then — no model change needed.
- **OD-5 — RESOLVED (confirmed + extended):** v1 per-batch P&L = **direct-tag only**
  (no raw-material cost splitting across branched outputs, no overhead allocation —
  deferred). **Extension:** viewing a batch **rolls up** income/expense tagged to its
  **descendant batches** (aggregation up the lineage tree, e.g. harvest → pulp → oil →
  soap). Roll-up is summation, not cost allocation, so it does not conflict with
  direct-tag-only.
- **Income recognition — DECIDED (new, was unspecified):** **Accrual** — income counts at
  **sale time**, regardless of when cash is received. Outstanding is tracked via
  `Payment` rows; payments move the outstanding balance, not P&L. Drives all REQ-016
  P&L/turnover numbers.
- **Default stages (seed):** **preparation → growing → production → marketing**; the
  `Stage` lookup is admin-editable (REQ-004/005), so stages can be added/renamed/removed.

### Entities (tables), grouped

**Identity & lookups**
- **`FarmProfile`** (REQ-003) — **single row**: name/label, logo (uploaded media),
  bio, land size, plot/area structure, tree/stock counts, **`fiscal_year_start_month`**
  (added 3c — India FY = April, disambiguates REQ-016 "yearly/seasonal"). (No per-table
  `farm_id`; REQ-030 single-farm — true multi-tenancy is a noted *later* seam.)
- **`EntityCategory`** (REQ-001/004) — admin-editable: living stock, buildings,
  machinery/tools, land, employees, …
- **`Stage`** (REQ-005/004) — admin-editable lookup; seed = preparation/growing/
  production/marketing.
- **`Plantation`** (REQ-019 tag capture in v1; rollup report is v2) — admin-editable
  grouping/project tag.
- **`Tag`** — generic admin-editable labels (M:N to Transaction, and to Contact).

**Entities & money ledger**
- **`Entity`** (REQ-001/002) — FK→`EntityCategory`, name, optional `count`, `is_active`.
  Carries both income & expense purely via `Transaction` rows (category never restricts
  direction).
- **`Transaction`** (REQ-002/005/017/031) — **single ledger table**:
  `direction` (income|expense), `amount` (**Decimal**, positive), `txn_date` (economic
  date reports filter on, separate from `created_at`), `is_overhead` flag (REQ-031).
  Nullable attribution FKs: `entity`, `batch`, `item`, `contact`, `stage`, `plantation`;
  `tags` M:N. Full attribution captured in v1 even where the matching report is v2
  (REQ-017).

**Inventory, production & batches**
- **`Item`** (REQ-006/032) — one table for **raw + finished** goods (an output can be a
  later input). Fields: name, own `unit`, optional admin-editable `sale_price`,
  `is_active`. Quantities are **Decimal**.
- **`Batch`** (REQ-010) — user-entered unique batch number (may encode name+date);
  lineage via production lines; supports per-batch P&L (direct-tag + descendant roll-up).
- **`Harvest`** (REQ-034) — date, source `Entity`/`Plantation`, `Item` (raw material),
  quantity+unit; **creates the `Batch`** and posts a **positive `StockMovement`**.
- **`StockMovement`** (REQ-008/027, OD-3) — source of truth: `item`, `batch`, `±quantity`,
  `reason` (harvest/production-in/production-out/sale/adjustment), `source` link. Stock
  level = sum of movements (per item, per batch).
- **`Recipe`** (REQ-009) — per-input allowed outputs: `Item → allowed-output Items` (M:N),
  admin-configured. No fixed quantity ratios in v1 (actual quantities entered at run time).
- **`ProductionRun`** + **`ProductionLine`** (REQ-007/008) — a run has **input lines** and
  **output lines**, each carrying `item`, `batch`, `quantity`. Supports multiple input
  batches → one output batch, arbitrary branching depth, and input/output reconciliation
  ("tally"); each line posts the matching `StockMovement`.

**Sales, payments & contacts**
- **`Contact`** (REQ-014/033) — one list; `type`/tag = customer | visitor | vendor
  (admin-editable) + `tags` M:N. Purchase history & outstanding balance are **computed**,
  not stored.
- **`Sale`** (REQ-011) — quick sale; one atomic posting creates: the Sale row (FK
  `contact`, `batch`, `item`, `quantity`, `txn_date`, **price snapshot** copied from
  catalog), a **negative `StockMovement`**, and an **income `Transaction`** (accrual).
- **`Payment`** (REQ-013) — rows linked to a Sale: `amount`, `date`. Outstanding = sale
  total − Σ payments; aggregated per contact.

**Communications & reporting (no new tables)**
- **REQ-015** — app generates price list / order confirmation from `Item` + `Sale`; sent
  manually via WhatsApp.
- **REQ-016 (v1)** — reads the `Transaction` ledger: whole-farm + per-batch P&L/turnover,
  month/year/custom (filter `txn_date`), printable via browser (SD-7). Per-entity/
  product-type/plantation/contact slices are v2, but their attribution FKs exist now.

### Addendum 2026-10-14 — Outsourced goods & procurement (REQ-036)

Reopened a slice of 3b during `/arch-design` to capture buy-in → repack → resell.
**No new kind of thing** — outsourced goods reuse the existing tables; only a flag, a
link, and one event are added:

- **`Item` = the single "ultimate product list"** (raw + finished + vendor goods); product-
  wise stock status is read here (stock = Σ StockMovements per item). An outsourced good is
  an ordinary `Item`, **never** an `Entity` (Entities stay farm-assets-only).
- **`Batch.origin`** = `in_house` | `outsourced` — **authoritative per lot**; because
  sales/stock/transactions reference a batch, the in-house vs outsourced split flows into
  every report and per-batch P&L automatically. (Own produce = `in_house` via Harvest;
  bought-in = `outsourced` via Procurement.) Same `Item` can have both kinds of batch.
- **`Item.vendors`** = **M:N → `Contact`** (type vendor, REQ-033) — standing "suppliers of
  this product" list, for future reference.
- **`Procurement`** (new, lightweight — mirror of `Harvest`): buy qty of an `Item` from a
  vendor → **positive `StockMovement`** (reason=`purchase`) on an `outsourced` `Batch`
  **+** an **expense `Transaction`** linked to the vendor contact. This is the mechanism
  that creates outsourced stock and attaches its cost; resale margin per bought-in batch
  then falls out of normal per-batch P&L.
- **Repack** = existing `ProductionRun` (consume outsourced batch → produce new batch);
  **Resell** = existing `Sale`. No change to those tables.
- **`StockMovement.reason`** gains `purchase` (alongside harvest/production-in/
  production-out/sale/adjustment).

This brings the table count to **18** (adds `Procurement`).

### Cross-cutting rules
- **Money = Decimal**, never float. Quantities = Decimal (kg/litres fractional).
- **Negative stock is ALLOWED** (changed from the initial "block" default at owner's
  request): a negative batch/item balance is a deliberate **"shortfall to procure"**
  signal (how much to buy in from other farmers/suppliers), surfaced in the UI, not a
  blocked action.
- **Audit (REQ-027):** abstract base with `created_at/by`, `updated_at/by`; django-auditlog
  registered on these models (SD-4).
- **History safety (REQ-004):** admin "remove" **archives** (`is_active=false`); FKs from
  historical records (Transaction, StockMovement, Sale) use **PROTECT** so deleting a
  category/stage/entity/item can never break past records.

### v1 → v2 seams (notes only, not built)
- Order workflow (REQ-011b/012) posts StockMovements at chosen status (OD-3 hook).
- Batch P&L cost-allocation (OD-5) replaces/augments direct-tag + roll-up.
- Plantation rollup report (REQ-019), extra REQ-016 report slices — data already captured.
- Multi-tenancy (REQ-030 later) — would introduce a farm scoping key.

---

## System architecture

> Phase 3c (`/arch-design`) — confirmed 2026-10-14. v1-only. Consistent with `## Stack`
> and `## Domain model` above.
> **Architecture diagram:** Excalidraw checkpoint `fa240ccb76f143aa8b`; image files
> `docs/requirements/farmOS-v1-system-architecture.svg` + `.png`.

### SA-1 — Layered architecture + service-layer seam
- **Four layers:** Presentation (templates + HTMX + Alpine, incl. `/m/` phone subset) →
  **Views (thin:** HTTP, forms, permissions, render HTMX partials; **no business logic)** →
  **Service layer** → Data (ORM / PostgreSQL).
- **Service layer is the core rule:** every operational write (`record_sale`,
  `record_harvest`, `run_production`, `procure`, and edit-in-place corrections) is a plain
  Python function wrapped in **`transaction.atomic()`**. It is the single place that keeps
  the multi-row postings consistent (Sale = Sale+StockMovement+Transaction; Harvest =
  Harvest+Batch+StockMovement; ProductionRun = lines+movements; Procurement =
  StockMovement+expense Transaction).
- **Django admin = lookups/catalog/prices/users/FarmProfile only.** `Transaction` and
  `StockMovement` are **read-only in admin** (derived, never hand-edited) so admin can't
  bypass posting logic.
- **No bulk writes on audited models** (auditlog uses signals that `bulk_create`/`.update()`
  skip).
- **Satisfies:** REQ-002/008/010/011/034/036 integrity; REQ-004 (admin).

### SA-2 — "Internal API" = service functions; REQ-028 is an extension
- v1 has **no REST/DRF** (SD-2 rejected an SPA). The internal contract is the
  service-function signatures. URL namespaces reserved: **`/`** (web), **`/m/`** (family
  subset, SD-3), **`/admin/`**, **`/api/`** (reserved for a future `/api/v1/` DRF + token
  auth). Future Telegram/n8n bot and website/CMS feed (REQ-028) call the **same service
  functions** — extension, not rewrite. Shown as **dashed future boxes** in the diagram.

### SA-3 — Auth & roles (REQ-021)
- Django **session auth**; **custom user model** (`AUTH_USER_MODEL`) from day one.
- **Two roles via groups:** **admin** (you) = everything incl. Django admin, catalog,
  prices, user management; **owner/family** = full operational data entry **+ edit/delete
  their records (edit-in-place) + view all P&L/turnover/outstanding reports** (owner's
  choice: full financial visibility). **Employees never log in** (they are Entities).
- Role checks in the **view layer**; `/admin/` staff-only; acting user passed to services so
  **auditlog records who** (via `AuditlogMiddleware`).
- **Password reset = admin-driven in-app**, no email/SMTP dependency (REQ-026). SMTP later
  if the owner's domain provides it.

### SA-4 — Corrections & stock policy
- **Edit-in-place corrections** (owner's choice): editing/deleting a record atomically
  re-computes its linked StockMovement + Transaction; auditlog keeps before/after.
- **Negative stock ALLOWED** — a negative balance is a surfaced **"shortfall to procure"**
  signal (REQ-036), not a blocked action. Admin can post an `adjustment` movement.

### SA-5 — Deployment topology on Coolify (REQ-026)
- **App container** (Dockerfile, SD-5): gunicorn + WhiteNoise (static/CSS); **Tailwind built
  in a Docker build stage** (standalone CLI, no Node runtime). Migrations run at deploy.
  **`/healthz`** endpoint for Coolify. Logs → **stdout** (Coolify captures).
- **PostgreSQL:** Coolify-bundled, farmOS owns a **dedicated db + user**.
- **TLS/domain:** Coolify reverse proxy terminates TLS (Let's Encrypt). Django needs
  **`SECURE_PROXY_SSL_HEADER`** + **`CSRF_TRUSTED_ORIGINS`** set for the domain (else
  "CSRF failed"; HTMX posts send the CSRF header).
- **Media volume:** FarmProfile **logo upload** needs a **persistent volume for
  `MEDIA_ROOT`**, served by the app and **included in backups** (WhiteNoise serves static
  only; PG backup excludes uploads — else logo lost on redeploy).
- **Backups:** PG dump + media volume → **owner-owned storage** (no paid service).
- **Timezone/fiscal year:** `TIME_ZONE=Asia/Kolkata`, `USE_TZ`; **`FarmProfile.
  fiscal_year_start_month`** (India FY = April) disambiguates REQ-016 "yearly/seasonal".

### SA-6 — Audit logging (REQ-027)
- **django-auditlog** registered on operational models; `AuditlogMiddleware` captures the
  actor; services avoid bulk writes so signals fire. Covers edit-in-place history.

### SA-7 — Platform / mobile (REQ-022)
- v1 = **responsive web** (one Django app serves laptop `/` and phone `/m/`). APK is **v2**
  via Capacitor remote-URL WebView over `/m/` (SD-3). No offline (REQ-023).

---

### Addendum 2026-10-17 — Phase 5 build follow-ups (from DESIGN-v1 §5)

> Surfaced during Phase 4 (Design) and confirmed at the start of Phase 5 (Build) via
> `/build-plan`. These **extend** the finalized decisions above — they do not rewrite them.
> Where a point supersedes an earlier reading, it says so explicitly.

**SA-8 — New service functions (same SA-1 pattern: thin view → atomic, audited service).**
The service layer gains three functions alongside `record_sale` / `record_harvest` /
`run_production` / `procure`:
- **`record_transaction`** — posts a standalone expense/income `Transaction` (DD-5). The
  overhead toggle clears the entity attribution. Serves the Record Expense/Income screen
  (REQ-002/005/031/017).
- **`record_payment`** — posts a `Payment` row against a `Sale`, validated `0 < amount ≤
  outstanding` where outstanding = sale total − Σ payments (DD-6, REQ-013).
- **`adjust_stock`** — **admin-only**; posts an audited `StockMovement` with
  `reason=adjustment` (±qty + note) from the Batch detail "Adjust stock" action (DD-9). This
  is the concrete mechanism for SA-4's "admin posts an adjustment movement" (which the
  domain model otherwise left without a screen, since `StockMovement` is read-only in admin).

**SA-9 — `record_sale` extended to capture the initial payment.**
`record_sale` additionally accepts the **received amount** and, within the same
`transaction.atomic()`, creates the **initial `Payment` row** so the Paid/Partial/Credit
state is correct on receipt (DD-4/UX-7). Contact is **required** on every sale (user
decision, 4c), with inline contact-add on the sale page.

**SA-10 — Model field additions (apply in the models + migrations build slices).**
- **`Item.code`** — **required, unique, uppercase A–Z/0–9, 2–8 chars**; drives the auto
  batch number `<ITEMCODE><YYMMDD>` (UX-4/DD-1).
- **`Entity.code`** — **optional**, no v1 behaviour attached (kept for parity/future use).
- **`Contact`** — explicit **`name`**, **`phone`** (warn-on-duplicate for REQ-015), **`notes`**.
- **`Transaction.note`** — free-text note field (DD-5).
- **`Batch.origin`** — remains authoritative, but is **editable on a production run**
  (default inherited from the inputs; repack/outsourced output can differ) (DD-2).

**SA-11 — "Open outsourced batch" is a query, not a status field.**
The procurement "pick an existing open batch" option (DD-3/UX-6) = *outsourced batches of
the same item, most-recent first*. No `status`/`is_open` column is added to `Batch`.

**SA-12 — Edit/delete policy: SHARED FAMILY EDIT (supersedes the per-owner reading).**
User decision 2026-10-17. **Any logged-in owner/family member may edit or delete any
operational record, regardless of who created it** (sale, expense/income, harvest,
production, procurement, payment, contact); **admin** retains full access to everything.
There is **no creator-based gate** on the edit/delete controls for the owner/family group.
This **supersedes** the narrower "edit/delete **their** records" wording in **SA-3** and the
"edit/delete visible only to `created_by` or admin" rule in **DESIGN-v1 DD-0** — the
`created_by`/`updated_by` audit fields are still recorded (SA-6), but they do **not** gate
the controls. Admin-only remains for `/admin/`, catalog/prices/users, and
`adjust_stock` (SA-8). Rationale: a close-knit family doing shared catch-up data entry;
auditlog preserves who-did-what, so shared edit does not lose accountability.
