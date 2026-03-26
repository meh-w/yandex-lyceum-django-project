__all__ = (
    "item_list",
    "item_detail",
)

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render

from catalog.models import Item, Tag


def item_list(request):
    items = (
        Item.objects.filter(is_published=True, category__is_published=True)
        .select_related("category")
        .prefetch_related(Prefetch("tags", queryset=Tag.objects.only("name")))
        .only("id", "name", "text", "category__name")
        .order_by("category__name")
    )

    context = {"items": items}

    return render(request, "catalog/item_list.html", context)


def item_detail(request, item_id):
    item = get_object_or_404(
        Item.objects.filter(is_published=True)
        .select_related("category", "main_image")
        .prefetch_related(
            Prefetch("tags", queryset=Tag.objects.only("name")),
            "images",
        )
        .only(
            "id",
            "name",
            "text",
            "category__name",
            "main_image__image",
        ),
        id=item_id,
    )

    context = {
        "item": item,
        "main_image": getattr(item, "main_image", None),
    }

    return render(request, "catalog/item.html", context)
