import random
from datetime import datetime
from django.core.serializers import serialize
import json
from django.http import JsonResponse, HttpResponseRedirect
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers, models
from .models import PatientUser, BookDoctor, DoctorCategory, DoctorUser, DoctorTimes, NurseUser, NurseService, \
    NurseServiceTimes, PhysiotherapistUser, PhysiotherapistService, PhysiotherapistServiceTimes, BookPhysio, \
    PharmacyUser, PharmacyMedicine, PharmacyDetail, BookMedicine, LapUser, LabService, LabDetail, OfferDoctor, \
    OfferNurseService, BookNurse, BookAnalytic

from .serializers import PatientUserSerializer, UserVerifyOTPSerializer, UserLoginSerializer, \
    ResetPassRequestSerializer, ResetPassSerializer, BookDoctorSerializer, DoctorCategorySerializer, \
    CategoryDoctorsSerializer, NurseSerializer, NurseServiceSerializer, NurseServiceTimesSerializer, \
    BookNurseSerializer, PhysioUserSerializer, PhysioServiceSerializer, PhysioServiceTimesSerializer, \
    BookPhysioSerializer, PharmacyUserSerializer, PharmacyMedicineSerializer, PharmacySerializer, \
    BookMedicineSerializer, LabUserSerializer, LabServiceSerializer, LabDetailSerializer, BookAnalyticSerializer, \
    BookDoctorSerializers, DoctorBookingsSerializer, OfferDoctorSerializer, OfferNurseServiceSerializer, \
    OfferPhysioServiceSerializer, OfferLabAnalyticSerializer, NurseBookingsSerializer, PhysioBookingsSerializer, \
    AnalyticBookingsSerializer

User = get_user_model()


def generate_otp() -> str:
    x = ""
    for _ in range(6):
        x += str(random.choice(range(10)))
    return x


base_url = "https://mobader.sa"
secret_key = 'sk_test_ZtGvaAiXEhnV2cd7YkMQsSxW'


def create_tap_payment_session(patient, price, book_model):
    url = "https://api.tap.company/v2/charges/"

    # customer info
    first_name = patient.auth_user_id.first_name
    last_name = patient.auth_user_id.last_name
    email = patient.auth_user_id.email
    mobile_phone = patient.mobile
    payload = {
        "amount": round(price),
        "currency": "SAR",
        "customer_initiated": True,
        "threeDSecure": True,
        "save_card": False,
        "description": "Test Description",
        "metadata": {"book_model": book_model},
        "reference": {
            "transaction": "txn_01",
            "order": "ord_01"
        },
        "receipt": {
            "email": True,
            "sms": True
        },
        "customer": {
            "first_name": first_name,
            "middle_name": "",
            "last_name": last_name,
            "email": email,
            "phone": {
                "country_code": 966,
                "number": int(mobile_phone)
            }
        },
        # The ID of the Merchant Account. Available on the Tap Dashboard (goSell > API Credentials > Merchant ID)
        "merchant": {"id": "1234"},
        "source": {"id": "src_card"},
        "post": {"url": f"{base_url}api/v1/tap_webhook/"},
        "redirect": {"url": base_url}
    }

    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        status_code = response.status_code

        redirect_url = response_data['transaction']['url']

        return response
    except requests.RequestException as e:
        return {"status": "error", "error": str(e)}


def retrieve_charge(charge_id):
    import requests

    url = f'https://api.tap.company/v2/charges/{charge_id}'

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.get(url, headers=headers)
    return response


def payment_is_approved(response_data):
    try:
        response_code = response_data["response"]["code"]
        card_security_code = response_data["card_security"]["code"]
        acquirer_response_code = response_data["acquirer"]["response"]["code"]

        if (
                response_code == '000'
                and card_security_code == 'M'
                and acquirer_response_code == '00'
        ):
            return True
    except KeyError:
        return False
    return False


# tap webhook
class TapWebhookView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        payload = request.data
        charge_id = payload['id']

        response = retrieve_charge(charge_id)
        response_data = response.json()

        if payment_is_approved(response_data):
            patient_mobile = response_data["customer"]["phone"]["number"]
            book_model = response_data["metadata"]["book_model"]
            patient = PatientUser.objects.filter(mobile=patient_mobile).first()

            if book_model == "BookDoctor":
                book_obj = BookDoctor.objects.filter(patient_id=patient.id).first()
                book_obj.is_paid = True
                book_obj.save()
            return JsonResponse({'status': 'success', 'message': 'Payment successful'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Payment not successful'})


class TapPaymentStatus(APIView):
    def get(self, request, *args, **kwargs):
        charge_id = kwargs['charge_id']
        url = f"https://api.tap.company/v2/charges/{charge_id}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {secret_key}",
        }

        response = requests.get(url, headers=headers)
        response_data = response.json()

        if payment_is_approved(response_data):
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)


# Authentication APIs
class PatientUserCreateView(generics.CreateAPIView):
    queryset = PatientUser.objects.all()
    serializer_class = PatientUserSerializer

    def perform_create(self, serializer):
        verification_value = generate_otp()
        serializer.validated_data['verification'] = verification_value
        super().perform_create(serializer)

        message_content = f"""
                Welcome to Mobader\n
                We care about your health, and your life is our mission.
                This is your Activation Code {verification_value}
                """
        try:
            # response = requests.get(
            #    f"https://mshastra.com/sendurlcomma.aspx?user=20094672&pwd=c12345&senderid=MOBADER&CountryCode=966&mobileno={serializer.validated_data['mobile']}&msgtext={message_content}&smstype=0"
            # )
            # response.raise_for_status()
            print(verification_value)
        except requests.RequestException as e:
            print(f"Error sending SMS: {e}")


class UserVerifyOTPView(generics.UpdateAPIView):
    queryset = PatientUser.objects.all()
    serializer_class = UserVerifyOTPSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(f'serializer:{serializer}')
        serializer.is_valid(raise_exception=True)

        verification_code = serializer.validated_data['verification_code']
        patient = PatientUser.objects.filter(verification=verification_code).last()

        if patient:
            patient.confirmed = True
            patient.save()
            return Response({'detail': 'Confirmed successfully'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            patient = PatientUser.objects.get(auth_user_id=user.id)

            user_info = {
                'id': patient.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'confirmed': patient.confirmed,
                'mobile': patient.mobile,
                'address': patient.address,
            }

            return Response({'status': 'success', 'token': access_token, 'user': user_info}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


class ResetPassRequestView(generics.CreateAPIView):
    serializer_class = ResetPassRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile_number = serializer.validated_data['mobile_number']

        # Check if the mobile number is in the database
        try:
            patient = PatientUser.objects.get(mobile=mobile_number)
        except PatientUser.DoesNotExist:
            return Response({'detail': 'User with this mobile number does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Generate OTP and update the verification field
        new_otp = generate_otp()
        patient.verification = new_otp
        patient.save()

        # sending the OTP to the mobile number
        message_content = f"""
                               Welcome to Mobader\n
                               There is a request to reset your password!
                               use this code: {new_otp}
                               If you did not make this request then please ignore this message.
                               """
        requests.get(
            f"https://mshastra.com/sendurlcomma.aspx?user=20094672&pwd=c12345&senderid=MOBADER&CountryCode=966&mobileno={mobile_number}&msgtext={message_content}&smstype=0"
        )

        response_data = {
            'detail': 'Verification code sent. Reset your password using the provided code.',
            'reset_password_url': '/api/reset-password/',  # Adjust the URL as needed
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ResetPassView(generics.UpdateAPIView):
    serializer_class = ResetPassSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification_code = serializer.validated_data['verification_code']
        new_password = serializer.validated_data['new_password']

        # check if a user with the provided verification code exists
        try:
            patient = PatientUser.objects.get(verification=verification_code)
        except PatientUser.DoesNotExist:
            return Response({'detail': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

        # update the user password
        patient.auth_user_id.set_password(new_password)
        patient.save()
        return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)


# get all doctors in the selected category
class CategoryDoctorsAPIView(generics.ListAPIView):
    serializer_class = CategoryDoctorsSerializer

    def get_queryset(self):
        category_id = self.kwargs['pk']
        times = models.DoctorTimes.objects.filter(doctor__category_id=category_id).values()
        cat_doctors = models.DoctorUser.objects.filter(category_id=category_id).values()
        list_doctors = []
        for doctor in cat_doctors:
            doctor["times"] = []
            for time in times:
                if time["doctor"] == doctor["id"]:
                    doctor["times"].append(time)

            list_doctors.append(doctor)

        return list_doctors


# New Code to get doctors and it's time
def get_doctors(request, pk):
    times = models.DoctorTimes.objects.filter(doctor__category_id=pk).values()
    cat_doctors = models.DoctorUser.objects.filter(category_id=pk).values()
    list_doctors = []
    for doctor in cat_doctors:
        doctor["times"] = []
        info = models.CustomUser.objects.filter(id=doctor["auth_user_id_id"])
        doctor["info"] = json.loads(serialize("json", info, fields=("username", "email", "first_name", "last_name")))
        for time in times:
            if time["doctor_id"] == doctor["id"]:
                doctor["times"].append(time)

        list_doctors.append(doctor)

    return JsonResponse({"status": "success", "data": list_doctors})


# get all categories
class CategoryListAPIView(generics.ListAPIView):
    queryset = DoctorCategory.objects.all()
    serializer_class = DoctorCategorySerializer


# get category by id
class CategoryAPIView(generics.RetrieveAPIView):
    queryset = DoctorCategory.objects.all()
    serializer_class = DoctorCategorySerializer


class BookDoctorCreateAPIView(generics.CreateAPIView):
    serializer_class = BookDoctorSerializer

    # we will uncomment this line after Authorization error fix
    # permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = PatientUser.objects.filter(id=request.data.get("patient")).first()
        doctor = DoctorUser.objects.get(id=request.data.get("doctor"))
        price = doctor.price
        book_time = DoctorTimes.objects.get(id=request.data.get("book_time"))
        is_paid = request.data.get("is_paid")
        book_type = request.data.get("book_type")
        if book_type == "meet":
            meeting_room = str(round(datetime.now().timestamp()))
        else:
            meeting_room = ""

        booking = serializer.save(
            patient=patient,
            doctor=doctor,
            book_time=book_time,
            book_type=book_type,
            meeting_room=meeting_room,
            status="PEN",
        )
        booking_data = BookDoctorSerializer(booking).data

        # open tap payment session
        book_model = "BookDoctor"
        if is_paid:
            payment_response = create_tap_payment_session(patient, price, book_model)
            payment_status_code = payment_response.status_code

            if payment_status_code == 200:
                payment_response_data = payment_response.json()
                response_data = {
                    "status": payment_status_code,
                    "message": "Payment completed",
                    "payment_response_data": payment_response_data,
                    "booking_data": booking_data
                }
                book_time.active = False
                book_time.save()
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": payment_status_code,
                    "message": "Booking completed",
                    "price": price,
                    "booking_data": booking_data
                }
                book_time.active = False
                book_time.save()
        response_data = {
            "status": "success",
            "message": "Booking completed",
            "price": price,
            "booking_data": booking_data
        }
        book_time.active = False
        book_time.save()

        return Response(response_data, status=status.HTTP_201_CREATED)


# Get all doctor bookings
class DoctorBookingsListAPIView(generics.ListAPIView):
    queryset = BookDoctor.objects.all()
    serializer_class = DoctorBookingsSerializer


# Get one doctor booking
class DoctorBookingRetrieveAPIView(generics.RetrieveAPIView):
    queryset = BookDoctor.objects.all()
    serializer_class = DoctorBookingsSerializer


# Offers ===============
class DoctorOffersListAPIView(generics.ListAPIView):
    serializer_class = OfferDoctorSerializer
    queryset = OfferDoctor.objects.all()


class DoctorOffersRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OfferDoctorSerializer
    queryset = OfferDoctor.objects.all()


class NurseOffersListAPIView(generics.ListAPIView):
    serializer_class = OfferNurseServiceSerializer
    queryset = OfferNurseService.objects.all()


class NurseOffersRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OfferNurseServiceSerializer
    queryset = OfferNurseService.objects.all()


class PhysioOffersListAPIView(generics.ListAPIView):
    serializer_class = OfferPhysioServiceSerializer
    queryset = OfferNurseService.objects.all()


class PhysioOffersRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OfferPhysioServiceSerializer
    queryset = OfferNurseService.objects.all()


class LabOffersListAPIView(generics.ListAPIView):
    serializer_class = OfferLabAnalyticSerializer
    queryset = OfferNurseService.objects.all()


class LabOffersRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OfferLabAnalyticSerializer
    queryset = OfferNurseService.objects.all()


# =========================================================
class NurseListAPIView(generics.ListAPIView):
    queryset = NurseUser.objects.all()
    serializer_class = NurseSerializer


class NurseServiceListAPIView(generics.ListAPIView):
    queryset = NurseService.objects.all()
    serializer_class = NurseServiceSerializer


class NurseServiceTimesListAPIView(generics.ListAPIView):
    queryset = NurseServiceTimes.objects.all()
    serializer_class = NurseServiceTimesSerializer


class NurseServiceAllTimesListAPIView(generics.ListAPIView):
    serializer_class = NurseServiceTimesSerializer

    def get_queryset(self):
        service_id = self.kwargs['service_id']  # Assuming the service_id is passed in the URL
        queryset = NurseServiceTimes.objects.filter(service=service_id)
        return queryset


class BookNurseAPIView(generics.CreateAPIView):
    queryset = BookNurse.objects.all()
    serializer_class = BookNurseSerializer

    # we will uncomment this line after Authorization error fix
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = PatientUser.objects.filter(id=request.data.get("patient")).first()
        service = NurseService.objects.filter(id=request.data.get("service")).first()
        nurse = NurseUser.objects.get(id=request.data.get("nurse"))
        time = NurseServiceTimes.objects.get(id=request.data.get("time"))

        booking = serializer.save(
            patient=patient,
            service=service,
            nurse=nurse,
            time=time,
            status="PEN",
        )
        time.active = False
        time.save()

        #  handling payment using Stripe
        return Response({"message": "Booking completed"}, status=status.HTTP_201_CREATED)


class NurseBookingsListAPIView(generics.ListAPIView):
    queryset = BookNurse.objects.all()
    serializer_class = NurseBookingsSerializer


# Get one doctor booking
class NurseBookingRetrieveAPIView(generics.RetrieveAPIView):
    queryset = BookNurse.objects.all()
    serializer_class = NurseBookingsSerializer


# =========================================================
# Physiotherapist & booking Physiotherapist

class PhysioListAPIView(generics.ListAPIView):
    queryset = PhysiotherapistUser.objects.all()
    serializer_class = PhysioUserSerializer


class PhysioServiceListAPIView(generics.ListAPIView):
    queryset = PhysiotherapistService.objects.all()
    serializer_class = PhysioServiceSerializer


class PhysioServiceTimesListAPIView(generics.ListAPIView):
    queryset = PhysiotherapistServiceTimes.objects.all()
    serializer_class = PhysioServiceTimesSerializer


class PhysioServiceAllTimesListAPIView(generics.ListAPIView):
    serializer_class = NurseServiceTimesSerializer

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        queryset = PhysiotherapistServiceTimes.objects.filter(service=service_id)
        return queryset


class BookPhysioAPIView(generics.CreateAPIView):
    serializer_class = BookPhysioSerializer

    # we will uncomment this line after Authorization error fix
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = PatientUser.objects.filter(id=request.data.get("patient")).first()
        service = PhysiotherapistService.objects.filter(id=request.data.get("service")).first()
        physio = PhysiotherapistUser.objects.get(id=request.data.get("physio"))
        time = PhysiotherapistServiceTimes.objects.get(id=request.data.get("time"))

        booking = serializer.save(
            patient=patient,
            service=service,
            physio=physio,
            time=time,
            status="PEN",
        )
        time.active = False
        time.save()

        #  handling payment using Stripe
        return Response({"message": "Booking completed"}, status=status.HTTP_201_CREATED)


class PhysioBookingsListAPIView(generics.ListAPIView):
    queryset = BookPhysio.objects.all()
    serializer_class = PhysioBookingsSerializer


# Get one doctor booking
class PhysioBookingRetrieveAPIView(generics.RetrieveAPIView):
    queryset = BookPhysio.objects.all()
    serializer_class = PhysioBookingsSerializer


# =========================================================
# pharmacy & booking medicine

class PharmacyUserListAPIView(generics.ListAPIView):
    queryset = PharmacyUser.objects.all()
    serializer_class = PharmacyUserSerializer


class PharmacyMedicineListAPIView(generics.ListAPIView):
    queryset = PharmacyMedicine.objects.all()
    serializer_class = PharmacyMedicineSerializer


class PharmacyListAPIView(generics.ListAPIView):
    queryset = PharmacyDetail.objects.all()
    serializer_class = PharmacySerializer


class BookMedicineAPIView(generics.CreateAPIView):
    serializer_class = BookMedicineSerializer

    # we will uncomment this line after Authorization error fix
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = PatientUser.objects.filter(id=request.data.get("patient")).first()
        pharma = PharmacyDetail.objects.filter(id=request.data.get("pharma")).first()
        medicine = PharmacyMedicine.objects.get(id=request.data.get("medicine"))
        count = request.data.get('count')
        if medicine.count >= int(count):
            booking = serializer.save(
                patient=patient,
                pharma=pharma,
                medicine=medicine,
                count=count,
                status="PEN",
            )
            # update medicine count
            medicine.count -= int(count)
            medicine.save()

        else:
            return Response({'detail': 'Not enough stock available for the requested medicine.'},
                            status=status.HTTP_400_BAD_REQUEST)

        #  handling payment using Stripe
        return Response({"message": "Booking completed"}, status=status.HTTP_201_CREATED)


# =========================================================
# lab & booking analytic


class LabUserListAPIView(generics.ListAPIView):
    queryset = LapUser.objects.all()
    serializer_class = LabUserSerializer


class LabUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = LapUser.objects.all()
    serializer_class = LabUserSerializer

class LabServiceListAPIView(generics.ListAPIView):
    queryset = LabService.objects.all()
    serializer_class = LabServiceSerializer


class LabServiceRetrieveAPIView(generics.RetrieveAPIView):
    queryset = LabService.objects.all()
    serializer_class = LabServiceSerializer


class LabListAPIView(generics.ListAPIView):
    queryset = LabDetail.objects.all()
    serializer_class = LabDetailSerializer


class LabRetrieveAPIView(generics.RetrieveAPIView):
    queryset = LabDetail.objects.all()
    serializer_class = LabDetailSerializer


class BookAnalyticAPIView(generics.CreateAPIView):
    serializer_class = BookAnalyticSerializer

    # we will uncomment this line after Authorization error fix
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = PatientUser.objects.filter(id=request.data.get("patient")).first()
        service = LabService.objects.filter(id=request.data.get("service")).first()
        lab = LabDetail.objects.get(id=request.data.get("lab"))

        booking = serializer.save(
            patient=patient,
            service=service,
            lab=lab,
            status="PEN",
        )
        #  handling payment using Stripe
        return Response({"status": "success", "message": "Booking completed"}, status=status.HTTP_201_CREATED)


class LabBookingsListAPIView(generics.ListAPIView):
    queryset = BookAnalytic.objects.all()
    serializer_class = AnalyticBookingsSerializer


# Get one doctor booking
class LabBookingRetrieveAPIView(generics.RetrieveAPIView):
    queryset = BookAnalytic.objects.all()
    serializer_class = AnalyticBookingsSerializer


# =========================================================
class SliderList(generics.ListAPIView):
    queryset = models.Slider.objects.all()
    serializer_class = serializers.SliderSerializer


class DoctorList(generics.ListCreateAPIView):
    queryset = models.DoctorUser.objects.all()
    serializer_class = serializers.DoctorSerializers


class DoctorListFilteredCategory(generics.ListAPIView):
    queryset = models.DoctorUser.objects.filter()
    serializer_class = serializers.DoctorFilterSerializers

    def get_queryset(self):
        cat_id = self.kwargs['cat']
        doctors = models.DoctorUser.objects.filter(category_id=cat_id)
        return doctors


class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DoctorUser.objects.all()
    serializer_class = serializers.DoctorDetailSerializers


class DoctorTimesList(generics.ListAPIView):
    queryset = models.DoctorTimes.objects.all()
    serializer_class = serializers.DoctorTimesSerializers


class PatientList(generics.ListCreateAPIView):
    queryset = models.PatientUser.objects.all()
    serializer_class = serializers.PatientSerializers


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.PatientUser.objects.all()
    serializer_class = serializers.PatientDetailSerializers


class BookDoctorList(generics.ListAPIView):
    queryset = models.BookDoctor.objects.all()
    serializer_class = serializers.BookDoctorSerializers

    # Override Query set
    # def get_queryset(self):
    #    book_id = self.kwargs['pk']
    #    book = models.BookDoctor.objects.get(id=book_id)
    #    book_detail = models.BookDoctor.objects.filter(book=book)
    #    return book_detail
