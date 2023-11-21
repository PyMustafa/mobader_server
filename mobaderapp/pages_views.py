from django.conf import settings
from django.shortcuts import render

from . import models


# For Admin Lang Switching
def switch_lang_code(path, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]
    if path == "":
        raise Exception("URL path for language switch is empty")
    elif path[0] != "/":
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception("%s is not a supported language code" % language)
    parts = path.split("/")
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language
    return "/".join(parts)


def home_ar(request):
    sliders = models.Slider.objects.all()
    images = models.ImageGallery.objects.all()
    context = {
        "active": "1",
        "sliders": sliders,
        "images": images,
    }
    return render(request, "ar/pages/home.html", context)
    
def media_ar(request):
    # sliders = models.Slider.objects.all()
    # images = models.ImageGallery.objects.all()
    context = {
        "active": "5",
        # "sliders": sliders,
        # "images": images,
    }
    return render(request, "ar/pages/media.html", context)


def medical_services_ar(request):
    context = {
        "active": "2",
    }
    return render(request, "ar/pages/medical_services.html", context)


def service_nursing_ar(request):
    context = {
        "active": "2",
    }
    return render(request, "ar/pages/service_nursing.html", context)


def service_medical_ar(request):
    context = {
        "active": "2",
    }
    return render(request, "ar/pages/service_medical.html", context)


def about_us_ar(request):
    context = {
        "active": "3",
    }
    return render(request, "ar/pages/about_us.html", context)


def contact_us_ar(request):
    context = {
        "active": "4",
    }
    return render(request, "ar/pages/contact_us.html", context)


# English Views
def home_en(request):
    sliders = models.Slider.objects.all()
    images = models.ImageGallery.objects.all()
    context = {
        "active": "1",
        "sliders": sliders,
        "images": images,
    }
    return render(request, "en/pages/home.html", context)


def medical_services_en(request):
    context = {
        "active": "2",
    }
    return render(request, "en/pages/medical_services.html", context)


def service_nursing_en(request):
    context = {
        "active": "2",
    }
    return render(request, "en/pages/service_nursing.html", context)


def service_medical_en(request):
    context = {
        "active": "2",
    }
    return render(request, "en/pages/service_medical.html", context)


def about_us_en(request):
    context = {
        "active": "3",
    }
    return render(request, "en/pages/about_us.html", context)


def contact_us_en(request):
    context = {
        "active": "4",
    }
    return render(request, "en/pages/contact_us.html", context)
