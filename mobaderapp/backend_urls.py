from django.urls import path

from . import backend_views as views


urlpatterns = [
    # Authentication urls
    path('register-patient/', views.PatientUserCreateView.as_view(), name='api-register-patient'),
    path('verify-otp/', views.UserVerifyOTPView.as_view(), name='api-verify-otp'),
    path('login/', views.UserLoginAPIView.as_view(), name='api-login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api-logout'),

    # reset password urls
    path("reset-password-request/", views.ResetPassRequestView.as_view(), name="reset-password-request"),
    path("reset-password/", views.ResetPassView.as_view(), name="reset-password-request"),

    # Book Doctor urls
    path("book-doctor/", views.BookDoctorCreateAPIView.as_view(), name="book-doctor"),
    path("doctor-bookings/", views.DoctorBookingsListAPIView.as_view(), name="doctor-bookings"),
    path("doctor-bookings/<int:pk>/", views.DoctorBookingRetrieveAPIView.as_view(), name="doctor-booking"),
    path("cat/", views.CategoryListAPIView.as_view(), name="category-all"),
    path("cat/<int:pk>/", views.CategoryAPIView.as_view(), name="category"),
    path("cat/<int:pk>/doctors/", views.get_doctors, name="category-doctors"),


    # tap payment
    path('tap-webhook/', views.TapWebhookView.as_view(), name='tap_webhook'),
    path('tap-payment-status/<str:charge_id>/', views.TapPaymentStatus.as_view(), name='tap-payment-status'),

    # Offers
    path('doctor-offers/', views.DoctorOffersListAPIView.as_view(), name='doctor-offers'),
    path('doctor-offers/<int:pk>', views.DoctorOffersRetrieveAPIView.as_view(), name='doctor-offer-details'),

    path('nurse-offers/', views.NurseOffersListAPIView.as_view(), name='nurse-offers'),
    path('nurse-offers/<int:pk>', views.NurseOffersRetrieveAPIView.as_view(), name='nurse-offer-details'),

    path('physio-offers/', views.PhysioOffersListAPIView.as_view(), name='Physio-offers'),
    path('physio-offers/<int:pk>', views.PhysioOffersRetrieveAPIView.as_view(), name='Physio-offer-details'),

    path('lab-offers/', views.LabOffersListAPIView.as_view(), name='lab-offers'),
    path('lab-offers/<int:pk>', views.LabOffersRetrieveAPIView.as_view(), name='lab-offer-details'),

    # Nurse & Nurse booking urls
    path("nurses/", views.NurseListAPIView.as_view(), name="nurses"),
    path("nurse-services/", views.NurseServiceListAPIView.as_view(), name="nurse-services"),
    path("nurse-service-times/", views.NurseServiceTimesListAPIView.as_view(), name="nurse-service-times"),
    path("book-nurse/", views.BookNurseAPIView.as_view(), name="book-nurse"),
    path("nurse-bookings/", views.NurseBookingsListAPIView.as_view(), name="nurse-bookings"),
    path("nurse-bookings/<int:pk>/", views.NurseBookingRetrieveAPIView.as_view(), name="nurse-booking-detail"),
    path("nurse-service/<int:service_id>/times/", views.NurseServiceAllTimesListAPIView.as_view(), name="service-times"),

    # physio & physio booking urls
    path("physio/", views.PhysioListAPIView.as_view(), name="physio-all"),
    path("physio-service/", views.PhysioServiceListAPIView.as_view(), name="physio-service-all"),
    path("physio-service-times/", views.PhysioServiceTimesListAPIView.as_view(), name="physio-service-times"),
    path("book-physio/", views.BookPhysioAPIView.as_view(), name="book-physio"),
    path("physio-bookings/", views.PhysioBookingsListAPIView.as_view(), name="physio-bookings"),
    path("physio-bookings/<int:pk>/", views.PhysioBookingRetrieveAPIView.as_view(), name="physio-booking-detail"),
    path("physio-service/<int:service_id>/times/", views.PhysioServiceAllTimesListAPIView.as_view(), name="physioservice-time"),

    # pharmacy & medicine booking urls
    path("pharmacist/", views.PharmacyUserListAPIView.as_view(), name="pharmacist-all"),
    path("medicine-all/", views.PharmacyMedicineListAPIView.as_view(), name="medicine-all"),
    path("pharmacy/", views.PharmacyListAPIView.as_view(), name="pharmacy"),
    path("book-medicine/", views.BookMedicineAPIView.as_view(), name="book-medicine"),

    # lab & analytic booking urls
    path("lab-admins/", views.LabUserListAPIView.as_view(), name="lab-admins"),
    path("lab-admins/<int:pk>/", views.LabUserRetrieveAPIView.as_view(), name="lab-admin-details"),

    path("lab-services/", views.LabServiceListAPIView.as_view(), name="lab-services"),
    path("lab-services/<int:pk>/", views.LabServiceRetrieveAPIView.as_view(), name="lab-service-details"),

    path("labs/", views.LabListAPIView.as_view(), name="labs"),
    path("labs/<int:pk>/", views.LabRetrieveAPIView.as_view(), name="lab-details"),

    path("book-analytic/", views.BookAnalyticAPIView.as_view(), name="book-analytic"),
    path("lab-bookings/", views.LabBookingsListAPIView.as_view(), name="lab-bookings"),
    path("lab-bookings/<int:pk>/", views.LabBookingRetrieveAPIView.as_view(), name="lab-booking-detail"),

    path("sliders/", views.SliderList.as_view(), name="sliders"),
    path("doctors/", views.DoctorList.as_view()),
    path("doctors/<int:cat>/", views.DoctorListFilteredCategory.as_view(), name="list_cat_doctors"),
    path("doctor/<int:pk>/", views.DoctorDetail.as_view()),
    path("doctor-times/<int:pk>/", views.DoctorTimesList.as_view()),
    path("patients/", views.PatientList.as_view()),
    path("patient/<int:pk>/", views.PatientDetail.as_view()),
    path("books/", views.BookDoctorList.as_view()),
]