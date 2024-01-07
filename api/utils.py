from django.core.mail import send_mail
from django.conf import settings



def send_otp_email(email, otp):
    subject = 'Your One Time Password (OTP)'
    message = f'Your OTP is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
