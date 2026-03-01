import http

import django.test
from django.urls import NoReverseMatch, reverse
from parameterized import parameterized

__all__ = ["CatalogURLTests"]


class CatalogURLTests(django.test.TestCase):
    def test_catalog_endpoint(self):
        url = reverse("catalog:item_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
        )

    @parameterized.expand(
        [
            ("001", http.HTTPStatus.OK),
            (0, http.HTTPStatus.OK),
            (1, http.HTTPStatus.OK),
            (20, http.HTTPStatus.OK),
            (300, http.HTTPStatus.OK),
        ],
    )
    def test_catalog_re_valid_numbers(self, int_item, expected_status):
        url = reverse(
            "catalog:return_number",
            kwargs={"int_item": int_item},
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            expected_status,
            msg=f"URL {url} should return {expected_status}",
        )

    @parameterized.expand(
        [
            ("negative", -3),
            ("float_positive", 5.27),
            ("float_negative", -0.2),
            ("string_abc", "abc"),
            ("string_123abc", "123abc"),
            ("empty_string", ""),
            ("emoji", "🤠🤨"),
            ("japanese", "よべま"),
            ("devanagari", "१२३"),
            ("bengali", "৭৮৯"),
            ("scientific", "1e3"),
            ("underscore", "1_000_000"),
        ],
    )
    def test_catalog_re_invalid_numbers(self, name, value):
        with self.assertRaises(NoReverseMatch):
            reverse("catalog:return_number", kwargs={"int_item": value})
