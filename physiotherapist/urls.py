from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="physio_dashboard"),
    path(
        "services_list/", views.ServicesListView.as_view(), name="physio_services_list"
    ),
    path(
        "service_create/", views.ServicesCreate.as_view(), name="physio_service_create"
    ),
    path(
        "service_update/<int:pk>/",
        views.ServicesUpdate.as_view(),
        name="physio_service_update",
    ),
    path(
        "service_delete/<int:pk>/",
        views.ServiceDeleteView.as_view(),
        name="physio_service_delete",
    ),
    path(
        "services_times_list/",
        views.ServicesTimesListView.as_view(),
        name="physio_services_times_list",
    ),
    path(
        "service_time_create/",
        views.ServicesTimesCreate.as_view(),
        name="physio_service_time_create",
    ),
    path(
        "service_time_update/<int:pk>/",
        views.ServicesTimeUpdate.as_view(),
        name="physio_service_time_update",
    ),
    path(
        "service_time_delete/<int:pk>/",
        views.ServiceTimeDeleteView.as_view(),
        name="physio_service_time_delete",
    ),
    path(
        "booking_pending/",
        views.booking_pending,
        name="physio_booking_pending",
    ),
    path(
        "booking_update/<int:pk>/",
        views.BookingUpdate.as_view(),
        name="physio_booking_update",
    ),
    path(
        "booking_list/",
        views.booking_list,
        name="physio_booking_list",
    ),
]
