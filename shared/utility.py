import re
import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
import phonenumbers
from decouple import config
from twilio.rest import Client


email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9._-]+\.[A-Z|a-z]{2,7}\b")
phone_regex = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")
username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")


def check_email_or_phone(email_or_phone):
    phone_number = phonenumbers.parse(email_or_phone)

    if re.fullmatch(email_regex, email_or_phone):
        email_or_phone = "email"
    elif phonenumbers.is_valid_number(phone_number):
        email_or_phone = 'phone_number'
    else:
        data = {
            'success': False,
            'message': 'Email yoki telefon raqamingiz noto\'g\'ri'
        }
        raise ValidationError(data)
    return email_or_phone



def check_user_tupe(user_input):
    # phone_number = phonenumbers.parse(user_input)

    if re.fullmatch(email_regex, user_input):
        user_input = 'email'
    elif re.fullmatch(phone_regex, user_input):
        user_input = 'phone'
    elif re.fullmatch(username_regex, user_input):
        user_input = 'username'
    else:
        data = {
            "success": False,
            "message": "Email, username, yoki telefon raqamingiz noto'g'ri!"
        }
        raise ValidationError(data)
    return user_input


class EmailThreed(threading.Thread):  # threading.Thread -> dasturga halal bermagan holda u bn paralel ishlashi uchun

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self): # ishga tushirish uchun
        self.email.send()


class Email:

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']] # qaysi emailga yuborish
        )

        if data.get('content_type') == 'html': # data ni tekshirish
            email.content_subtype = 'html'
        EmailThreed(email).start()


def send_email(email, code): # emailga code yuborish
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {'code': code}
    )
    Email.send_email(
        {
            'subject': "Ro'yxatdan o'tish",
            'to_email': email,
            'body': html_content,
            'content_type': "html"
        }
    )


def send_phone_code(phone, code):
    account_sid = config('account_sid')
    auth_token = config('auth_token')
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"Sizning tasdiqlash kodingiz: {code}\n",
        from_="+998889480405",
        to=f"{phone}"
    )
    