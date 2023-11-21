from rest_framework import serializers

from . import models
from .models import CustomUser, PatientUser, BookDoctor, DoctorCategory, DoctorUser, NurseUser, NurseService, \
    NurseServiceTimes, BookNurse, PhysiotherapistUser, PhysiotherapistService, PhysiotherapistServiceTimes, BookPhysio, \
    PharmacyUser, PharmacyMedicine, PharmacyDetail, BookMedicine, LapUser, LabService, LabDetail, BookAnalytic, DoctorTimes


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
    auth_user_id = CustomUserSerializer()

    class Meta:
        model = PatientUser
        fields = ['auth_user_id', 'profile_pic', 'mobile', 'address']

    def create(self, validated_data):
        base_user_data = validated_data.pop('auth_user_id')
        custom_user_serializer = CustomUserSerializer(data=base_user_data)
        if custom_user_serializer.is_valid():
            custom_user = custom_user_serializer.save()
            patient_user = PatientUser.objects.create(auth_user_id=custom_user, **validated_data)
            return patient_user
        else:
            raise serializers.ValidationError(custom_user_serializer.errors)


class UserVerifyOTPSerializer(serializers.Serializer):
    verification_code = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
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
        fields = ['id', 'auth_user_id', "profile_pic", "price", "mobile_phone", "address"]

    def __init__(self, *args, **kwargs):
            super(CategoryDoctorsSerializer, self).__init__(*args, **kwargs)
            self.Meta.depth = 1


# =========================================================
# nurses & booking nurse


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


class BookNurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookNurse
        fields = ['patient', 'service', 'nurse', 'time']


# =========================================================
# Physiotherapist & booking Physiotherapist

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


# ===========================================================
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Slider
        fields = ["id", "title", "thumbnail", "description"]


class DoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorUser
        fields = ["id", "auth_user_id", "address", "mobile_phone", "category_id", "price", "profile_pic"]

    def __init__(self, *args, **kwargs):
        super(DoctorSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class DoctorFilterSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorUser
        fields = ["id", "auth_user_id", "address", "mobile_phone", "category_id", "price", "profile_pic"]

        def __init__(self, *args, **kwargs):
            super(DoctorFilterSerializers, self).__init__(*args, **kwargs)
            self.Meta.depth = 1


class DoctorDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorUser
        fields = ["id", "auth_user_id", "address", "mobile_phone", "category_id", "price", "profile_pic"]

    def __init__(self, *args, **kwargs):
        super(DoctorDetailSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class DoctorTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DoctorTimes
        fields = ["id", "doctor", "start_time", "end_time"]

    def __init__(self, *args, **kwargs):
        super(DoctorTimesSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class PatientSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.PatientUser
        fields = ["id", "auth_user_id", "address", "mobile"]

    def __init__(self, *args, **kwargs):
        super(PatientSerializers, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


class PatientDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.PatientUser
        fields = ["id", "auth_user_id", "address", "mobile"]

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