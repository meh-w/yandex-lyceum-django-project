__all__ = ("AboutURLTests",)

import http

import django.test
from django.urls import reverse


class AboutURLTests(django.test.TestCase):
    def test_about_endpoint(self):
        url = reverse("about:about")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
        )
