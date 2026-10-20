# farmOS — Architecture, v1 (MVP)

> Finalized 2026-10-14 (Phase 3 gate confirmed). Consolidates the Phase 3 working log
> (`20-architecture-decisions.md`: `## Stack`, `## Domain model`, `## System architecture`)
> and the v1 scope (`REQUIREMENTS-v1.md` + register `10-requirements-register.md`).
> **Scope: v1 only.** v2/later items appear only as noted seams.

---

## 1. Chosen stack (the "how", tied to NFRs)

| Decision | Choice | Why / NFR satisfied |
|---|---|---|
| **Backend** (SD-1) | **Django** (5.2 LTS line, Python 3.12+) | Built-in admin ≈ REQ-004 (edit categories/stages/tags) + REQ-032 (price catalog); auth+groups = REQ-021 roles; mature audit pkg = REQ-027; first-class PostgreSQL. Honours owner's Python/self-hosted lean. |
| **Frontend** (SD-2) | **Django templates + HTMX + Alpine.js** (Tailwind) | REQ-022 responsive web; one codebase, solo-maintainable; HTMX gives app-like partial updates for quick-sale/tally/live-P&L. |
| **Mobile/APK** (SD-3) | **Capacitor remote-URL WebView over a curated `/m/` family subset** (build = v2) | Confirms REQ-022 APK path without a 2nd codebase; family gets only key flows; no offline (REQ-023). |
| **Data/auth/audit** (SD-4) | **Django ORM + migrations · session auth + groups · django-auditlog** | REQ-021 (roles), REQ-027 (audit), REQ-026 (no paid auth). |
| **Deploy** (SD-5) | **Committed Dockerfile on Coolify** · gunicorn + WhiteNoise · dedicated DB/user on bundled PostgreSQL · backups to owner storage | REQ-026 (self-hosted VPS+Coolify, bundled PG, no paid svc), REQ-023, REQ-030. |
| **Background jobs** (SD-6) | **None in v1** (no Celery/Redis) | Nothing in v1 needs async; minimal infra (REQ-026). |
| **Report export** (SD-7) | **Browser print / Save-as-PDF** (WeasyPrint as later upgrade path) | REQ-016/015 printable/shareable; no added deps (REQ-026). |

---

## 2. Data / domain model

**Source of truth:** `20-architecture-decisions.md` → `## Domain model` (full field lists).
**ER diagram:** Excalidraw checkpoint **`6a28140651434bf696`** (current, incl. REQ-036);
canonical image files `docs/requirements/farmOS-v1-domain-ER.svg` + `.png`.
(Prior checkpoint `7bfb393e3cc44189b2` was the pre-REQ-036 sketch, superseded.)

### 2.1 Resolved open decisions
- **OD-1 → one `Entity` table** + admin-editable `EntityCategory` (table-per-category can't
  satisfy runtime category edits, REQ-004).
- **OD-3 → deduct stock on save**; inventory is a **`StockMovement` ledger** (source of
  truth, stock = Σ movements); v2 order workflow just posts a movement at a chosen status.
- **OD-5 → direct-tag only** for v1 batch P&L **+ descendant-batch roll-up** (aggregation up
  the lineage tree, not cost allocation — allocation still deferred).
- **Income recognition → accrual** (counts at sale time; payments move outstanding, not P&L).
- **Stages seed:** preparation → growing → production → marketing (admin-editable).

### 2.2 Tables (18)
Identity/lookups: `FarmProfile` (single row; incl. `fiscal_year_start_month`),
`EntityCategory`, `Stage`, `Plantation`, `Tag`.
Money/entities: `Entity`, `Transaction` (one ledger; direction + Decimal amount + txn_date +
is_overhead + nullable attribution FKs + tags M:N).
Inventory/production: `Item` (one catalog, raw+finished; `vendors` M:N→Contact),
`Batch` (`origin` in_house|outsourced authoritative), `Harvest`, `Procurement` (REQ-036),
`StockMovement` (reasons incl. `purchase`), `Recipe`, `ProductionRun` + `ProductionLine`.
Sales/contacts: `Contact` (customer/visitor/vendor), `Sale` (quick; price snapshot),
`Payment`.

### 2.3 REQ-036 — outsourced goods (addendum)
Bought-in goods are ordinary **Items** in a **Batch** stamped `origin=outsourced` (never
Entities), brought in by a lightweight **Procurement** event (+StockMovement reason=purchase
+ vendor expense Transaction). Repack = ProductionRun; resell = Sale. `Item.vendors` is the
standing supplier list. **Negative stock is allowed** as a "shortfall to procure" signal.

---

## 3. System architecture

**Source of truth:** `20-architecture-decisions.md` → `## System architecture` (SA-1..SA-7).
**Architecture diagram:** Excalidraw checkpoint **`fa240ccb76f143aa8b`**; image files
`docs/requirements/farmOS-v1-system-architecture.svg` + `.png`.

### 3.1 Components & layers (SA-1)
Presentation (templates + HTMX + Alpine; `/m/` subset) → **Views (thin:** HTTP/forms/
permissions/HTMX partials, no business logic) → **Service layer** (`record_sale`,
`record_harvest`, `run_production`, `procure`, edit-in-place corrections — each
`transaction.atomic()`; the one place stock + ledger stay consistent) → Data (ORM /
PostgreSQL). Django admin = lookups/catalog/prices/users/FarmProfile only; `Transaction`
and `StockMovement` read-only in admin. No bulk writes on audited models.

### 3.2 API (SA-2)
v1 internal contract = **service-function signatures** (no DRF). URL namespaces reserved:
`/` (web), `/m/` (family subset), `/admin/`, **`/api/`** (future DRF `/api/v1/` + token
auth). Future Telegram/n8n bot and website/CMS feed (REQ-028) call the **same services** —
extension, not rewrite.

### 3.3 Auth & roles (SA-3)
Session auth; **custom user model**. Groups: **admin** = everything incl. Django admin,
catalog, prices, users; **owner/family** = full operational entry + edit/delete own records
+ **view all P&L/turnover/outstanding**. Employees never log in (they're Entities). Password
reset admin-driven (no SMTP). Acting user passed to services → auditlog records *who*.

### 3.4 Corrections & stock policy (SA-4)
**Edit-in-place** (atomic re-compute of linked movement + transaction; auditlog keeps
history). **Negative stock allowed** (procurement signal; admin posts `adjustment` to fix).

### 3.5 Deployment on Coolify (SA-5)
App container (Dockerfile: gunicorn + WhiteNoise; Tailwind in a build stage; migrations at
deploy; `/healthz`; logs→stdout). PostgreSQL: Coolify-bundled, dedicated db/user. TLS via
Coolify proxy (Let's Encrypt) → Django needs `SECURE_PROXY_SSL_HEADER` +
`CSRF_TRUSTED_ORIGINS` (HTMX posts send CSRF header). **Persistent `MEDIA_ROOT` volume** for
the FarmProfile logo, **included in backups** (WhiteNoise serves static only). Backups (PG
dump + media) → owner-owned storage; no paid services. `TIME_ZONE=Asia/Kolkata`, `USE_TZ`;
`fiscal_year_start_month` on FarmProfile.

### 3.6 Audit logging (SA-6)
django-auditlog + `AuditlogMiddleware` on operational models; services avoid bulk writes.

### 3.7 Platform / mobile (SA-7)
v1 responsive web (one app serves `/` laptop + `/m/` phone). APK v2 (Capacitor over `/m/`).
No offline.

---

## 4. Non-functional requirements — how the architecture meets them

| NFR | Requirement | Met by |
|---|---|---|
| Users & roles | REQ-021 | SA-3: session auth, custom user, admin vs owner/family groups; employees = Entities |
| Platform | REQ-022 | SD-2/SA-7 responsive web; SD-3 Capacitor `/m/` path for v2 APK |
| Connectivity | REQ-023 | Cloud-hosted on Coolify; no offline (WebView loads live app) |
| Language | REQ-024a | English-only UI (no i18n layer in v1) |
| Hosting & budget | REQ-026 | SD-5/SA-5: owner VPS + Coolify, bundled PostgreSQL, Dockerfile, backups to owner storage, **no paid third-party** (auth, jobs, export, PDF all self-hosted/none) |
| Audit logging | REQ-027 | SA-6 django-auditlog + middleware; archive-not-delete + PROTECT FKs |
| Hardware/IoT | REQ-029 | None in scope — no integration layer |
| Productization | REQ-030 | Single-farm install, single `FarmProfile` row, no `farm_id` scatter; multi-tenancy = later seam |
| Data start | REQ-025 (v1) | Fresh start; no migration path built |

---

## 5. Requirement → architecture traceability (v1)

| REQ | Handled by |
|---|---|
| REQ-001 Entities & categories | `Entity` + `EntityCategory` (OD-1) |
| REQ-002 Dual income/expense ledger | `Transaction.direction`; any entity via tagged txns |
| REQ-003 Farm portfolio | `FarmProfile` (single row; logo on media volume) |
| REQ-004 Admin customization | Django admin over lookup tables (EntityCategory/Stage/Tag/…) |
| REQ-005 Free ledger + stage tags | `Transaction.stage` (admin-editable `Stage`) |
| REQ-006 Raw+finished inventory | `Item` (one catalog) + `StockMovement` |
| REQ-007 Branching transformation | `ProductionRun` + `ProductionLine` (input/output lines) |
| REQ-008 Consume/yield + tally | Service `run_production` atomic; movement reconciliation |
| REQ-009 Per-input recipes | `Recipe` (Item→allowed-output Items M:N) |
| REQ-010 Batch numbering & P&L | `Batch` + lineage; direct-tag + descendant roll-up (OD-5) |
| REQ-011 Quick sale | `Sale` + service `record_sale` (atomic: StockMovement + income Transaction) |
| REQ-013 Payment tracking | `Payment` rows; outstanding computed |
| REQ-014 Contacts/CRM | `Contact`; history/outstanding computed |
| REQ-015 In-app compose | Templates generate price list/confirmation (no new tables) |
| REQ-016 P&L & turnover (v1 subset) | Reports over `Transaction` (whole-farm + per-batch; print/Save-as-PDF, SD-7) |
| REQ-017 Rich attribution | `Transaction` nullable FKs + tags M:N |
| REQ-021 Users & roles | SA-3 |
| REQ-022 Platform | SA-7 / SD-2 / SD-3 |
| REQ-023 Connectivity | Cloud-hosted; no offline |
| REQ-024a Language | English-only templates |
| REQ-025 (v1) Data start | Fresh install, no migration path built |
| REQ-026 Hosting & budget | SD-5 / SA-5 |
| REQ-027 Audit logging | SA-6 |
| REQ-030 Productization | Single-farm model |
| REQ-031 Overhead bucket | `Transaction.is_overhead` |
| REQ-032 Price catalog | `Item.sale_price` (admin-editable); copied to Sale as snapshot |
| REQ-033 Vendors/suppliers | `Contact` type=vendor; `Item.vendors` M:N; expense txns link vendor |
| REQ-034 Harvest event | `Harvest` (service opens Batch + StockMovement) |
| REQ-036 Outsourced goods/procurement | `Procurement` + `Batch.origin` + `Item.vendors` (§2.3) |

---

## 6. Open questions / assumptions carried into Phase 4 (Design)

- **Report UX & "export" fidelity** — exact print/Save-as-PDF layouts for P&L/turnover and
  the price list (SD-7); whether WeasyPrint is needed is a Phase-4 judgment.
- **`/m/` family subset** — which exact flows the phone-first subset exposes (SD-3) is a
  Design decision; v1 build can start with the full responsive web and carve `/m/` later.
- **Negative-stock UI** — how the "shortfall to procure" signal is surfaced (list/badge/report).
- **Batch numbering format** — user-defined; conventions to suggest (REQ-010 assumption).
- **Deferred modelling** — OD-5 cost-allocation, v2 order workflow (REQ-011b/012), report
  slices (REQ-016 remaining), plantation rollup (REQ-019) — data already captured; views are
  later.

---

## 7. Diagrams index

| Diagram | Checkpoint | Files |
|---|---|---|
| Context/workflow (Phase 2) | `c7c7a71619bc4e1783` | (inline) |
| ER / domain model (Phase 3b, incl. REQ-036) | `6a28140651434bf696` (current; `7bfb393e3cc44189b2` superseded) | `farmOS-v1-domain-ER.svg` + `.png` (canonical) |
| System architecture (Phase 3c) | `fa240ccb76f143aa8b` | `farmOS-v1-system-architecture.svg` + `.png` |
