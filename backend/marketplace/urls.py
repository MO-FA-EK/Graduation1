from django.urls import path
from . import views

urlpatterns = [
    path("programmers/", views.programmer_list, name="programmer_list"),
    path("programmers/<int:id>/", views.programmer_detail, name="programmer_detail"),
    path("programmers/<int:id>/rate/", views.rate_programmer, name="rate_programmer"),
    path("programmers/<int:id>/view/", views.increment_profile_views, name="programmer_view"),
    path("programmers/<int:id>/contact/", views.increment_contact_clicks, name="programmer_contact"),
    
    path("profile/", views.my_profile, name="my_profile"),
    path("contact/", views.contact_us, name="contact_us"),

    path("projects/my/", views.my_projects, name="my_projects"),
    path("projects/create/<int:freelancer_id>/", views.create_project, name="create_project"),
    path("projects/<int:project_id>/update/", views.update_project, name="update_project"),
    path("projects/<int:project_id>/accept/", views.accept_project, name="accept_project"),

    path("projects/payment-intent/<int:project_id>/", views.create_payment_intent, name="create_payment_intent"),
    
    path("projects/confirm-payment/<str:payment_id>/", views.confirm_payment, name="confirm_payment_stripe"), 

    path("projects/<int:project_id>/confirm-payment/", views.confirm_project_payment_status, name="confirm_project_payment"),
    
    path("admin/projects/", views.AdminProjectListView.as_view(), name="admin_project_list"),
    path("admin/projects/<int:id>/delete/", views.AdminDeleteProjectView.as_view(), name="admin_project_delete"),
]