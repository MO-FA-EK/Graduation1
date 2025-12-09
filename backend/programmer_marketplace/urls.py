from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Marketplace endpoints
    path("api/", include("marketplace.urls")),

    # Authentication: register + login
    path("api/auth/", include("accounts.urls")),
]
