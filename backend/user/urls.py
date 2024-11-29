from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from user.views import (
    RegisterUserView,
    CustomTokenObtainPairView,
    EmailVerificationView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("account-verification/", EmailVerificationView.as_view(), name="account_activation"),
]
