from django.urls import path, re_path

from . import doctor_views

urlpatterns = [
    path("dashboard/", doctor_views.dashboard, name="doctor_dashboard"),
    path(
        "booking_pending/", doctor_views.booking_pending, name="doctor_booking_pending"
    ),
    path(
        "booking_update/<int:pk>/",
        doctor_views.BookingUpdate.as_view(),
        name="doctor_booking_update",
    ),
    path("booking_list/", doctor_views.booking_list, name="doctor_booking_list"),
    path(
        "meeting-room/<str:room>",
        doctor_views.meeting_room,
        name="doctor_meeting_room",
    ),
    path(
        "appoint_list/", doctor_views.AppointmentListView.as_view(), name="appoint_list"
    ),
    re_path(r"^appoint/new/$", doctor_views.event, name="appoint_add"),
    re_path(
        r"^appoint/edit/(?P<event_id>\d+)/$", doctor_views.event, name="appoint_edit"
    ),
]
