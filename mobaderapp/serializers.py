from rest_framework import serializers

from . import models
from .models import CustomUser, PatientUser, BookDoctor, DoctorCategory, DoctorUser, NurseUser, NurseService, \
    NurseServiceTimes, BookNurse, PhysiotherapistUser, PhysiotherapistService, PhysiotherapistServiceTimes, BookPhysio, \
    PharmacyUser, PharmacyMedicine, PharmacyDetail, BookMedicine, LapUser, LabService, LabDetail, BookAnalytic, \
    DoctorTimes, Offer, OfferDoctor, OfferNurseService, OfferPhysioService, OfferLabAnalytic


# Authentication Serializers
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['user_type'] = 8
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PatientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientUser
        fields = ['username', 'mobile', 'email', 'password']


class UserVerifyOTPSerializer(serializers.Serializer):
    verification_code = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    mobile = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        help_text='Enter your password.'
    )


# Reset Password serializers
class ResetPassRequestSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(write_only=True, help_text='Enter your phone number.')


class ResetPassSerializer(serializers.Serializer):
    verification_code = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        help_text='Enter your password.')


# =========================================================
# doctors & booking doctor


class DoctorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorCategory
        fields = '__all__'


class BookDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDoctor
        fields = ["patient", "doctor", "book_time", "is_paid", "book_type"]


class CategoryDoctorsSerializer(serializers.ModelSerializer):
    # auth_user_id = CustomUserSerializer()

    class Meta:
        model = DoctorUser
        fields = ['id', "profile_pic", "price", "mobile", "address"]

    def __init__(self, *args, **kwargs):
        super(CategoryDoctorsSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class DoctorBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDoctor
        fields = '__all__'


# =========================================================
# nurses & booking nurse

class NurseBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNurse
        fields = '__all__'


class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseUser
        fields = '__all__'


class NurseServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseService
        fields = '__all__'


class NurseServiceTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NurseServiceTimes
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(NurseServiceTimesSerializer, self).__init__(*args, **kwargs)
            self.Meta.depth = 2


class BookNurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNurse
        fields = ['patient', 'service', 'nurse', 'time']


# =========================================================
# Physiotherapist & booking Physiotherapist

class PhysioBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPhysio
        fields = '__all__'


class PhysioUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysiotherapistUser
        fields = '__all__'


class PhysioServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysiotherapistService
        fields = '__all__'


class PhysioServiceTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysiotherapistServiceTimes
        fields = '__all__'


class BookPhysioSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPhysio
        fields = ['patient', 'physio', 'service', 'time']


# =========================================================
# pharmacy & booking medicine

class PharmacyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyUser
        fields = '__all__'


class PharmacyMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyMedicine
        fields = '__all__'


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyDetail
        fields = '__all__'


class BookMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMedicine
        fields = ['patient', 'pharma', 'medicine', 'count']


# =========================================================
# lab & booking analytic

class LabUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LapUser
        fields = '__all__'


class LabServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabService
        fields = '__all__'


class LabDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabDetail
        fields = '__all__'


class BookAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAnalytic
        fields = ['patient', 'lab', 'service']


class AnalyticBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAnalytic
        fields = '__all__'



# Offers ==========================
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class OfferDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDoctor
        fields = ['id', 'offer', 'doctor']
        depth = 1


class OfferNurseServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferNurseService
        fields = ['id', 'offer', 'nurse_service']
        depth = 1


class OfferPhysioServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferPhysioService
        fields = ['id', 'offer', 'physio_service']
        depth = 1


class OfferLabAnalyticSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferLabAnalytic
        fields = ['id', 'offer', 'lab_analytic']
        depth = 1


# ===========================================================
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slider
        fields = ["id", "title", "thumbnail", "description"]


class DoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorUser
        fields = ["id", "address", "mobile", "category_id", "price", "profile_pic"]

    def __init__(self, *args, **kwargs):
        super(DoctorSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class DoctorFilterSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorUser
        fields = ["id", "address", "mobile", "category_id", "price", "profile_pic"]
        depth = 1


class DoctorDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorUser
        fields = ["id", "address", "mobile", "category_id", "price", "profile_pic"]

    def __init__(self, *args, **kwargs):
        super(DoctorDetailSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class DoctorTimesSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorTimes
        fields = ["id", "doctor", "day", "start_time", "end_time"]

    def __init__(self, *args, **kwargs):
        super(DoctorTimesSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class PatientSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.PatientUser
        fields = ["id", "address", "mobile"]

    def __init__(self, *args, **kwargs):
        super(PatientSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class PatientDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.PatientUser
        fields = ["id", "address", "mobile"]

    def __init__(self, *args, **kwargs):
        super(PatientDetailSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class BookDoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.BookDoctor
        fields = ["id", "patient", "doctor", "book_time", "is_paid", "book_type", "meeting_room"]

    def __init__(self, *args, **kwargs):
        super(BookDoctorSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1
