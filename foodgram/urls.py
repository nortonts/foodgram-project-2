from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path


handler404 = "recipes.views.page_not_found"
handler500 = "recipes.views.server_error"

urlpatterns = [
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("purchases/", include("purchases.urls")),
    path("about/", include("django.contrib.flatpages.urls")),
    path(
        "about-author/",
        views.flatpage,
        {"url": "/about-author/"},
        name="about_author",
    ),
    path(
        "about-spec/",
        views.flatpage,
        {"url": "/about-spec/"},
        name="about_spec",
    ),
    path("", include("recipes.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
