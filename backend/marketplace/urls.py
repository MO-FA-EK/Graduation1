from django.urls import path
from . import views

urlpatterns = [
    path("programmers/", views.programmer_list, name="programmer_list"),
    path("programmers/<int:id>/", views.programmer_detail, name="programmer_detail"),
    path("programmers/<int:id>/rate/", views.rate_programmer, name="rate_programmer"),
    path("profile/", views.my_profile, name="my_profile"),
]
