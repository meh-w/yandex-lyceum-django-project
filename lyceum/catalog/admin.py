import django.contrib.admin

import catalog.models

__all__ = [
    "CategoryAdmin",
    "ItemAdmin",
    "TagAdmin",
]


class ItemMainImageInline(django.contrib.admin.StackedInline):
    model = catalog.models.ItemMainImage
    extra = 0
    max_num = 1
    verbose_name = "главное изображение"


class ItemImageInline(django.contrib.admin.TabularInline):
    model = catalog.models.ItemImage
    extra = 1
    verbose_name = "изображение"
    verbose_name_plural = "изображения"


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        "admin_image",
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)

    inlines = (
        ItemMainImageInline,
        ItemImageInline,
    )

    @django.contrib.admin.display(description="Краткое описание")
    def short_text(self, obj):
        return obj.text[:50]


@django.contrib.admin.register(catalog.models.Tag)
class TagAdmin(django.contrib.admin.ModelAdmin):
    pass


@django.contrib.admin.register(catalog.models.Category)
class CategoryAdmin(django.contrib.admin.ModelAdmin):
    pass
