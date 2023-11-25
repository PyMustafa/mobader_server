from django.shortcuts import render 
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mobaderapp.models import PhysiotherapistService, PhysiotherapistUser, PhysiotherapistServiceTimes, BookPhysio
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


# Create your views here.
def dashboard(request):
    return render(request, "physio/en/home.html")

class ServicesListView(ListView):
    model = PhysiotherapistService
    template_name = "physio/en/service_list.html"


class ServicesCreate(SuccessMessageMixin, CreateView):
    model = PhysiotherapistService
    success_message = "Service Added!"
    fields = ["title", "details", "price"]
    template_name = "physio/en/service_create.html"

    
    def form_valid(self, form):
        service = form.save(commit=False)
        physio_instance = PhysiotherapistUser.objects.get(id=self.request.user.id)
        service.save()
        service.physiotherapist.set([physio_instance])

        messages.success(self.request, "Service Created Successfully")
        return HttpResponseRedirect(reverse("physio_services_list"))



class ServicesUpdate(UpdateView):
    model = PhysiotherapistService
    success_message = "Service Updated!"
    fields = ["title", "details", "price"]
    template_name = "physio/en/service_update.html"


class ServiceDeleteView(DeleteView):
    model = PhysiotherapistService
    success_message = "Service Deleted!"
    template_name = "physio/en/service_delete.html"
    success_url = reverse_lazy("physio_services_list")



class ServicesTimesListView(ListView): 
    model = PhysiotherapistServiceTimes
    queryset = PhysiotherapistServiceTimes.objects.filter(
        active = True
    )
    template_name = "physio/en/service_time_list.html"

    def get_context_data(self, **kwargs):
        context = super(ServicesTimesListView, self).get_context_data(**kwargs)
        context['services'] = PhysiotherapistService.objects.all()
        return context


class ServicesTimesCreate(SuccessMessageMixin, CreateView):
    model = PhysiotherapistServiceTimes
    success_message = "Service Added!"
    fields = ["service", "day", "start_time", "end_time"]
    template_name = "physio/en/service_time_create.html"

    def get_context_data(self, **kwargs):
        context = super(ServicesTimesCreate, self).get_context_data(**kwargs)
        context['services'] = PhysiotherapistService.objects.all()
        return context

    
    def form_valid(self, form):
        print(self.request.POST.get('service'))
        service_time = form.save(commit=False)
        service_time.service = PhysiotherapistService.objects.get(
            id=self.request.POST.get('service')
        )
        service_time.physio = PhysiotherapistUser.objects.get(id=self.request.user.id)
        service_time.active = True
        service_time.save()
        messages.success(self.request, "Service Time Created Successfully")
        return HttpResponseRedirect(reverse("physio_services_times_list"))



class ServicesTimeUpdate(UpdateView):
    model = PhysiotherapistServiceTimes
    success_message = "Service Time Updated!"
    fields = [ "day", "start_time", "end_time"]
    template_name = "physio/en/service_time_update.html"


class ServiceTimeDeleteView(DeleteView):
    model = PhysiotherapistServiceTimes
    success_message = "Service Time Deleted!"
    template_name = "physio/en/service_time_delete.html"
    success_url = reverse_lazy("physio_services_times_list")



# Bookings
def booking_pending(request):
    context = {}
    physio = PhysiotherapistUser.objects.get(
        id = request.user.id
    )
    book_physio = BookPhysio.objects.filter(
        physio_id = physio.id, 
        status = "PEN"
    )
    context['bookphysio'] = book_physio
    return render(request, "physio/en/booking_pending.html", context)

def booking_list(request):
    context = {}
    physio = PhysiotherapistUser.objects.get(
        id = request.user.id
    )
    book_physio = BookPhysio.objects.filter(
        physio_id = physio.id
    )
    context['bookphysio'] = book_physio
    return render(request, "physio/en/all_booking.html", context)

class BookingUpdate(UpdateView):
    model = BookPhysio
    success_message = "Book Updated!"
    fields = ["status"]
    template_name = "physio/en/booking_update.html"