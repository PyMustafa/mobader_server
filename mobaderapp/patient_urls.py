from django.urls import path

from . import patient_views

urlpatterns = [
    # =================================================
    # Register
    path(
        "register/",
        patient_views.PatientUserCreateView.as_view(),
        name="register_patient",
    ),
    #path(
    #    "register/",
    #    patient_views.register_view,
    #    name="register_patient",
    #),
    path(
        "confirm-account/<str:phone>/",
        patient_views.confirm_account,
        name="confirm_account",
    ),
    # =================================================
    # Dashboard
    path(
        "dashboard/",
        patient_views.dashboard,
        name="patient_dashboard",
    ),
    # =================================================
    # All Services and Booking
    path(
        "all-services/",
        patient_views.all_services,
        name="patient_all_services",
    ),
    path(
        "all-services/book_doctor/",
        patient_views.book_doctor,
        name="patient_book_doctor",
    ),
    path(
        "all-services/book_nurse/",
        patient_views.book_nurse,
        name="patient_book_nurse",
    ),
    path(
        "all-services/book_physio/",
        patient_views.book_physio,
        name="patient_book_physio",
    ),
    path(
        "all-services/book_analytic/",
        patient_views.book_analytic,
        name="patient_book_analytic",
    ),
    path(
        "all-services/book_medicine/",
        patient_views.book_medicine,
        name="patient_book_medicine",
    ),
    path(
        "all-services/book-meeting/",
        patient_views.book_meeting,
        name="patient_book_meeting",
    ),
    path(
        "all-services/meeting-room/<str:room>",
        patient_views.meeting_room,
        name="meeting_room",
    ),
    # =================================================
    # All Details
    path(
        "all-booking-doctors/",
        patient_views.all_booking_doctors,
        name="patient_all_booking_doctors",
    ),
    path(
        "all-booking-nurses/",
        patient_views.all_booking_nurses,
        name="patient_all_booking_nurses",
    ),
    path(
        "all-booking-physio/",
        patient_views.all_booking_physio,
        name="patient_all_booking_physio",
    ),
    path(
        "all-booking-analytics/",
        patient_views.all_booking_analytics,
        name="patient_all_booking_analytics",
    ),
    path(
        "all-booking-medicines/",
        patient_views.all_booking_medicines,
        name="patient_all_booking_medicines",
    ),
    # Services
    path(
        "api/get-self-address",
        patient_views.get_user_address,
        name="get_user_address",
    ),
    path(
        "api/list-service-doctors",
        patient_views.list_service_doctors,
        name="list_service_doctors",
    ),
    path(
        "api/list-nurses",
        patient_views.list_nurses,
        name="list_nurses",
    ),
    path(
        "api/list-physio",
        patient_views.list_physio,
        name="list_physio",
    ),
    path(
        "api/list-labs",
        patient_views.list_labs,
        name="list_labs",
    ),
    path(
        "api/list-pharma",
        patient_views.list_medicines,
        name="list_medicines",
    ),
    path(
        "api/get-booking-slots",
        patient_views.get_booking_slots,
        name="get_booking_slots",
    ),
    path(
        "api/get_times_nurse",
        patient_views.get_times_nurse,
        name="get_times_nurse",
    ),
    path(
        "api/get_times_physio",
        patient_views.get_times_physio,
        name="get_times_physio",
    ),
]
