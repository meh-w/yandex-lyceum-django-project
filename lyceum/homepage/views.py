import http

import django.http
from django.shortcuts import render
from django.utils import timezone

from homepage.fake_items import FAKE_ITEMS

__all__ = [
    "coffee",
    "main_view",
]


def coffee(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


def main_view(request):
    context = {
        "items": FAKE_ITEMS,
        "now": timezone.now(),
    }
    return render(request, "homepage/main.html", context)
