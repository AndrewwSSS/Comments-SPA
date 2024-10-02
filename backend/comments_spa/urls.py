from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path("api/users/", include("user.urls")),
    path("api/", include("comments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
