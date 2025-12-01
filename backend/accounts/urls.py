from django.urls import path
from .views import RegisterView, LoginView, TokenRefreshCustomView, ValidateTokenView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("login/", LoginView.as_view(), name="auth_login"),
    path("refresh/", TokenRefreshCustomView.as_view(), name="auth_refresh"),
    path("validate-token/", ValidateTokenView.as_view(), name="auth_validate"),
]
