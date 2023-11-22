from django import forms
from django.forms import ModelForm, DateInput

from .models import (
    DoctorTimes,
    BookDoctor,
    BookNurse,
    BookPhysio,
    BookAnalytic,
    BookMedicine,
    PatientUser,
    CustomUser,
)

# Register
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        phone_number_processed = re.match("^\+?(\d+)$", phone_number)
        if phone_number_processed and len(phone_number_processed[1]) >= 9:
            if len(phone_number_processed[1]) == 9:
                return phone_number_processed[1]

            phone_number_stripped = re.match("^966(\d{9})$", phone_number_processed[1])
            if phone_number_stripped:
                return phone_number_stripped[1]
        raise forms.ValidationError("Invalid Phone Number. Must satisfy: +966123456789")
        
        
# Login for all users
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EventForm(ModelForm):
    class Meta:
        model = DoctorTimes
        widgets = {
            "start_time": DateInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }
        fields = ["title", "start_time", "end_time"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class ServiceVisitBooking(ModelForm):
    class Meta:
        model = BookDoctor
        fields = "__all__"

    def clean_patient_address(self):
        print("Finish Service")
        patient_addr = self.cleaned_data["patient_address"]
        if patient_addr != "":
            return patient_addr
        raise forms.ValidationError("Invalid Address")


class ServiceVisitBookingNurse(ModelForm):
    class Meta:
        model = BookNurse
        fields = "__all__"


class ServiceVisitBookingPhysio(ModelForm):
    class Meta:
        model = BookPhysio
        fields = "__all__"


class ServiceVisitBookingAnalytic(ModelForm):
    class Meta:
        model = BookAnalytic
        fields = "__all__"


class ServiceVisitBookingMedicine(ModelForm):
    class Meta:
        model = BookMedicine
        fields = "__all__"

