from datetime import datetime
import json
import random
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
import stripe
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from mobaderapp.forms import (
    UserRegistrationForm,
    ServiceVisitBooking,
    ServiceVisitBookingNurse,
    ServiceVisitBookingPhysio,
    ServiceVisitBookingAnalytic,
    ServiceVisitBookingMedicine,
)
from mobaderapp.models import (
    CustomUser,
    DoctorCategory,
    DoctorTimes,
    DoctorUser,
    NurseUser,
    PatientUser,
    BookDoctor,
    PhysiotherapistUser,
    BookNurse,
    NurseService,
    NurseServiceTimes,
    BookPhysio,
    PhysiotherapistService,
    PhysiotherapistServiceTimes,
    BookAnalytic,
    LabDetail,
    LabService,
    BookMedicine,
    PharmacyDetail,
    PharmacyMedicine,
)


# =================================================
# Register
def generate_otp() -> str:
    x = ""
    for _ in range(6):
        x += str(random.choice(range(10)))
    return x
   
# =====================================================================
class PatientUserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    success_message = "Patient Created!"
    fields = ["username", "email", "password"]
    template_name = "en/patient/register.html"

    def form_valid(self, form):
        # Sending OTP
        number = generate_otp()
        message_content = f"Mobader OTP Activation Number From Server: {number}"
        requests.get(
            f"http://mshastra.com/sendurlcomma.aspx?user=20094672&pwd=c12345&senderid=GCHOSPITAL&CountryCode=966&mobileno={self.request.POST.get('mobile')}&msgtext={message_content}&smstype=0"
        )
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 8
        user.set_password(form.cleaned_data["password"])
        user.save()
        cre = CustomUser.objects.get(email=user.email)
        patient = PatientUser(auth_user_id=cre, mobile=self.request.POST.get("mobile"), verification=number, address=self.request.POST.get("address"))
        patient.save()
        messages.success(self.request, "Patient Created Successfully")
        return HttpResponseRedirect(
            reverse(
                "confirm_account", kwargs={"phone": self.request.POST.get("mobile")}
            )
        )


def confirm_account(request, phone):
    patient = PatientUser.objects.filter(mobile=phone).first()
    print("================")
    print(patient)
    if request.method == "POST":
        enter_code = request.POST.get("code")
        print(enter_code)
        if patient.verification == enter_code:
            print("valid")
            patient.confirmed = True
            patient.save()
            messages.success(request, "Confirmed Success")
            return HttpResponseRedirect(reverse("login"))
        messages.error(request, "sorry, Not valid")
        return HttpResponseRedirect(reverse("confirm_account", kwargs={"phone": phone}))
    else:
        return render(request, "en/pages/confirm_account.html", {"phone": phone})


# =================================================
# Dashboard


def dashboard(request):
    context = {}
    context["categories"] = DoctorCategory.objects.all()
    context["doctors"] = DoctorUser.objects.all()
    context["nurses"] = NurseUser.objects.all()
    context["physiotherapists"] = PhysiotherapistUser.objects.all()
    context["labs"] = LabDetail.objects.all()
    context["pharma"] = PharmacyDetail.objects.all()

    return render(request, "en/patient/home.html", context)


# =================================================
# All Services and Booking


def all_services(request):
    return render(request, "en/patient/all_service.html")


def book_doctor(request):
    if request.method == "POST":
        if request.user.id:
            request.POST = request.POST.dict()
            booking = BookDoctor()
            # Get Patient
            booking.patient = PatientUser.objects.filter(
                auth_user_id=request.user.id
            ).first()
            # Get Doctor
            booking.doctor = DoctorUser.objects.get(id=request.POST["doctor_pk"])
            # Get Time Booking
            book_time = DoctorTimes.objects.get(id=request.POST["booking_slot"])
            booking.book_time = book_time
            # Set Default book_type
            booking.book_type = "visit"
            # Set Default Status
            booking.status = "PEN"
            if request.POST.get("payment_stripe"):
                service_name = "Mobader Doctor Visit"
                price = DoctorUser.objects.get(id=request.POST["doctor_pk"]).price
                current_site = get_current_site(request)
                # stripe.api_key = settings.STRIPE_SECRETKEY
                url = "https://api.tap.company/v2/charges/"
                payload = {
                    "amount": int(price),
                    "currency": "SAR",
                    "description": service_name,
                    "customer": {
                        "first_name": "amr",
                        "phone": {
                            "country_code": 966,
                            "number": 51234567,
                        },
                    },
                    "source": {"id": "src_all"},
                    "redirect": {
                        "url": f"http://{current_site}/patient/all-booking-doctors/"
                    },
                }
                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "Authorization": "Bearer sk_test_ZtGvaAiXEhnV2cd7YkMQsSxW",
                }
                response = requests.post(url, json=payload, headers=headers)
                res = json.loads(response.text)
                booking.is_paid = True
                # book_time.active = False
                book_time.save()
                booking.save()
                return redirect(res["transaction"]["url"])
            else:
                booking.is_paid = False
                book_time.active = False
                book_time.save()
                booking.status = "PEN"
                booking.save()
                messages.success(
                    request, "Booking Completed, please wait until it accepted"
                )
                return redirect("patient_dashboard")
        else:
            return redirect("login")
    booking_form = ServiceVisitBooking()
    context = {}
    context["patient"] = PatientUser.objects.filter(
        auth_user_id=request.user.id
    ).first()
    context["service_type"] = "Booking Doctor"
    context["categories"] = DoctorCategory.objects.all()
    context["doctors"] = DoctorUser.objects.all()
    context["booking_form"] = booking_form

    return render(request, "en/patient/doctor_visit.html", context)


def book_nurse(request):
    if request.method == "POST":
        if request.user.id:
            request.POST = request.POST.dict()
            booking = BookNurse()
            booking.patient = PatientUser.objects.filter(
                auth_user_id=request.user.id
            ).first()
            booking.nurse = NurseUser.objects.get(id=request.POST["nurse_pk"])
            booking.service = NurseService.objects.get(
                id=request.POST["category_class"]
            )
            booking.time = NurseServiceTimes.objects.get(
                id=request.POST["booking_slot"]
            )
            booking.status = "PEN"
            if request.POST.get("payment_stripe"):
                stripe_service_name = "SedrahCare Nurse Visit"
                price = booking.service.price
                current_site = get_current_site(request)
                stripe.api_key = settings.STRIPE_SECRETKEY
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "product_data": {"name": stripe_service_name},
                                "currency": "sar",
                                "unit_amount": int(price) * 100,
                            },
                            "quantity": 1,
                        },
                    ],
                    mode="payment",
                    customer_creation="always",
                    success_url=f"http://{current_site}/user/verify_order?status=success&pk={booking.pk}",
                    cancel_url=f"http://{current_site}/user/verify_order?status=failed&pk={booking.pk}",
                )
                booking.status = "PEN"
                booking.time.active = False
                booking.time.save()
                booking.save()
                return redirect(checkout_session.url, code=303)
            else:
                booking.time.active = False
                booking.time.save()
                booking.status = "PEN"
                booking.save()
                messages.success(
                    request, "Booking Completed, please wait until it accepted"
                )
                return redirect("patient_dashboard")
        else:
            return redirect("login")
    booking_form = ServiceVisitBookingNurse()
    context = {}
    context["patient"] = PatientUser.objects.filter(
        auth_user_id=request.user.id
    ).first()
    context["service_type"] = "Booking Nurse"
    context["services"] = NurseService.objects.all()
    context["booking_form"] = booking_form

    return render(request, "en/patient/nurse_visit.html", context)


def book_physio(request):
    if request.method == "POST":
        if request.user.id:
            request.POST = request.POST.dict()
            booking = BookPhysio()
            booking.patient = PatientUser.objects.filter(
                auth_user_id=request.user.id
            ).first()
            booking.physio = PhysiotherapistUser.objects.get(
                id=request.POST["physio_pk"]
            )
            booking.service = PhysiotherapistService.objects.get(
                id=request.POST["category_class"]
            )
            booking.time = PhysiotherapistServiceTimes.objects.get(
                id=request.POST["booking_slot"]
            )
            booking.status = "PEN"
            if request.POST.get("payment_stripe"):
                stripe_service_name = "SedrahCare Physiotherapist Visit"
                price = booking.service.price
                current_site = get_current_site(request)
                stripe.api_key = settings.STRIPE_SECRETKEY
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "product_data": {"name": stripe_service_name},
                                "currency": "sar",
                                "unit_amount": int(price) * 100,
                            },
                            "quantity": 1,
                        },
                    ],
                    mode="payment",
                    customer_creation="always",
                    success_url=f"http://{current_site}/user/verify_order?status=success&pk={booking.pk}",
                    cancel_url=f"http://{current_site}/user/verify_order?status=failed&pk={booking.pk}",
                )
                booking.status = "PEN"
                booking.time.active = False
                booking.time.save()
                booking.save()
                return redirect(checkout_session.url, code=303)
            else:
                booking.time.active = False
                booking.time.save()
                booking.status = "PEN"
                booking.save()
                messages.success(
                    request, "Booking Completed, please wait until it accepted"
                )
                return redirect("patient_dashboard")
        else:
            return redirect("login")
    booking_form = ServiceVisitBookingPhysio()
    context = {}
    context["patient"] = PatientUser.objects.filter(
        auth_user_id=request.user.id
    ).first()
    context["service_type"] = "Booking Physiotherapist"
    context["services"] = PhysiotherapistService.objects.all()
    context["booking_form"] = booking_form

    return render(request, "en/patient/physio_visit.html", context)


def book_analytic(request):
    if request.method == "POST":
        if request.user.id:
            request.POST = request.POST.dict()
            booking = BookAnalytic()
            booking.patient = PatientUser.objects.filter(
                auth_user_id=request.user.id
            ).first()
            booking.lab = LabDetail.objects.get(id=request.POST["lab_pk"])
            booking.service = LabService.objects.get(id=request.POST["category_class"])
            booking.status = "PEN"
            if request.POST.get("payment_stripe"):
                stripe_service_name = "SedrahCare Analytics"
                price = booking.service.price
                current_site = get_current_site(request)
                stripe.api_key = settings.STRIPE_SECRETKEY
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "product_data": {"name": stripe_service_name},
                                "currency": "sar",
                                "unit_amount": int(price) * 100,
                            },
                            "quantity": 1,
                        },
                    ],
                    mode="payment",
                    customer_creation="always",
                    success_url=f"http://{current_site}/user/verify_order?status=success&pk={booking.pk}",
                    cancel_url=f"http://{current_site}/user/verify_order?status=failed&pk={booking.pk}",
                )
                booking.status = "PEN"
                booking.save()
                return redirect(checkout_session.url, code=303)
            else:
                booking.status = "PEN"
                booking.save()
                messages.success(
                    request, "Booking Completed, please wait until it accepted"
                )
                return redirect("patient_dashboard")
        else:
            return redirect("login")
    booking_form = ServiceVisitBookingAnalytic()
    context = {}
    context["patient"] = PatientUser.objects.filter(
        auth_user_id=request.user.id
    ).first()
    context["service_type"] = "Booking Analytic"
    context["services"] = LabService.objects.all()
    context["booking_form"] = booking_form

    return render(request, "en/patient/lab_visit.html", context)


def book_medicine(request):
    if request.method == "POST":
        if request.user.id:
            request.POST = request.POST.dict()
            print(request.POST)
            booking = BookMedicine()
            booking.patient = PatientUser.objects.filter(
                auth_user_id=request.user.id
            ).first()
            booking.pharma = PharmacyDetail.objects.get(
                id=request.POST["category_class"]
            )
            booking.medicine = PharmacyMedicine.objects.get(
                id=request.POST["medicine_pk"]
            )
            booking.count = 1
            booking.status = "PEN"
            if request.POST.get("payment_stripe"):
                stripe_service_name = "SedrahCare Medicine"
                price = booking.medicine.price * int(booking.count)
                current_site = get_current_site(request)
                stripe.api_key = settings.STRIPE_SECRETKEY
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "product_data": {"name": stripe_service_name},
                                "currency": "sar",
                                "unit_amount": int(price) * 100,
                            },
                            "quantity": 1,
                        },
                    ],
                    mode="payment",
                    customer_creation="always",
                    success_url=f"http://{current_site}/user/verify_order?status=success&pk={booking.pk}",
                    cancel_url=f"http://{current_site}/user/verify_order?status=failed&pk={booking.pk}",
                )
                booking.status = "PEN"
                booking.medicine.count -= booking.count
                booking.medicine.save()
                booking.save()
                return redirect(checkout_session.url, code=303)
            else:
                booking.status = "PEN"
                booking.medicine.count -= booking.count
                booking.medicine.save()
                booking.save()
                messages.success(
                    request, "Booking Completed, please wait until it accepted"
                )
                return redirect("patient_dashboard")
        else:
            return redirect("login")
    booking_form = ServiceVisitBookingMedicine()
    context = {}
    context["patient"] = PatientUser.objects.filter(
        auth_user_id=request.user.id
    ).first()
    context["service_type"] = "Booking Medicine"
    context["pharmas"] = PharmacyDetail.objects.all()
    context["booking_form"] = booking_form

    return render(request, "en/patient/medicine_order.html", context)


@login_required
def book_meeting(request):
    if request.method == "POST":
        if request.user.id:
            request.POST = request.POST.dict()
            booking = BookDoctor()
            # Get Patient
            booking.patient = PatientUser.objects.filter(
                auth_user_id=request.user.id
            ).first()
            # Get Doctor
            booking.doctor = DoctorUser.objects.get(id=request.POST["doctor_pk"])
            # Get Time Booking
            book_time = DoctorTimes.objects.get(id=request.POST["booking_slot"])
            booking.book_time = book_time
            # Set Default book_type
            booking.book_type = "meet"
            # Set Default Meeting Room
            booking.meeting_room = str(round(datetime.now().timestamp()))
            # Set Default Status
            booking.status = "PEN"
            if request.POST.get("payment_stripe"):
                stripe_service_name = "Mobader Doctor Meet"
                booking.is_paid = True
                price = DoctorUser.objects.get(id=request.POST["doctor_pk"]).price
                current_site = get_current_site(request)
                stripe.api_key = settings.STRIPE_SECRETKEY
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "product_data": {"name": stripe_service_name},
                                "currency": "sar",
                                "unit_amount": int(price) * 100,
                            },
                            "quantity": 1,
                        },
                    ],
                    mode="payment",
                    customer_creation="always",
                    success_url=f"http://{current_site}/user/verify_order?status=success&pk={booking.pk}",
                    cancel_url=f"http://{current_site}/user/verify_order?status=failed&pk={booking.pk}",
                )
                book_time.active = False
                book_time.save()
                booking.save()
                return redirect(checkout_session.url, code=303)
        else:
            return redirect("login")
    booking_form = ServiceVisitBooking()
    context = {}
    context["patient"] = PatientUser.objects.filter(
        auth_user_id=request.user.id
    ).first()
    context["service_type"] = "Meeting Doctor"
    context["categories"] = DoctorCategory.objects.all()
    context["doctors"] = DoctorUser.objects.all()
    context["booking_form"] = booking_form
    return render(request, "en/patient/doctor_meet.html", context)


@login_required
def meeting_room(request, room):
    context = {"agora_id": settings.AGORA_APP_ID, "room": room}
    return render(request, "en/patient/meeting_room.html", context)


"""
context = {"agora_id": settings.AGORA_APP_ID}
return render(request, "en/patient/meeting_room.html", context)
"""

# =================================================
# All Details


def all_booking_doctors(request):
    context = {}
    patient = PatientUser.objects.get(auth_user_id=request.user.id)
    book_doctor = BookDoctor.objects.filter(patient_id=patient.id)
    context["bookdoctors"] = book_doctor
    return render(request, "en/patient/all_booking_doctors.html", context)


def all_booking_nurses(request):
    context = {}
    patient = PatientUser.objects.get(auth_user_id=request.user.id)
    book_nurse = BookNurse.objects.filter(patient_id=patient.id)
    context["booknurses"] = book_nurse
    return render(request, "en/patient/all_booking_nurses.html", context)


def all_booking_physio(request):
    context = {}
    patient = PatientUser.objects.get(auth_user_id=request.user.id)
    book_physio = BookPhysio.objects.filter(patient_id=patient.id)
    context["bookphysio"] = book_physio
    return render(request, "en/patient/all_booking_physio.html", context)


def all_booking_analytics(request):
    context = {}
    patient = PatientUser.objects.get(auth_user_id=request.user.id)
    book_analytic = BookAnalytic.objects.filter(patient_id=patient.id)
    context["bookanalytics"] = book_analytic
    return render(request, "en/patient/all_booking_lab.html", context)


def all_booking_medicines(request):
    context = {}
    patient = PatientUser.objects.get(auth_user_id=request.user.id)
    book_medicines = BookMedicine.objects.filter(patient_id=patient.id)
    context["bookmedicines"] = book_medicines
    return render(request, "en/patient/all_booking_medicine.html", context)


# Services
@csrf_exempt
def get_user_address(request):
    lon = request.GET.get("lon")
    lat = request.GET.get("lat")

    if lon and lat:
        try:
            place = requests.get(
                f"{settings.LOCATIONIQ_API}&accept-language=ar&lon={lon}&lat={lat}"
            ).json()
            return JsonResponse({"address": place["display_name"]})
        except Exception as err:
            return HttpResponse("error", status=500)

    return JsonResponse({"error": "invalid params provided"})


@csrf_exempt
def list_service_doctors(request):
    if request.method == "POST":
        context = {"doctors": []}
        data = json.loads(request.body)

        try:
            doctors = DoctorUser.objects.filter(category_id=data["category_type"])

            for doctor in doctors:
                try:
                    photo = str(doctor.profile_pic)
                except:
                    photo = None
                doctor_name = str(doctor.auth_user_id)
                context["doctors"].append(
                    {
                        "phone": doctor.mobile_phone,
                        "address": doctor.address,
                        "price": doctor.price,
                        "name": doctor_name,
                        "photo": photo,
                        "id": doctor.id,
                    }
                )
            return JsonResponse(context)
        except Exception as err:
            return JsonResponse({"error": "invalid params"}, status=404)
    return JsonResponse({"error": "invalid method"}, status=405)


@csrf_exempt
def list_nurses(request):
    if request.method == "POST":
        context = {"nurses": []}
        data = json.loads(request.body)
        try:
            service = NurseService.objects.get(id=data["service_id"])
            nurses = NurseUser.objects.filter(id=service.nurse_id)

            for nurse in nurses:
                try:
                    photo = str(nurse.profile_pic)
                except:
                    photo = None
                nurse_name = str(nurse.auth_user_id)
                context["nurses"].append(
                    {
                        "price": service.price,
                        "phone": nurse.mobile,
                        "address": nurse.address,
                        "name": nurse_name,
                        "photo": photo,
                        "id": nurse.id,
                    }
                )
            return JsonResponse(context)
        except Exception as err:
            return JsonResponse({"error": "invalid params"}, status=404)
    return JsonResponse({"error": "invalid method"}, status=405)


@csrf_exempt
def list_physio(request):
    if request.method == "POST":
        context = {"physios": []}
        data = json.loads(request.body)

        try:
            service = PhysiotherapistService.objects.get(id=data["service_id"])
            physios = PhysiotherapistUser.objects.filter(id=service.physiotherapist_id)

            for physio in physios:
                try:
                    photo = str(physio.profile_pic)
                except:
                    photo = None
                physio_name = str(physio.auth_user_id)
                context["physios"].append(
                    {
                        "price": service.price,
                        "phone": physio.mobile_phone,
                        "address": physio.address,
                        "name": physio_name,
                        "photo": photo,
                        "id": physio.id,
                    }
                )
            return JsonResponse(context)
        except Exception as err:
            return JsonResponse({"error": "invalid params"}, status=404)
    return JsonResponse({"error": "invalid method"}, status=405)


@csrf_exempt
def list_labs(request):
    if request.method == "POST":
        context = {"labs": []}
        data = json.loads(request.body)
        try:
            service = LabService.objects.filter(id=data["service_id"]).first()
            labs = LabDetail.objects.all()
            for lab in labs:
                if lab.id == service.lap.id:
                    try:
                        photo = str(lab.thumbnail)
                    except:
                        photo = None
                    lab_name = str(lab.name)
                    context["labs"].append(
                        {
                            "price": service.price,
                            "phone": lab.mobile_phone,
                            "address": lab.address,
                            "name": lab_name,
                            "photo": photo,
                            "id": lab.id,
                        }
                    )
            return JsonResponse(context)
        except Exception as err:
            return JsonResponse({"error": "invalid params"}, status=404)
    return JsonResponse({"error": "invalid method"}, status=405)


@csrf_exempt
def list_medicines(request):
    if request.method == "POST":
        context = {"medicines": []}
        data = json.loads(request.body)
        try:
            pharma = PharmacyDetail.objects.filter(id=data["pharma_id"]).first()
            medicines = PharmacyMedicine.objects.all()
            for medicine in medicines:
                if pharma.id == medicine.pharmacy.id:
                    try:
                        photo = str(medicine.image)
                    except:
                        photo = None
                    medicine_name = str(medicine.title)
                    context["medicines"].append(
                        {
                            "price": medicine.price,
                            "count": medicine.count,
                            "phone": pharma.mobile_phone,
                            "address": pharma.address,
                            "name": medicine_name,
                            "photo": photo,
                            "id": medicine.id,
                        }
                    )
            return JsonResponse(context)
        except Exception as err:
            return JsonResponse({"error": "invalid params"}, status=404)
    return JsonResponse({"error": "invalid method"}, status=405)


def datetime_to_arab(date):
    date = date.lower()
    numbers = {
        48: 1632,
        49: 1633,
        50: 1634,
        51: 1635,
        52: 1636,
        53: 1637,
        54: 1638,
        55: 1639,
        56: 1640,
        57: 1641,
    }
    letters = {
        "jan": "يناير",
        "feb": "فبراير",
        "mar": "مارس",
        "apr": "ابريل",
        "may": "ماية",
        "jun": "يونيه",
        "jul": "يوليو",
        "aug": "اغسطس",
        "sep": "سبتمبر",
        "oct": "اكتوبر",
        "nov": "نوفمبر",
        "dec": "ديسمبر",
        "am": "صباحا",
        "pm": "مساءا",
    }
    date = date.translate(numbers)
    for key, val in letters.items():
        date = date.replace(key, val)
    return date.split()


@csrf_exempt
def get_booking_slots(request):
    if request.method == "POST":
        data = json.loads(request.body)
        context = {"slots": []}

        try:
            doctor = DoctorUser.objects.get(pk=data["id"])

            slots = DoctorTimes.objects.filter(doctor=doctor)

            for slot in slots:
                if slot.active:
                    context["slots"].append(
                        {
                            "id": slot.id,
                            "day": f"{slot.start_time.strftime('%d %b %Y')} || {slot.title} ",
                            "start_time": slot.start_time.strftime("%I:%M %p"),
                            "end_time": slot.end_time.strftime("%I:%M %p"),
                        }
                    )

            return JsonResponse(context)
        except Exception as err:
            print(err)
            return JsonResponse({"error": "invalid params"})
    return JsonResponse({"error": "invalid method"})


@csrf_exempt
def get_times_nurse(request):
    if request.method == "POST":
        data = json.loads(request.body)
        context = {"slots": []}
        try:
            slots = NurseServiceTimes.objects.filter(service_id=data["id"])
            for slot in slots:
                if slot.active:
                    context["slots"].append(
                        {
                            "id": slot.id,
                            "day": str(slot.day),
                            "start_time": slot.start_time.strftime("%I:%M %p"),
                            "end_time": slot.end_time.strftime("%I:%M %p"),
                        }
                    )

            return JsonResponse(context)
        except Exception as err:
            print(err)
            return JsonResponse({"error": "invalid params"})
    return JsonResponse({"error": "invalid method"})


@csrf_exempt
def get_times_physio(request):
    if request.method == "POST":
        data = json.loads(request.body)
        context = {"slots": []}
        try:
            slots = PhysiotherapistServiceTimes.objects.filter(service_id=data["id"])
            for slot in slots:
                if slot.active:
                    context["slots"].append(
                        {
                            "id": slot.id,
                            "day": str(slot.day),
                            "start_time": slot.start_time.strftime("%I:%M %p"),
                            "end_time": slot.end_time.strftime("%I:%M %p"),
                        }
                    )

            return JsonResponse(context)
        except Exception as err:
            print(err)
            return JsonResponse({"error": "invalid params"})
    return JsonResponse({"error": "invalid method"})
