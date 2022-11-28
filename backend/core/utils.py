from django.core.mail import send_mail
from django.conf import settings
import math, random,uuid

def send_custom_email(subject,message,recipient):
    subject = subject
    message = message
    send_mail(subject, message,
                settings.DEFAULT_FROM_EMAIL, [recipient])

def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'media/' + filename
