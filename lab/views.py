from django.shortcuts import render 
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from mobaderapp.models import LabService, LapUser, LabDetail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy



# Create your views here.
def dashboard(request):
    return render(request, "lab/en/home.html")

class ServicesListView(ListView):
    model = LabService
    template_name = "lab/en/service_list.html"


class ServicesCreate(SuccessMessageMixin, CreateView):
    model = LabService
    success_message = "Service Added!"
    fields = ["title", "image", "details", "price"]
    template_name = "lab/en/service_create.html"

    
    def form_valid(self, form):
        service = form.save(commit=False)
        service.lap = LabDetail.objects.get(
            admin_id= LapUser.objects.get(
            auth_user_id=self.request.user.id
        )
        )
        service.save()
        messages.success(self.request, "Service Created Successfully")
        return HttpResponseRedirect(reverse("lab_services_list"))



class ServicesUpdate(UpdateView):
    model = LabService
    success_message = "Service Updated!"
    fields = ["title", "image", "details", "price"]
    template_name = "lab/en/service_update.html"


class ServiceDeleteView(DeleteView):
    model = LabService
    success_message = "Service Deleted!"
    template_name = "lab/en/service_delete.html"
    success_url = reverse_lazy("lab_services_list")


class LapDetailListView(ListView):
    model = LabDetail
    template_name = "lab/en/lab_detail.html"



class LabDetailCreate(SuccessMessageMixin, CreateView):
    model = LabDetail
    success_message = "Lab Added!"
    fields = ["name", "thumbnail", "description", "mobile_phone", "address", "open_time", "close_time"]
    template_name = "lab/en/lab_create.html"

    
    def form_valid(self, form):
        lab_detail = form.save(commit=False)
        lab_detail.admin = LapUser.objects.get(
            auth_user_id=self.request.user.id
        )
        lab_detail.save()
        messages.success(self.request, "Laboratory Created Successfully")
        return HttpResponseRedirect(reverse("lab_detail"))



class LabDetailUpdate(UpdateView):
    model = LabDetail
    success_message = "Lab Detail Updated!"
    fields = ["name", "thumbnail", "description", "mobile_phone", "address", "open_time", "close_time"]
    template_name = "lab/en/lab_update.html"


class LabDeleteView(DeleteView):
    model = LabDetail
    success_message = "Lab Detail Deleted!"
    template_name = "lab/en/lab_delete.html"
    success_url = reverse_lazy("lab_detail")