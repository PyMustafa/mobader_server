from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


# ===========================================
# Media
class MediaCenter(models.Model):
    title = models.CharField(max_length=200)
    video = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("media")


# ===========================================
# Team
class TeamSlider(models.Model):
    image = models.FileField()

    def get_absolute_url(self):
        return reverse("team")


# ===========================================
# Events
class EventSlider(models.Model):
    image = models.FileField()

    def get_absolute_url(self):
        return reverse("event")


# ===========================================
# Doctor Category { القلب ، الامراض الصدريه }
class DoctorCategory(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    url_slug = models.CharField(max_length=200)
    thumbnail = models.FileField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("categories_doctor")


# ===========================================
# All Users
class CustomUser(AbstractUser):
    user_type_choices = (
        (1, "Admin"),
        (2, "Staff"),
        (3, "Doctor"),
        (4, "Nurse"),
        (5, "Lap"),
        (6, "Pharmacy"),
        (7, "Physiotherapist"),
        (8, "Patient"),
    )
    user_type = models.CharField(max_length=2, choices=user_type_choices, default=8)


class AdminUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    created_at = models.DateTimeField(auto_now_add=True)


class StaffUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("staff_list")


class DoctorUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    category_id = models.ForeignKey(
        DoctorCategory,
        on_delete=models.CASCADE,
        related_name="doctor_category",
        null=True,
    )
    profile_pic = models.FileField(default="")
    price = models.FloatField(default=0.0)
    hospital_name = models.CharField(max_length=20, default="")
    mobile_phone = models.CharField(max_length=15, default="")
    address = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.auth_user_id.username

    def get_absolute_url(self):
        return reverse("doctor_list")


class NurseUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    hospital_name = models.CharField(max_length=20, default="")
    address = models.CharField(max_length=255, default="")
    mobile = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("nurse_list")


class LapUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    address = models.CharField(max_length=255, default="")
    mobile = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("lab_list")


class PharmacyUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    address = models.CharField(max_length=255, default="")
    mobile = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("pharma_list")


class PhysiotherapistUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="")
    hospital_name = models.CharField(max_length=20, default="")
    mobile_phone = models.CharField(max_length=15, default="")
    address = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("physio_list")


class PatientUser(models.Model):
    auth_user_id = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_pic = models.FileField(default="", blank=True, null=True, )
    mobile = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255, default="")
    verification = models.CharField(max_length=7)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.auth_user_id.username

    def get_absolute_url(self):
        return reverse("login")


# =========================================================
# Doctor Times
class DoctorTimes(models.Model):
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(
        DoctorUser,
        on_delete=models.CASCADE,
        related_name="doctor_times",
    )
    title = models.CharField(max_length=200, blank=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.start_time)

    @property
    def get_html_url(self):
        url = reverse("appoint_edit", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


# ============================================================
# Nurse Service
class NurseService(models.Model):
    id = models.AutoField(primary_key=True)
    nurse = models.ForeignKey(
        NurseUser, on_delete=models.CASCADE, related_name="nurse_service"
    )
    title = models.CharField(max_length=200)
    details = models.TextField(null=True)
    price = models.FloatField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("nurse_services_list")


class NurseServiceTimes(models.Model):
    id = models.AutoField(primary_key=True)
    service = models.ForeignKey(
        NurseService, on_delete=models.CASCADE, related_name="nurse_service_time"
    )
    day = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-day"]

    def get_absolute_url(self):
        return reverse("nurse_services_times_list")


# ============================================================
# Lap Details
class LabDetail(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(
        LapUser, on_delete=models.CASCADE, related_name="lap_user"
    )
    name = models.CharField(max_length=250)
    thumbnail = models.FileField()
    description = models.TextField()
    mobile_phone = models.CharField(max_length=15)
    address = models.TextField(null=True)
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("lab_detail")


class LabService(models.Model):
    id = models.AutoField(primary_key=True)
    lap = models.ForeignKey(
        LabDetail,
        on_delete=models.CASCADE,
        related_name="lap_service",
    )
    title = models.CharField(max_length=200)
    image = models.FileField(null=True)
    details = models.TextField(null=True)
    price = models.FloatField()

    def get_absolute_url(self):
        return reverse("lab_services_list")


# =============================================================
# Pharmacy Details


class PharmacyDetail(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(
        PharmacyUser, on_delete=models.CASCADE, related_name="pharmacy_user"
    )
    name = models.CharField(max_length=250)
    thumbnail = models.FileField()
    description = models.TextField()
    mobile_phone = models.CharField(max_length=15)
    address = models.TextField(null=True)
    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PharmacyMedicine(models.Model):
    id = models.AutoField(primary_key=True)
    pharmacy = models.ForeignKey(
        PharmacyDetail,
        on_delete=models.CASCADE,
        related_name="pharmacy_medicine",
    )
    title = models.CharField(max_length=200)
    count = models.IntegerField(default=1)
    image = models.FileField(null=True)
    details = models.TextField(null=True)
    price = models.FloatField()


# ============================================================
# Physiotherapist Service
class PhysiotherapistService(models.Model):
    id = models.AutoField(primary_key=True)
    physiotherapist = models.ForeignKey(
        PhysiotherapistUser,
        on_delete=models.CASCADE,
        related_name="physiotherapist_service",
    )
    title = models.CharField(max_length=200)
    details = models.TextField(null=True)
    price = models.FloatField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("physio_services_list")


class PhysiotherapistServiceTimes(models.Model):
    id = models.AutoField(primary_key=True)
    service = models.ForeignKey(
        PhysiotherapistService,
        on_delete=models.CASCADE,
        related_name="physio_service_time",
    )
    day = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-day"]

    def get_absolute_url(self):
        return reverse("physio_services_times_list")


# =============================================================
# Patient Booking
class BookDoctor(models.Model):
    class Status(models.TextChoices):
        PENDING = "PEN", "Pending"
        ACCEPTED = "ACC", "Accepted"
        REFUSED = "REF", "Refused"

    class Type(models.TextChoices):
        VISIT = "VISIT", "Visit"
        MEET = "MEET", "Meet"

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        PatientUser, on_delete=models.CASCADE, related_name="book_doctor"
    )
    doctor = models.ForeignKey(
        DoctorUser, on_delete=models.CASCADE, related_name="doctor_info"
    )
    book_time = models.ForeignKey(
        DoctorTimes, on_delete=models.CASCADE, related_name="book_time_doctor"
    )
    is_paid = models.BooleanField(default=False)
    book_type = models.CharField(max_length=20, choices=Type.choices, default=Type.VISIT, blank=True)
    meeting_room = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(
        max_length=4, choices=Status.choices, default=Status.PENDING, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("doctor_booking_list")


class BookNurse(models.Model):
    class Status(models.TextChoices):
        PENDING = "PEN", "Pending"
        ACCEPTED = "ACC", "Accepted"
        REFUSED = "REF", "Refused"

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        PatientUser, on_delete=models.CASCADE, related_name="book_nurse"
    )
    nurse = models.ForeignKey(
        NurseUser, on_delete=models.CASCADE, related_name="nurse_info"
    )
    service = models.ForeignKey(
        NurseService, on_delete=models.CASCADE, related_name="book_service_nurse"
    )
    time = models.ForeignKey(
        NurseServiceTimes,
        on_delete=models.CASCADE,
        related_name="book_time_nurse_service",
    )
    status = models.CharField(
        max_length=4, choices=Status.choices, default=Status.PENDING, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("nurse_booking_list")


class BookPhysio(models.Model):
    class Status(models.TextChoices):
        PENDING = "PEN", "Pending"
        ACCEPTED = "ACC", "Accepted"
        REFUSED = "REF", "Refused"

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        PatientUser, on_delete=models.CASCADE, related_name="book_physio"
    )
    physio = models.ForeignKey(
        PhysiotherapistUser, on_delete=models.CASCADE, related_name="physio_info"
    )
    service = models.ForeignKey(
        PhysiotherapistService,
        on_delete=models.CASCADE,
        related_name="book_service_physio",
    )
    time = models.ForeignKey(
        PhysiotherapistServiceTimes,
        on_delete=models.CASCADE,
        related_name="book_time_physio_service",
    )
    status = models.CharField(
        max_length=4, choices=Status.choices, default=Status.PENDING, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("physio_booking_list")


class BookAnalytic(models.Model):
    class Status(models.TextChoices):
        PENDING = "PEN", "Pending"
        ACCEPTED = "ACC", "Accepted"
        REFUSED = "REF", "Refused"

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        PatientUser, on_delete=models.CASCADE, related_name="book_analytic"
    )
    lab = models.ForeignKey(
        LabDetail, on_delete=models.CASCADE, related_name="lab_info"
    )
    service = models.ForeignKey(
        LabService, on_delete=models.CASCADE, related_name="book_service_lab"
    )
    status = models.CharField(
        max_length=4, choices=Status.choices, default=Status.PENDING, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("analytic_booking_list")


class BookMedicine(models.Model):
    class Status(models.TextChoices):
        PENDING = "PEN", "Pending"
        ACCEPTED = "ACC", "Accepted"
        REFUSED = "REF", "Refused"

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        PatientUser, on_delete=models.CASCADE, related_name="book_medicine"
    )
    pharma = models.ForeignKey(
        PharmacyDetail, on_delete=models.CASCADE, related_name="pharma_info"
    )
    medicine = models.ForeignKey(
        PharmacyMedicine, on_delete=models.CASCADE, related_name="book_medicine_pharma"
    )
    count = models.IntegerField(default=1)
    status = models.CharField(
        max_length=4, choices=Status.choices, default=Status.PENDING, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("pharma_booking_list")


# ===================================================================
class Slider(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.FileField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("sliders")


class ImageGallery(models.Model):
    thumbnail = models.FileField()

    def get_absolute_url(self):
        return reverse("gallery")


# ===================================================================
class Offer(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.FileField()
    description = models.TextField()
    price = models.FloatField(default=0.0)
    offer_type = models.CharField(max_length=20, default="offerdoctor")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("offers")


class OfferOrder(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="offer_order",
    )
    patient = models.ForeignKey(
        PatientUser,
        on_delete=models.CASCADE,
        related_name="patient_booking_order",
    )

    def __str__(self):
        return self.offer.title


class OfferDoctor(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="offer_doctor",
    )
    doctor = models.ForeignKey(
        DoctorUser,
        on_delete=models.CASCADE,
        related_name="doctor_for_offer",
    )

    def __str__(self):
        return self.offer.title


class OfferNurseService(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="offer_nurse",
    )
    nurse_service = models.ForeignKey(
        NurseService,
        on_delete=models.CASCADE,
        related_name="nurse_service_offer",
    )

    def __str__(self):
        return self.offer.title


class OfferPhysioService(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="offer_physio",
    )
    physio_service = models.ForeignKey(
        PhysiotherapistService,
        on_delete=models.CASCADE,
        related_name="physio_service_offer",
    )

    def __str__(self):
        return self.offer.title


class OfferLabAnalytic(models.Model):
    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="offer_analytic",
    )
    lab_analytic = models.ForeignKey(
        LabService,
        on_delete=models.CASCADE,
        related_name="lab_service_offer",
    )

    def __str__(self):
        return self.offer.title


# ==============================================================
# Manage Users (1, "Admin"), (2, "Staff"), (3, "Doctor"), (4, "Nurse"), (5, "LapAdmin"), (6, "PharmacyAdmin"),
#                          (7, "Physiotherapist"), (8, "Patient")
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminUser.objects.create(auth_user_id=instance)
        if instance.user_type == 2:
            StaffUser.objects.create(auth_user_id=instance)
        if instance.user_type == 3:
            DoctorUser.objects.create(auth_user_id=instance)
        if instance.user_type == 4:
            NurseUser.objects.create(auth_user_id=instance)
        if instance.user_type == 5:
            LapUser.objects.create(auth_user_id=instance)
        if instance.user_type == 6:
            PharmacyUser.objects.create(auth_user_id=instance)
        if instance.user_type == 7:
            PhysiotherapistUser.objects.create(auth_user_id=instance)
        if instance.user_type == 8:
            PatientUser.objects.create(auth_user_id=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminuser.save()
    if instance.user_type == 2:
        instance.staffuser.save()
    if instance.user_type == 3:
        instance.doctoruser.save()
    if instance.user_type == 4:
        instance.nurseuser.save()
    if instance.user_type == 5:
        instance.lapuser.save()
    if instance.user_type == 6:
        instance.pharmacyuser.save()
    if instance.user_type == 7:
        instance.physiotherapistuser.save()
    if instance.user_type == 8:
        instance.patientuser.save()
