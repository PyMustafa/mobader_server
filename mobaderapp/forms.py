from django import forms
from django.forms import ModelForm, DateInput

from .models import (
    DoctorTimes,
    BookDoctor,
    BookNurse,
    BookPhysio,
    BookAnalytic,
    BookMedicine,
)


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

