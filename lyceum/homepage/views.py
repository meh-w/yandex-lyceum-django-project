__all__ = (
    "coffee",
    "echo_form",
    "echo_submit",
    "main_view",
)

import http

from django.db.models import Prefetch
import django.http
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

from catalog.models import Item, Tag


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


def main_view(request):
    items_on_main = (
        Item.objects.filter(is_published=True, is_on_main=True)
        .select_related("category")
        .prefetch_related(Prefetch("tags", queryset=Tag.objects.only("name")))
        .only("id", "name", "text", "category__name")
        .order_by("name")
    )

    for item in items_on_main:
        item.text = strip_tags(item.text)

    context = {"items": items_on_main}

    return render(request, "homepage/main.html", context)


def echo_form(request):
    return render(request, "homepage/echo_form.html")


@csrf_exempt
@require_POST
def echo_submit(request):
    text = request.POST.get("text", "")
    return HttpResponse(text, content_type="text/plain; charset=utf-8")
