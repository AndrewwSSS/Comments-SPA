from django.urls import path
from captcha.views import CaptchaAPIView


urlpatterns = [
    path("", CaptchaAPIView.as_view(), name="captcha"),
]