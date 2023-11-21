import calendar
from datetime import datetime, timedelta, date
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import ListView, UpdateView

from mobaderapp.utils import Calendar
from .forms import EventForm
from .models import DoctorTimes, DoctorUser, BookDoctor


def dashboard(request):
    return render(request, "en/doctor/home.html")


# New Appointment
class AppointmentListView(ListView):
    model = DoctorTimes
    template_name = "en/doctor/appointment_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


def event(request, event_id=None):
    doctor = DoctorUser.objects.get(auth_user_id=request.user.id)
    instance = DoctorTimes(doctor=doctor)
    if event_id:
        instance = get_object_or_404(DoctorTimes, pk=event_id)
    else:
        instance = DoctorTimes(doctor=doctor)
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("appoint_list"))
    return render(request, "en/doctor/appointment_create.html", {"form": form})


# Bookings
def booking_pending(request):
    context = {}
    doctor = DoctorUser.objects.get(auth_user_id=request.user.id)
    book_doctor = BookDoctor.objects.filter(doctor_id=doctor.id, status="PEN")
    context["bookdoctors"] = book_doctor
    return render(request, "en/doctor/booking_pending.html", context)


def booking_list(request):
    context = {}
    doctor = DoctorUser.objects.get(auth_user_id=request.user.id)
    book_doctor = BookDoctor.objects.filter(doctor_id=doctor.id)
    context["bookdoctors"] = book_doctor
    return render(request, "en/doctor/all_booking.html", context)


class BookingUpdate(UpdateView):
    model = BookDoctor
    success_message = "Book Updated!"
    fields = ["status"]
    template_name = "en/doctor/booking_update.html"


@login_required
def meeting_room(request, room):
    context = {"agora_id": settings.AGORA_APP_ID, "room": room}
    return render(request, "en/doctor/meeting_room.html", context)
