from django.urls import path
from . import views

urlpatterns = [
    path("programmers/", views.programmer_list, name="programmer_list"),
    path("programmers/<int:id>/", views.programmer_detail, name="programmer_detail"),
    path("programmers/<int:id>/rate/", views.rate_programmer, name="rate_programmer"),

    # tracking
    path("programmers/<int:id>/view/", views.increment_profile_views, name="programmer_view"),
    path("programmers/<int:id>/contact/", views.increment_contact_clicks, name="programmer_contact"),

    path("profile/", views.my_profile, name="my_profile"),
]
