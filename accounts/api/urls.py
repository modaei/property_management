from .views import (
    RegisterAPIView,
    UserRetrieveUpdateAPIView,
    ChangePasswordView,
    RequestValidationTokenView,
    ConfirmValidationTokenView,
    JWTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView

from django.urls import path, include

app_name = 'accounts-api'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="register"),
    path('user-info/', UserRetrieveUpdateAPIView.as_view(), name="user-info"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('token/', JWTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('verify/request-verify/', RequestValidationTokenView.as_view(), name="request-validation"),
    path('verify/confirm-verify/', ConfirmValidationTokenView.as_view(), name="confirm-validation"),
]
