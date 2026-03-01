from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from sorl.thumbnail import get_thumbnail

from catalog.validators import ValidateMustContain
from core.models import (
    BaseIsPublishedModel,
    BaseNameModel,
    NormalizedNameMixinModel,
)

__all__ = [
    "Category",
    "Item",
    "ItemImage",
    "ItemMainImage",
    "Tag",
]


class Category(BaseIsPublishedModel, BaseNameModel, NormalizedNameMixinModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text=(
            "до 200 символов, уникальное значение,"
            " только цифры, латиница и символы - и _"
        ),
    )

    weight = models.PositiveIntegerField(
        default=100,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(32767),
        ],
        verbose_name="вес",
        help_text="число из диапазона [1;32767]",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Tag(BaseIsPublishedModel, BaseNameModel, NormalizedNameMixinModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text=(
            "до 200 символов, уникальное значение,"
            " только цифры, латиница и символы - и _"
        ),
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Item(BaseIsPublishedModel, BaseNameModel):
    text = CKEditor5Field(
        validators=[
            ValidateMustContain("превосходно", "роскошно"),
        ],
        verbose_name="текст",
        help_text=("текст, в котором содержится превосходно/роскошно"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="категория",
        help_text="выберите категорию",
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="related",
        verbose_name="тег",
        help_text="выберите теги для товара",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def admin_image(self):
        if hasattr(self, "main_image") and self.main_image.image:
            thumb = get_thumbnail(
                self.main_image.image,
                "300x300",
                crop="center",
                quality=85,
            )
            return mark_safe(f"<img src='{thumb.url}' width='40' height='40'>")
        return "—"

    admin_image.short_description = "Изображение"


class ItemMainImage(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        related_name="main_image",
        verbose_name="товар",
    )
    image = models.ImageField(
        upload_to="items/main/",
        verbose_name="главное изображение",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"

    def __str__(self):
        return f"Главное изображение {self.item}"


class ItemImage(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="товар",
    )
    image = models.ImageField(
        upload_to="items/gallery/",
        verbose_name="изображение",
    )

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return f"Изображение {self.item}"
