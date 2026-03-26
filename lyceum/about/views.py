__all__ = ("about_view",)

from django.shortcuts import render
from django.utils import timezone


def about_view(request):
    context = {
        "now": timezone.now(),
    }

    return render(request, "about/about.html", context)
