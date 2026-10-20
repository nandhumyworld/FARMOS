from django.test import TestCase
from django.urls import reverse


class SkeletonSmokeTests(TestCase):
    """Stage-A skeleton smoke tests. Behavioural TDD starts at Slice B0."""

    def test_healthz_ok(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    def test_home_placeholder_renders(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
