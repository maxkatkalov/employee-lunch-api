from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user-area/", include("user_service.urls")),
    path(
        "api/restaurants-management/",
        include("restaurant_service.urls", namespace="restaurant"),
    ),
    path("api/polling/", include("polling_service.urls", namespace="polling")),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
