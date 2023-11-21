from django.urls import path 
from . import views 
urlpatterns = [
    path("", views.dashboard, name="lab_dashboard"),
    path("services_list/", views.ServicesListView.as_view(), name="lab_services_list"),
    path("service_create/", views.ServicesCreate.as_view(), name="lab_service_create"),
    path("service_update/<int:pk>/", views.ServicesUpdate.as_view(),
         name="lab_service_update", ),
    path(
        "service_delete/<int:pk>/",
        views.ServiceDeleteView.as_view(),
        name="lab_service_delete",
    ),
    path("lab_detail/", views.LapDetailListView.as_view(), name="lab_detail"),
    path("lab_detail_create/", views.LabDetailCreate.as_view(), name="lab_detail_create"),
    path("lab_detail_update/<int:pk>/", views.LabDetailUpdate.as_view(),
         name="lab_detail_update", ),
    path(
        "lab_delete/<int:pk>/",
        views.LabDeleteView.as_view(),
        name="lab_detail_delete",
    ),
]
