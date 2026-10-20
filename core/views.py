from django.http import HttpResponse
from django.shortcuts import render


def healthz(request):
    """Liveness probe for Coolify (SA-5). Plain 200, no DB touch."""
    return HttpResponse("ok", content_type="text/plain")


def home_placeholder(request):
    """Temporary home so routing/login redirects resolve.

    Replaced by the real action-first Dashboard in Stage A Slice A3.
    """
    return render(request, "home_placeholder.html")
