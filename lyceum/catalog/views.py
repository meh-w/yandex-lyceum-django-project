import django.http
from django.shortcuts import render
from django.utils import timezone

from homepage.fake_items import FAKE_ITEMS

__all__ = [
    "item_list_view",
    "item_view",
    "return_number",
]


def item_list_view(request):
    context = {
        "items": FAKE_ITEMS,
        "now": timezone.now(),
    }
    return render(request, "catalog/item_list.html", context)


def item_view(request, item_id):
    item = next((x for x in FAKE_ITEMS if x["id"] == item_id), None)

    context = {
        "item": item,
        "now": timezone.now(),
    }
    return render(request, "catalog/item.html", context)


def return_number(request, int_item):
    return django.http.HttpResponse(str(int_item))
