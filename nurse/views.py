from django.shortcuts import render 
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mobaderapp.models import NurseService, NurseUser, NurseServiceTimes, BookNurse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


# Create your views here.
def dashboard(request):
    return render(request, "nurse/en/home.html")

class ServicesListView(ListView):
    model = NurseService
    template_name = "nurse/en/service_list.html"


class ServicesCreate(SuccessMessageMixin, CreateView):
    model = NurseService
    success_message = "Service Added!"
    fields = ["title", "details", "price"]
    template_name = "nurse/en/service_create.html"

    
    def form_valid(self, form):
        service = form.save(commit=False)
        service.nurse = NurseUser.objects.get(
            auth_user_id=self.request.user.id
        )
        service.save()
        messages.success(self.request, "Service Created Successfully")
        return HttpResponseRedirect(reverse("nurse_services_list"))



class ServicesUpdate(UpdateView):
    model = NurseService
    success_message = "Service Updated!"
    fields = ["title", "details", "price"]
    template_name = "nurse/en/service_update.html"


class ServiceDeleteView(DeleteView):
    model = NurseService
    success_message = "Service Deleted!"
    template_name = "nurse/en/service_delete.html"
    success_url = reverse_lazy("nurse_services_list")


class ServicesTimesListView(ListView):
    model = NurseServiceTimes
    queryset = NurseServiceTimes.objects.filter(
        active = True
    )
    template_name = "nurse/en/service_time_list.html"

    def get_context_data(self, **kwargs):
        context = super(ServicesTimesListView, self).get_context_data(**kwargs)
        context['services'] = NurseService.objects.all()
        return context


class ServicesTimesCreate(SuccessMessageMixin, CreateView):
    model = NurseServiceTimes
    success_message = "Service Added!"
    fields = ["service", "day", "start_time", "end_time"]
    template_name = "nurse/en/service_time_create.html"

    def get_context_data(self, **kwargs):
        context = super(ServicesTimesCreate, self).get_context_data(**kwargs)
        context['services'] = NurseService.objects.all()
        return context

    
    def form_valid(self, form):
        print(self.request.POST.get('service'))
        service_time = form.save(commit=False)
        service_time.service = NurseService.objects.get(
            id=self.request.POST.get('service')
        )
        service_time.active = True
        service_time.save()
        messages.success(self.request, "Service Time Created Successfully")
        return HttpResponseRedirect(reverse("nurse_services_times_list"))



class ServicesTimeUpdate(UpdateView):
    model = NurseServiceTimes
    success_message = "Service Time Updated!"
    fields = [ "day", "start_time", "end_time"]
    template_name = "nurse/en/service_time_update.html"


class ServiceTimeDeleteView(DeleteView):
    model = NurseServiceTimes
    success_message = "Service Deleted!"
    template_name = "nurse/en/service_time_delete.html"
    success_url = reverse_lazy("nurse_services_times_list")

# Bookings
def booking_pending(request):
    context = {}
    nurse = NurseUser.objects.get(
        auth_user_id = request.user.id
    )
    book_nurse = BookNurse.objects.filter(
        nurse_id = nurse.id, 
        status = "PEN"
    )
    context['booknurse'] = book_nurse
    return render(request, "nurse/en/booking_pending.html", context) 

def booking_list(request):
    context = {}
    nurse = NurseUser.objects.get(
        auth_user_id = request.user.id
    )
    book_nurse = BookNurse.objects.filter(
        nurse_id = nurse.id
    )
    context['booknurse'] = book_nurse
    return render(request, "nurse/en/all_booking.html", context)

class BookingUpdate(UpdateView):
    model = BookNurse
    success_message = "Book Updated!"
    fields = ["status"]
    template_name = "nurse/en/booking_update.html"