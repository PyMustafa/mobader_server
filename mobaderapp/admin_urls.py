from django.urls import path

from . import admin_views

urlpatterns = [
    # ========================================================
    # PAGE FOR ADMIN
    path(
        "admin_home/",
        admin_views.admin_home,
        name="admin_home",
    ),
    # ========================================================
    # Sliders
    path(
        "sliders/",
        admin_views.SliderListView.as_view(),
        name="sliders",
    ),
    path(
        "slider_create/",
        admin_views.SliderCreate.as_view(),
        name="slider_create",
    ),
    path(
        "slider_update/<int:pk>/",
        admin_views.SliderUpdate.as_view(),
        name="slider_update",
    ),
    path(
        "slider_delete/<int:pk>/",
        admin_views.SliderDeleteView.as_view(),
        name="slider_delete",
    ),
    # ========================================================
    # Media Center
    path(
        "media/",
        admin_views.MediaListView.as_view(),
        name="media",
    ),
    path(
        "media_create/",
        admin_views.MediaCreate.as_view(),
        name="media_create",
    ),
    path(
        "media_update/<int:pk>/",
        admin_views.MediaUpdate.as_view(),
        name="media_update",
    ),
    path(
        "media_delete/<int:pk>/",
        admin_views.MediaDeleteView.as_view(),
        name="media_delete",
    ),
    # ========================================================
    # Team Slider
    path(
        "team/",
        admin_views.TeamListView.as_view(),
        name="team",
    ),
    path(
        "team_create/",
        admin_views.TeamCreate.as_view(),
        name="team_create",
    ),
    path(
        "team_delete/<int:pk>/",
        admin_views.TeamDeleteView.as_view(),
        name="team_delete",
    ),
    # ========================================================
    # Events Slider
    path(
        "event/",
        admin_views.EventListView.as_view(),
        name="event",
    ),
    path(
        "event_create/",
        admin_views.EventCreate.as_view(),
        name="event_create",
    ),
    path(
        "event_delete/<int:pk>/",
        admin_views.EventDeleteView.as_view(),
        name="event_delete",
    ),
    # ========================================================
    # Gallery Images
    path(
        "gallery/",
        admin_views.GalleryListView.as_view(),
        name="gallery",
    ),
    path(
        "image_create/",
        admin_views.ImageCreate.as_view(),
        name="image_create",
    ),
    path(
        "image_delete/<int:pk>/",
        admin_views.ImageDeleteView.as_view(),
        name="image_delete",
    ),
    # ========================================================
    # Categories Doctors
    path(
        "categories_doctor/",
        admin_views.CategoriesListView.as_view(),
        name="categories_doctor",
    ),
    path(
        "category_create/",
        admin_views.CategoriesCreate.as_view(),
        name="category_create",
    ),
    path(
        "category_update/<int:pk>/",
        admin_views.CategoriesUpdate.as_view(),
        name="category_update",
    ),
    path(
        "category_delete/<int:pk>/",
        admin_views.CategoriesDeleteView.as_view(),
        name="category_delete",
    ),
    # ========================================================
    # Staff User
    path(
        "staff_list/",
        admin_views.StaffUserListView.as_view(),
        name="staff_list",
    ),
    path(
        "staff_create/",
        admin_views.StaffUserCreateView.as_view(),
        name="staff_create",
    ),
    # ========================================================
    # Doctor User
    path(
        "doctor_list/",
        admin_views.DoctorUserListView.as_view(),
        name="doctor_list",
    ),
    path(
        "doctor_create/",
        admin_views.DoctorUserCreateView.as_view(),
        name="doctor_create",
    ),
    path(
        "doctor_update/<int:pk>/",
        admin_views.DoctorUpdate.as_view(),
        name="doctor_update",
    ),
    # ========================================================
    # Nurses
    path(
        "nurse_list/",
        admin_views.NurseUserListView.as_view(),
        name="nurse_list",
    ),
    path(
        "nurse_create/",
        admin_views.NurseUserCreateView.as_view(),
        name="nurse_create",
    ),
    path(
        "nurse_update/<int:pk>/",
        admin_views.NurseUpdate.as_view(),
        name="nurse_update",
    ),
    # ========================================================
    # Lab Admins
    path(
        "lab_list/",
        admin_views.LabUserListView.as_view(),
        name="lab_list",
    ),
    path(
        "lab_create/",
        admin_views.LabUserCreateView.as_view(),
        name="lab_create",
    ),
    path(
        "lab_update/<int:pk>/",
        admin_views.LabUpdate.as_view(),
        name="lab_update",
    ),
    # ========================================================
    # Pharmacy Admins
    path(
        "pharma_list/",
        admin_views.PharmaUserListView.as_view(),
        name="pharma_list",
    ),
    path(
        "pharma_create/",
        admin_views.PharmaUserCreateView.as_view(),
        name="pharma_create",
    ),
    path(
        "pharma_update/<int:pk>/",
        admin_views.PharmaUpdate.as_view(),
        name="pharma_update",
    ),
    # ========================================================
    # Physiotherapist
    path(
        "physio_list/",
        admin_views.PhysiotherapistUserListView.as_view(),
        name="physio_list",
    ),
    path(
        "physio_create/",
        admin_views.PhysiotherapistUserCreateView.as_view(),
        name="physio_create",
    ),
    path(
        "physio_update/<int:pk>/",
        admin_views.PhysiotherapistUpdate.as_view(),
        name="physio_update",
    ),
    # ========================================================
    # Patient
    path(
        "patient_list/",
        admin_views.PatientUserListView.as_view(),
        name="patient_list",
    ),
    # TODO: Add services for nurse, lab, physiotherapist
]
