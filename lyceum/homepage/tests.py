__all__ = (
    "HomepageContextTests",
    "HomepageURLTests",
)

import http

from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Item


class HomepageContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Категория", slug="cat")

        cls.item_on_main = Item.objects.create(
            name="На главной",
            text="превосходно",
            category=cls.category,
            is_published=True,
            is_on_main=True,
        )

        cls.item_not_on_main = Item.objects.create(
            name="Не на главной",
            text="превосходно",
            category=cls.category,
            is_published=True,
            is_on_main=False,
        )

        cls.unpublished = Item.objects.create(
            name="Скрытый",
            text="превосходно",
            category=cls.category,
            is_published=False,
            is_on_main=True,
        )

    def test_homepage_context_keys(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertIn("items", response.context)

    def test_homepage_filters_correctly(self):
        response = self.client.get(reverse("homepage:main"))
        items = response.context["items"]
        item_ids = [item.id for item in items]

        self.assertIn(self.item_on_main.id, item_ids)
        self.assertNotIn(self.item_not_on_main.id, item_ids)
        self.assertNotIn(self.unpublished.id, item_ids)

    def test_homepage_sorted_by_name(self):
        Item.objects.create(
            name="Ааа первый",
            text="превосходно",
            category=self.category,
            is_published=True,
            is_on_main=True,
        )

        response = self.client.get(reverse("homepage:main"))
        items = list(response.context["items"])
        item_names = [item.name for item in items]

        self.assertEqual(item_names[0], "Ааа первый")
        self.assertEqual(item_names[1], "На главной")

    @classmethod
    def tearDownClass(cls):
        Item.objects.all().delete()
        Category.objects.all().delete()
        super().tearDownClass()


class HomepageURLTests(TestCase):
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
