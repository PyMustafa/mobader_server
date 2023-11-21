from django.contrib import admin

from .models import (
    StaffUser,
    DoctorCategory,
    DoctorUser,
)

admin.site.register(StaffUser)
admin.site.register(DoctorCategory)
admin.site.register(DoctorUser)
