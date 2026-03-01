import http

import django.test
from django.urls import reverse

__all__ = ["HomepageURLTests"]


class HomepageURLTests(django.test.TestCase):
    def test_homepage_endpoint(self):
        url = reverse("homepage:main")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
        )

    def test_coffee_endpoint(self):
        url = reverse("homepage:coffee")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.IM_A_TEAPOT,
        )
        self.assertEqual(response.content.decode("utf-8"), "Я чайник")
