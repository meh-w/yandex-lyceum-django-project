import django.test
from django.urls import reverse

__all__ = [
    "ReverseMiddlewareEnabledTests",
    "ReverseMiddlewareDisabledTests",
    "ReverseMiddlewareDefaultTests",
]


@django.test.override_settings(ALLOW_REVERSE=True)
class ReverseMiddlewareEnabledTests(django.test.TestCase):
    def setUp(self):
        from lyceum.middleware import ReverseRussianEveryTenthMiddleware

        ReverseRussianEveryTenthMiddleware.counter = 0

    def test_reverse_is_enabled(self):
        url = reverse("homepage:coffee")
        for i in range(1, 10):
            response = self.client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")

        response = self.client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "Я кинйач")

    def test_20th_response_also_reversed(self):
        from lyceum.middleware import ReverseRussianEveryTenthMiddleware

        ReverseRussianEveryTenthMiddleware.counter = 0

        url = reverse("homepage:coffee")
        for i in range(10):
            response = self.client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "Я кинйач")

        for i in range(9):
            response = self.client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")

        response = self.client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "Я кинйач")


@django.test.override_settings(ALLOW_REVERSE=False)
class ReverseMiddlewareDisabledTests(django.test.TestCase):
    def setUp(self):
        from lyceum.middleware import ReverseRussianEveryTenthMiddleware

        ReverseRussianEveryTenthMiddleware.counter = 0

    def test_reverse_is_disabled(self):
        url = reverse("homepage:coffee")
        for i in range(1, 10 + 1):
            response = self.client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")


class ReverseMiddlewareDefaultTests(django.test.TestCase):
    def setUp(self):
        from lyceum.middleware import ReverseRussianEveryTenthMiddleware

        ReverseRussianEveryTenthMiddleware.counter = 0

    def test_default_behavior(self):
        url = reverse("homepage:coffee")
        for i in range(9):
            response = self.client.get(url)
            self.assertEqual(response.content.decode("utf-8"), "Я чайник")

        response = self.client.get(url)
        self.assertEqual(response.content.decode("utf-8"), "Я кинйач")
