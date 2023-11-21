from django.shortcuts import render
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mobaderapp.models import (
    PharmacyMedicine,
    PharmacyUser,
    PharmacyDetail,
    BookMedicine,
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


# Create your views here.
def dashboard(request):
    return render(request, "pharma/en/home.html")


class MedicineListView(ListView):
    model = PharmacyMedicine
    template_name = "pharma/en/medicine_list.html"


class MedicineCreate(SuccessMessageMixin, CreateView):
    model = PharmacyMedicine
    success_message = "Medicine Added!"
    fields = ["title", "count", "image", "details", "price"]
    template_name = "pharma/en/medicine_create.html"

    def form_valid(self, form):
        medicine = form.save(commit=False)
        print(self.request.user.id)
        admin = PharmacyUser.objects.get(auth_user_id=self.request.user.id)
        medicine.pharmacy = PharmacyDetail.objects.get(
            admin_id= admin.id
        )
        print(medicine)
        medicine.save()
        messages.success(self.request, "Medicine Created Successfully")
        return HttpResponseRedirect(reverse("pharma_medicine_list"))


class MedicineUpdate(UpdateView):
    model = PharmacyMedicine
    success_message = "Medicine Updated!"
    fields = ["title", "count", "image", "details", "price"]
    template_name = "pharma/en/medicine_update.html"


class MedicineDeleteView(DeleteView):
    model = PharmacyMedicine
    success_message = "Medicine Deleted!"
    template_name = "pharma/en/medicine_delete.html"
    success_url = reverse_lazy("pharma_medicine_list")


class PharmaDetailListView(ListView):
    model = PharmacyDetail
    template_name = "pharma/en/pharma_detail.html"


class PharmaDetailCreate(SuccessMessageMixin, CreateView):
    model = PharmacyDetail
    success_message = "Pharmacy Added!"
    fields = [
        "name",
        "thumbnail",
        "description",
        "mobile_phone",
        "address",
        "open_time",
        "close_time",
    ]
    template_name = "pharma/en/pharma_create.html"

    def form_valid(self, form):
        pharma_detail = form.save(commit=False)
        pharma_detail.admin = PharmacyUser.objects.get(
            auth_user_id=self.request.user.id
        )
        pharma_detail.save()
        messages.success(self.request, "Pharmacy Created Successfully")
        return HttpResponseRedirect(reverse("pharma_detail"))


class PharmaDetailUpdate(UpdateView):
    model = PharmacyDetail
    success_message = "Pharmacy Detail Updated!"
    fields = [
        "name",
        "thumbnail",
        "description",
        "mobile_phone",
        "address",
        "open_time",
        "close_time",
    ]
    template_name = "pharma/en/pharma_update.html"


class PharmaDetialDeleteView(DeleteView):
    model = PharmacyDetail
    success_message = "Pharmacy Deleted!"
    template_name = "pharma/en/pharma_delete.html"
    success_url = reverse_lazy("pharma_detail")


# Bookings
def booking_pending(request):
    context = {}
    pharma_user = PharmacyUser.objects.get(auth_user_id=request.user.id)
    pharma = PharmacyDetail.objects.get(admin_id=pharma_user.id)
    book_medicine = BookMedicine.objects.filter(pharma_id=pharma.id, status="PEN")
    context["bookmedicine"] = book_medicine
    return render(request, "pharma/en/booking_pending.html", context)


def booking_list(request):
    context = {}
    pharma_user = PharmacyUser.objects.get(auth_user_id=request.user.id)
    pharma = PharmacyDetail.objects.get(admin_id=pharma_user.id)
    book_medicine = BookMedicine.objects.filter(pharma_id=pharma.id)
    context["bookmedicine"] = book_medicine
    return render(request, "pharma/en/all_booking.html", context)


class BookingUpdate(UpdateView):
    model = BookMedicine
    success_message = "Book Updated!"
    fields = ["status"]
    template_name = "pharma/en/booking_update.html"
