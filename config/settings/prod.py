"""Production settings — Coolify + Dockerfile (SD-5/SA-5)."""
from .base import *  # noqa: F401,F403
from .base import env_list

DEBUG = False

# TLS terminates at the Coolify proxy; trust its forwarded header (SA-5).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS", "")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
