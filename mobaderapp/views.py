from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                mobile=cd["mobile"],
                password=cd["password"],
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.user_type == "1":
                        return HttpResponseRedirect(reverse("admin_home"))
                    if user.user_type == "2":
                        return HttpResponseRedirect(reverse("home_ar"))
                    if user.user_type == "3":
                        return HttpResponseRedirect(reverse("doctor_dashboard"))
                    if user.user_type == "4":
                        return HttpResponseRedirect(reverse("nurse_dashboard"))
                    if user.user_type == "5":
                        return HttpResponseRedirect(reverse("lab_dashboard"))
                    if user.user_type == "6":
                        return HttpResponseRedirect(reverse("pharma_dashboard"))
                    if user.user_type == "7":
                        return HttpResponseRedirect(reverse("physio_dashboard"))
                    if user.user_type == "8":
                        return HttpResponseRedirect(reverse("patient_dashboard"))
            else:
                messages.error(request, "Error in Login! Invalid Login Details ")
                return render(request, "en/pages/signin.html", {"form": form})
    else:
        form = LoginForm()
    return render(request, "en/pages/signin.html", {"form": form})


def users_logout_process(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return HttpResponseRedirect(reverse("home_ar"))
