from django.urls import path

from homepage.views import (
    coffee,
    echo_form,
    echo_submit,
    main_view,
)

app_name = "homepage"

urlpatterns = [
    path("", main_view, name="main"),
    path("coffee/", coffee, name="coffee"),
    path("echo/", echo_form, name="echo_form"),
    path("echo/submit/", echo_submit, name="echo_submit"),
]
