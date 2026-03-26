__all__ = ("CatalogContextTests",)

from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from catalog.models import Category, Item, ItemImage, ItemMainImage, Tag


class CatalogContextTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Категория", slug="cat")
        cls.tag = Tag.objects.create(name="тег", slug="tag")

        cls.item = Item.objects.create(
            name="Товар",
            text="<p>превосходно</p>",
            category=cls.category,
            is_published=True,
            is_on_main=True,
        )
        cls.item.tags.set([cls.tag])

        cls.main_image = ItemMainImage.objects.create(
            item=cls.item,
            image="main.jpg",
        )
        cls.extra_image = ItemImage.objects.create(
            item=cls.item,
            image="extra.jpg",
        )

        cls.unpublished = Item.objects.create(
            name="Скрытый",
            text="превосходно",
            category=cls.category,
            is_published=False,
            is_on_main=False,
        )

        cls.item2 = Item.objects.create(
            name="Второй товар",
            text="<p>роскошно</p>",
            category=cls.category,
            is_published=True,
            is_on_main=True,
        )

        cls.not_on_main = Item.objects.create(
            name="Не на главной",
            text="<p>превосходно</p>",
            category=cls.category,
            is_published=True,
            is_on_main=False,
        )

        cls.expected_published_count = Item.objects.filter(
            is_published=True,
        ).count()

        cls.expected_main_count = Item.objects.filter(
            is_published=True,
            is_on_main=True,
        ).count()

    def test_item_list_context_keys(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_item_list_context_type(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertIsInstance(response.context["items"], QuerySet)

    def test_item_list_filters_unpublished(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = response.context["items"]
        item_ids = [item.id for item in items]
        self.assertNotIn(self.unpublished.id, item_ids)

    def test_item_list_items_count(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertEqual(len(items), self.expected_published_count)

    def test_item_detail_context_keys(self):
        response = self.client.get(
            reverse("catalog:item", args=[self.item.id]),
        )
        self.assertIn("item", response.context)

    def test_item_detail_has_main_image(self):
        response = self.client.get(
            reverse("catalog:item", args=[self.item.id]),
        )
        item = response.context["item"]
        self.assertTrue(hasattr(item, "main_image"))
        self.assertEqual(item.main_image, self.main_image)

    def test_item_detail_has_additional_images(self):
        response = self.client.get(
            reverse("catalog:item", args=[self.item.id]),
        )
        item = response.context["item"]
        additional_images = list(item.images.all())
        self.assertEqual(len(additional_images), 1)
        self.assertEqual(additional_images[0].id, self.extra_image.id)

    @parameterized.expand(
        [
            ("unpublished", "unpublished"),
            ("nonexistent", 999),
        ],
    )
    def test_item_detail_404(self, name, item_id):
        if name == "unpublished":
            item_id = self.unpublished.id

        response = self.client.get(reverse("catalog:item", args=[item_id]))
        self.assertEqual(response.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        ItemImage.objects.all().delete()
        ItemMainImage.objects.all().delete()
        Item.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        super().tearDownClass()
