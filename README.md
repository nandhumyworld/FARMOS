# farmOS (v1)

Single-farm operations app for a family natural-farming business — captures harvests,
production, procurement and sales through an atomic, audited service layer, and reports
P&L / turnover / outstanding and per-batch economics.

**Stack:** Django 5.2 LTS · HTMX + Alpine · Tailwind (standalone CLI, no Node) · PostgreSQL ·
gunicorn + WhiteNoise · Docker on Coolify. See `docs/requirements/ARCHITECTURE-v1.md`.

**Build approach:** UI-first — see `docs/requirements/40-build-plan.md` (Stage A static UI
prototype → ▲ UI review → Stage B backend wiring). Requirements/architecture/design are in
`docs/requirements/` (`REQUIREMENTS-v1.md`, `ARCHITECTURE-v1.md`, `DESIGN-v1.md`).

## Local development

Requires Python 3.12+ (use `py -3.13` on Windows).

```bash
# 1. Virtualenv + deps
py -3.13 -m venv .venv
.venv\Scripts\activate            # Windows (PowerShell: .venv\Scripts\Activate.ps1)
pip install -r requirements.txt

# 2. Environment — copy the template and fill in your DB URL
copy .env.example .env            # cp on macOS/Linux
#   set DATABASE_URL to your cloud Postgres, or leave blank to use local SQLite

# 3. Build CSS (Tailwind standalone CLI)
tailwindcss -i static/src/input.css -o static/css/app.css --watch

# 4. Migrate + run
python manage.py migrate
python manage.py runserver
```

- App: http://127.0.0.1:8000/ · Health: http://127.0.0.1:8000/healthz · Admin: `/admin/`
- Create an admin user: `python manage.py createsuperuser`

## Database

Dev/test and production both use PostgreSQL via `DATABASE_URL` (Django ORM + migrations).
If `DATABASE_URL` is unset, dev falls back to a local SQLite file — enough for the Stage A
UI prototype, which has no domain models yet.

## Tests

```bash
python manage.py test
```

## Deployment

Coolify builds the committed `Dockerfile`; set env vars (`SECRET_KEY`, `DEBUG=False`,
`ALLOWED_HOSTS`, `DATABASE_URL`, `CSRF_TRUSTED_ORIGINS`) in Coolify. Migrations run at start;
`/healthz` is the health probe. A persistent volume backs `MEDIA_ROOT` (FarmProfile logo).
