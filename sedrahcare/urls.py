from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    # Main Pages
    path("", include("mobaderapp.pages_urls")),
    path("api/v1/", include("mobaderapp.backend_urls")),
    path("api-auth/", include("rest_framework.urls")),
    # Admin Pages
    path("admin/", include("mobaderapp.admin_urls")),
    path("patient/", include("mobaderapp.patient_urls")),
    path("doctor/", include("mobaderapp.doctor_urls")),
    path("nurse/", include("nurse.urls")),
    path("physio/", include("physiotherapist.urls")),
    path("lab/", include("lab.urls")),
    path("pharma/", include("pharma.urls")),
    path("chatroom/", include("chatroom.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

