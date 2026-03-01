from django.urls import path

from homepage.views import (
    coffee,
    main_view,
)

app_name = "homepage"

urlpatterns = [
    path("", main_view, name="main"),
    path("coffee/", coffee, name="coffee"),
]
