from django.urls import path, include


urlpatterns = [
    path("api/users/", include("user.urls")),
    path("api/", include("comments.urls")),
]
