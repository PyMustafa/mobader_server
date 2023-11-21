from calendar import HTMLCalendar
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import DoctorTimes


def generate_otp(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def send_otp_email(email, otp):
    subject = "Mobader Verification Code"
    message = f"Your verification code is: {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

"""
def send_otp_phone(phone_number, otp):
    account_sid = (
        "ACb6e1af6e8b3359dd353e34aa121f7be6"  # Replace with your Twilio account SID
    )
    auth_token = (
        "7f077b103c1a36140db53b8813558618"  # Replace with your Twilio auth token
    )

    twilio_phone_number = "+19382532163"  # Replace with your Twilio phone number

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your OTP is: {otp}", from_=twilio_phone_number, to=phone_number
    )
    print(message)
"""

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_time__day=day)
        d = ""
        for event in events_per_day:
            d += f"<li> {event.get_html_url} </li>"

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = DoctorTimes.objects.filter(
            start_time__year=self.year, start_time__month=self.month
        )

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        return cal
