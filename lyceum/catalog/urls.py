from django.urls import path, re_path

from catalog.views import item_list_view, item_view, return_number

app_name = "catalog"

urlpatterns = [
    path("", item_list_view, name="item_list"),
    path("<int:item_id>/", item_view, name="item"),
    re_path(
        r"^re/(?P<int_item>[0-9]+)/$",
        return_number,
        name="return_number",
    ),
]
