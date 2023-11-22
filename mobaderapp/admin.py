from django.contrib import admin

from .models import (
    StaffUser,
    DoctorCategory,
    DoctorUser,
    Offer,
    OfferDoctor,
    OfferOrder,

)

admin.site.register(StaffUser)
admin.site.register(DoctorCategory)
admin.site.register(DoctorUser)
admin.site.register(Offer)
admin.site.register(OfferDoctor)
admin.site.register(OfferOrder)
