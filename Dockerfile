# farmOS v1 — production image for Coolify (SD-5/SA-5).
# gunicorn + WhiteNoise; Tailwind built via the standalone CLI (pytailwindcss, no Node).
FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.prod

WORKDIR /app

# System deps kept minimal (psycopg[binary] needs no libpq-dev).
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Build Tailwind CSS and collect static (SD-5). SECRET_KEY needed only to import settings.
RUN SECRET_KEY=build-only tailwindcss -i static/src/input.css -o static/css/app.css --minify \
    && SECRET_KEY=build-only python manage.py collectstatic --noinput

EXPOSE 8000

# Migrations run at deploy, then serve. /healthz is the Coolify probe.
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
