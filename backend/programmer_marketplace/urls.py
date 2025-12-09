from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/auth/", include("accounts.urls")),     # register + login
    path("api/", include("marketplace.urls")),        # programmers
]
