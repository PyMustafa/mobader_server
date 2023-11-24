from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import (
    DoctorCategory,
    CustomUser,
    DoctorUser,
    StaffUser,
    NurseUser,
    PhysiotherapistUser,
    PharmacyUser,
    LapUser,
    PatientUser,
    Slider,
    ImageGallery,
    MediaCenter,
    TeamSlider,
    EventSlider,
)


@login_required(login_url="admin_login")
def admin_home(request):
    context = {
        "num_staff": StaffUser.objects.count(),
        "num_doctors": DoctorUser.objects.count(),
        "num_nurses": NurseUser.objects.count(),
        "num_physiotherapist": PhysiotherapistUser.objects.count(),
        "num_pharmacy": PharmacyUser.objects.count(),
        "num_laps": LapUser.objects.count(),
        "num_patients": PatientUser.objects.count(),
    }
    return render(request, "en/admin/home.html", context)


# ========================================================
# Slider Items


class SliderListView(ListView):
    model = Slider
    template_name = "en/admin/slider_list.html"


class SliderCreate(SuccessMessageMixin, CreateView):
    model = Slider
    success_message = "Slider Added!"
    fields = "__all__"
    template_name = "en/admin/slider_create.html"


class SliderUpdate(UpdateView):
    model = Slider
    success_message = "Slider Updated!"
    fields = "__all__"
    template_name = "en/admin/slider_update.html"


class SliderDeleteView(DeleteView):
    model = Slider
    success_message = "Slider Deleted!"
    template_name = "en/admin/slider_delete.html"
    success_url = reverse_lazy("sliders")
    
# ========================================================
# Media Items


class MediaListView(ListView):
    model = MediaCenter
    template_name = "en/admin/media_list.html"


class MediaCreate(SuccessMessageMixin, CreateView):
    model = MediaCenter
    success_message = "Media Added!"
    fields = "__all__"
    template_name = "en/admin/media_create.html"


class MediaUpdate(UpdateView):
    model = MediaCenter
    success_message = "Media Updated!"
    fields = "__all__"
    template_name = "en/admin/media_update.html"


class MediaDeleteView(DeleteView):
    model = MediaCenter
    success_message = "Media Deleted!"
    template_name = "en/admin/media_delete.html"
    success_url = reverse_lazy("media")

# ========================================================
# Team Images
class TeamListView(ListView):
    model = TeamSlider
    template_name = "en/admin/team_list.html"


class TeamCreate(SuccessMessageMixin, CreateView):
    model = TeamSlider
    success_message = "Team Added!"
    fields = "__all__"
    template_name = "en/admin/team_create.html"


class TeamDeleteView(DeleteView):
    model = TeamSlider
    success_message = "Team Deleted!"
    template_name = "en/admin/team_delete.html"
    success_url = reverse_lazy("team")
    
# ========================================================
# Event Images
class EventListView(ListView):
    model = EventSlider
    template_name = "en/admin/event_list.html"


class EventCreate(SuccessMessageMixin, CreateView):
    model = EventSlider
    success_message = "Event Added!"
    fields = "__all__"
    template_name = "en/admin/event_create.html"


class EventDeleteView(DeleteView):
    model = EventSlider
    success_message = "Event Deleted!"
    template_name = "en/admin/event_delete.html"
    success_url = reverse_lazy("event")
    

# ========================================================
# Gallery Images
class GalleryListView(ListView):
    model = ImageGallery
    template_name = "en/admin/gallery_list.html"


class ImageCreate(SuccessMessageMixin, CreateView):
    model = ImageGallery
    success_message = "Image Added!"
    fields = "__all__"
    template_name = "en/admin/gallery_create.html"


class ImageDeleteView(DeleteView):
    model = ImageGallery
    success_message = "Image Deleted!"
    template_name = "en/admin/gallery_delete.html"
    success_url = reverse_lazy("gallery")


# ========================================================
# Category of Doctors
class CategoriesListView(ListView):
    model = DoctorCategory
    template_name = "en/admin/category_list.html"


class CategoriesCreate(SuccessMessageMixin, CreateView):
    model = DoctorCategory
    success_message = "Category Added!"
    fields = "__all__"
    template_name = "en/admin/category_create.html"


class CategoriesUpdate(UpdateView):
    model = DoctorCategory
    success_message = "Category Updated!"
    fields = "__all__"
    template_name = "en/admin/category_update.html"


class CategoriesDeleteView(DeleteView):
    model = DoctorCategory
    success_message = "Category Deleted!"
    template_name = "en/admin/category_delete.html"
    success_url = reverse_lazy("categories_doctor")


# ========================================================
# Staff
class StaffUserListView(ListView):
    model = StaffUser
    template_name = "en/admin/staff/staff_list.html"


class StaffUserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "Staff Created!"
    fields = ["first_name", "last_name", "username", "email", "password"]
    template_name = "en/admin/staff/staff_create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 2
        user.set_password(form.cleaned_data["password"])
        user.save()
        # ========================
        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        user.staffuser.profile_pic = profile_pic_url
        user.staffuser.save()
        messages.success(self.request, "Staff Created Successfully")
        return HttpResponseRedirect(reverse("staff_list"))


# ========================================================
# Doctor User
class DoctorUserListView(ListView):
    model = DoctorUser
    template_name = "en/admin/doctors/doctor_list.html"


class DoctorUpdate(UpdateView):
    model = DoctorUser
    success_message = "Doctor Updated!"
    fields = ["price", "address"]
    template_name = "en/admin/doctors/doctor_update.html"


class DoctorUserCreateView(SuccessMessageMixin, CreateView):
    model = DoctorUser
    success_message = "Doctor Created!"
    fields = ["mobile", "password", "first_name", "last_name", "username", "email", "price", "address"]
    template_name = "en/admin/doctors/doctor_create.html"

    def get_context_data(self, **kwargs):
        context = super(DoctorUserCreateView, self).get_context_data(**kwargs)
        context["categories"] = DoctorCategory.objects.all()
        return context
        
    def form_valid(self, form):
        user = form.save(commit=False)
        #user.is_active = True
        user.user_type = 3
        user.set_password(form.cleaned_data["password"])
        #user.save()
        # Saving Doctor User
        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = filename

        user.profile_pic = profile_pic_url
        user.category_id = DoctorCategory.objects.filter(
            id=self.request.POST.get("category")
        ).first()
        user.save()
        messages.success(self.request, "Doctor Created Successfully")
        return HttpResponseRedirect(reverse("doctor_list"))

    


# ========================================================
# Nurse User
class NurseUserListView(ListView):
    model = NurseUser
    template_name = "en/admin/nurses/nurse_list.html"


class NurseUpdate(UpdateView):
    model = NurseUser
    success_message = "Nurse Updated!"
    fields = ["mobile", "address"]
    template_name = "en/admin/nurses/nurse_update.html"


class NurseUserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "Nurse Created!"
    fields = ["first_name", "last_name", "username", "email", "password"]
    template_name = "en/admin/nurses/nurse_create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 4
        user.set_password(form.cleaned_data["password"])
        user.save()
        # Saving Nurse User
        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        user.nurseuser.profile_pic = profile_pic_url
        user.nurseuser.hospital_name = self.request.POST.get("hospital_name")
        user.nurseuser.mobile = self.request.POST.get("mobile")
        user.nurseuser.address = self.request.POST.get("address")
        user.nurseuser.save()
        messages.success(self.request, "Nurse Created Successfully")
        return HttpResponseRedirect(reverse("nurse_list"))


# ========================================================
# Lab Admins
class LabUserListView(ListView):
    model = LapUser
    template_name = "en/admin/lab/lab_list.html"


class LabUpdate(UpdateView):
    model = LapUser
    success_message = "Lab Admin Updated!"
    fields = ["mobile", "address"]
    template_name = "en/admin/lab/lab_update.html"


class LabUserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "Lap Admin Created!"
    fields = ["first_name", "last_name", "username", "email", "password"]
    template_name = "en/admin/lab/lab_create.html"

    def form_valid(self, form):
        # Saving Custom User Object for Nurse User
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 5
        user.set_password(form.cleaned_data["password"])
        user.save()
        # Saving Nurse User
        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        user.lapuser.profile_pic = profile_pic_url
        user.lapuser.mobile = self.request.POST.get("mobile")
        user.lapuser.address = self.request.POST.get("address")
        user.lapuser.save()
        messages.success(self.request, "Lab Admin Created Successfully")
        return HttpResponseRedirect(reverse("lab_list"))


# ========================================================
# Pharmacy Admins
class PharmaUserListView(ListView):
    model = PharmacyUser
    template_name = "en/admin/pharma/pharma_list.html"


class PharmaUpdate(UpdateView):
    model = PharmacyUser
    success_message = "Pharmacy Admin Updated!"
    fields = ["mobile", "address"]
    template_name = "en/admin/pharma/pharma_update.html"


class PharmaUserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "Pharmacy Admin Created!"
    fields = ["first_name", "last_name", "username", "email", "password"]
    template_name = "en/admin/pharma/pharma_create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 6
        user.set_password(form.cleaned_data["password"])
        user.save()
        # ========================
        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        user.pharmacyuser.profile_pic = profile_pic_url
        user.pharmacyuser.mobile = self.request.POST.get("mobile")
        user.pharmacyuser.address = self.request.POST.get("address")
        user.pharmacyuser.save()
        messages.success(self.request, "Pharmacy Admin Created Successfully")
        return HttpResponseRedirect(reverse("pharma_list"))


# ========================================================
# Physiotherapist
class PhysiotherapistUserListView(ListView):
    model = PhysiotherapistUser
    template_name = "en/admin/physio/physio_list.html"


class PhysiotherapistUpdate(UpdateView):
    model = PhysiotherapistUser
    success_message = "Physiotherapist Updated!"
    fields = ["mobile_phone", "address"]
    template_name = "en/admin/physio/physio_update.html"


class PhysiotherapistUserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "Physiotherapist Created!"
    fields = ["first_name", "last_name", "username", "email", "password"]
    template_name = "en/admin/physio/physio_create.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 7
        user.set_password(form.cleaned_data["password"])
        user.save()
        # ========================
        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        user.physiotherapistuser.profile_pic = profile_pic_url
        user.physiotherapistuser.hospital_name = self.request.POST.get("hospital_name")
        user.physiotherapistuser.mobile_phone = self.request.POST.get("mobile_phone")
        user.physiotherapistuser.address = self.request.POST.get("address")
        user.physiotherapistuser.save()
        messages.success(self.request, "Physiotherapist Created Successfully")
        return HttpResponseRedirect(reverse("physio_list"))


# ========================================================
# Patient
class PatientUserListView(ListView):
    model = PatientUser
    template_name = "en/admin/patient/patient_list.html"
