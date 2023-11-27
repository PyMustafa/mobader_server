from django.urls import path

from . import pages_views, views

urlpatterns = [
    path("", pages_views.home_ar, name="home_ar"),
    path("user/login/", views.user_login, name="login"),
    path("login/", views.user_login, name="user-login"),
    path(
        "users_logout_process/", views.users_logout_process, name="users_logout_process"
    ),
    path("media/", pages_views.media_ar, name="media_ar"),
    path("about-us/", pages_views.about_us_ar, name="about_us_ar"),
    path("contact-us/", pages_views.contact_us_ar, name="contact_us_ar"),
    path(
        "medical-servies/", pages_views.medical_services_ar, name="medical_services_ar"
    ),
    path(
        "medical-servies/service-nursing/",
        pages_views.service_nursing_ar,
        name="service_nursing_ar",
    ),
    path(
        "medical-servies/service-medical/",
        pages_views.service_medical_ar,
        name="service_medical_ar",
    ),
    # English routes
    path("en/", pages_views.home_en, name="home_en"),
    path("en/about-us/", pages_views.about_us_en, name="about_us_en"),
    path("en/contact-us/", pages_views.contact_us_en, name="contact_us_en"),
    path(
        "en/medical-servies/",
        pages_views.medical_services_en,
        name="medical_services_en",
    ),
    path(
        "en/medical-servies/service-nursing/",
        pages_views.service_nursing_en,
        name="service_nursing_en",
    ),
    path(
        "en/medical-servies/service-medical/",
        pages_views.service_medical_en,
        name="service_medical_en",
    ),
]
