from django.core.exceptions import ValidationError
import django.test
from parameterized import parameterized

from catalog.models import Category, Item, Tag

__all__ = [
    "ItemTextValidationTests",
    "ModelsValidationTests",
]


class ItemTextValidationTests(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name="категория",
            slug="cat_ego_ry",
            weight=100,
            is_published=True,
        )

    @parameterized.expand(
        [
            ("just_text", "просто текст"),
            ("substring_text_01", "мы говорим про роскошность"),
            ("substring_text_02", "и про превосходность тоже говорим"),
        ],
    )
    def test_text_witout_mandatory_words(self, name, text):
        item = Item(
            name="товар",
            text=text,
            category=self.category,
            is_published=True,
        )

        with self.assertRaises(ValidationError):
            item.full_clean()

    @parameterized.expand(
        [
            ("valid_01", "это превосходно работает"),
            ("valid_02", "абсолютно роскошно"),
            ("both_valid", "роскошно и превосходно"),
            ("with_html_tags", "<p><strong>превосходно</strong></p>"),
            ("so_much_space_but_valid", "                       \nроскошно  "),
            ("uppercase", "это ПРЕВОСХОДНО"),
            ("mixed_case", "это ПрЕвОсХодНо"),
            ("with_symbols", "роскошно!@@"),
            ("with_comma", "превосходно, роскошно, друзья"),
        ],
    )
    def test_text_with_mandatory_words(self, name, text):
        item = Item(
            name="товар",
            text=text,
            category=self.category,
            is_published=True,
        )

        item.full_clean()

    @classmethod
    def tearDownClass(cls):
        Category.objects.all().delete()
        Item.objects.all().delete()
        super().tearDownClass()


class ModelsValidationTests(django.test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category_data = {
            "name": "тестовая категория",
            "slug": "test_slug",
            "weight": 100,
        }

        cls.tag_data = {
            "name": "тестовый тег",
            "slug": "test_tag",
        }

        cls.category = Category.objects.create(
            name="категория",
            slug="cat_ego_ry",
            weight=100,
        )

        cls.test_category = Category.objects.create(
            name="тестовая категория",
            slug="test_slug",
        )

        cls.test_tag = Tag.objects.create(
            name="тестовый тег",
            slug="test_tag",
        )

    @parameterized.expand(
        [
            ("cat_name_max", Category, "name", "а" * 151, "category_data"),
            ("cat_slug_max", Category, "slug", "а" * 201, "category_data"),
            ("tag_name_max", Tag, "name", "а" * 151, "tag_data"),
            ("tag_slug_max", Tag, "slug", "а" * 201, "tag_data"),
        ],
    )
    def test_max_length(self, name, model_class, field, long_value, data_key):
        data = getattr(self, data_key).copy()
        data[field] = long_value

        obj = model_class(**data)

        with self.assertRaises(ValidationError) as context:
            obj.full_clean()

        self.assertIn(field, context.exception.message_dict)

    @parameterized.expand(
        [
            ("weight_min", 0),
            ("weight_max", 32768),
            ("weight_negative", -10),
        ],
    )
    def test_weight_validation(self, name, weight_value):
        data = self.category_data.copy()
        data["weight"] = weight_value

        category = Category(**data)

        with self.assertRaises(ValidationError) as context:
            category.full_clean()

        self.assertIn("weight", context.exception.message_dict)

    def test_weight_default(self):
        category = Category.objects.create(
            name="другая категория",
            slug="other_slug",
        )
        self.assertEqual(category.weight, 100)

    def test_item_name_max_length(self):
        item = Item(
            name="а" * 151,
            text="превосходно",
            category=self.category,
        )

        with self.assertRaises(ValidationError) as context:
            item.full_clean()

        self.assertIn("name", context.exception.message_dict)

    @parameterized.expand(
        [
            ("category_published", "test_category"),
            ("tag_published", "test_tag"),
        ],
    )
    def test_is_published_default(self, name, obj_attr):
        obj = getattr(self, obj_attr)
        self.assertTrue(obj.is_published)

    def test_item_published_default(self):
        item = Item.objects.create(
            name="новый товар",
            text="превосходно",
            category=self.category,
        )
        self.assertTrue(item.is_published)
