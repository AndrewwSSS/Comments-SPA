from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path("api/users/", include("user.urls")),
    path("api/", include("comments.urls")),
    path("api/captcha", include("captcha.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
