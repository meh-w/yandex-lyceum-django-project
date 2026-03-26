from django.urls import path

from catalog.views import item_detail, item_list

app_name = "catalog"

urlpatterns = [
    path("", item_list, name="item-list"),
    path("<int:item_id>/", item_detail, name="item"),
]
