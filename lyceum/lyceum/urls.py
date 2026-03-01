from django.conf import settings
from django.conf.urls.static import static
import django.contrib
from django.urls import include, path

urlpatterns = [
    path("", include("homepage.urls")),
    path("about/", include("about.urls")),
    path("admin/", django.contrib.admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
