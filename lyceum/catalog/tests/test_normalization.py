__all__ = (
    "CategoryNormalizationTests",
    "TagNormalizationTests",
    "CrossModelNameTests",
    "DifficultTests",
)

from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from catalog.models import Category, Tag


class CategoryNormalizationTests(TestCase):
    @parameterized.expand(
        [
            ("телефоны",),
            ("ТЕЛЕФОНЫ",),
            ("  телефоны  ",),
            ("телефоны!!!",),
            ("ТеЛеФоНы???",),
        ],
    )
    def test_cannot_create_similar_categories(self, duplicate_name):
        Category.objects.create(
            name="Телефоны",
            slug="telefon",
        )

        duplicate = Category(name=duplicate_name, slug="telefon-slug")

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    @parameterized.expand(
        [
            ("3аря"),
            ("зapя"),
            ("Зapя!!!"),
            (" 3АРЯ "),
        ],
    )
    def test_cant_create_leet_duplicates(self, duplicate_name):
        Category.objects.create(name="Заря", slug="zarya")

        duplicate = Category(name=duplicate_name, slug="zarya2")

        with self.assertRaises(ValidationError):
            duplicate.full_clean()


class TagNormalizationTests(TestCase):
    @parameterized.expand(
        [
            ("смартфоны",),
            ("СМАРТФОНЫ",),
            ("  смартфоны  ",),
            ("смартфоны!!!",),
            ("СмАрТфОнЫ???",),
        ],
    )
    def test_cannot_create_similar_tags(self, duplicate_name):
        Tag.objects.create(
            name="Смартфоны",
            slug="smartphone",
        )

        duplicate = Tag(name=duplicate_name, slug="smartphone-second")

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    @parameterized.expand(
        [
            ("l0l"),
            ("lоl"),
        ],
    )
    def test_difficult_duplicates(self, duplicate_name):
        Tag.objects.create(name="lol", slug="lol")

        duplicate = Tag(name=duplicate_name, slug="lol2")

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_yo_equals_e(self):
        Tag.objects.create(name="ёлка", slug="elka")

        duplicate = Tag(name="елка", slug="elka2")

        with self.assertRaises(ValidationError):
            duplicate.full_clean()


class CrossModelNameTests(TestCase):
    def test_category_and_tag_can_have_same_name(self):
        Category.objects.create(name="Ноутбуки", slug="notebook")

        tag = Tag(name="Ноутбуки", slug="notebook-tag")

        tag.full_clean()


class DifficultTests(TestCase):
    def test_b_cyrillic_vs_latin(self):
        Category.objects.create(name="воровать", slug="vorovat")

        duplicate = Category(name="вороватb", slug="vorovat2")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_i_l_1_equivalence(self):
        Category.objects.create(name="иллюзия", slug="illuziya")

        duplicates = ["iллюзия", "lлюзия", "1люзия"]
        for dup in duplicates:
            duplicate = Category(name=dup, slug=f"{dup}-slug")
            with self.assertRaises(ValidationError):
                duplicate.full_clean()

    def test_yoga_equivalence(self):
        Category.objects.create(name="йога", slug="yoga")

        duplicate = Category(name="иога", slug="yoga2")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
