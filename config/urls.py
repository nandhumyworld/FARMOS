"""farmOS v1 URL configuration.

Namespaces reserved per SA-2: `/` (web), `/m/` (family subset, Stage A Slice A4),
`/admin/` (Django admin), `/api/` (future DRF). Only the skeleton routes exist now;
screens are added by `/build-next` (Stage A).
"""
from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz", views.healthz, name="healthz"),
    # Placeholder home so LOGIN_REDIRECT_URL resolves; real Dashboard = Slice A3.
    path("", views.home_placeholder, name="dashboard"),
]
