from django.urls import path
from . import views
from .views import RegisterView, LoginView, ChangePasswordView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    
    path("admin/users/", views.AdminUserListView.as_view(), name="admin_user_list"),
    path("admin/users/<int:id>/delete/", views.AdminDeleteUserView.as_view(), name="admin_user_delete"),
]