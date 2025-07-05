# users/services.py
from django.core.mail import send_mail
from django.conf import settings
from .utils import create_invite_token

def send_invitation_email(user):
    token = create_invite_token(user.id)
    activation_link = f"https://example.com/complete-registration/?token={token}"
    
    subject = "Завершите регистрацию"
    message = f"Здравствуйте, {user.full_name}!\n\nПерейдите по ссылке, чтобы завершить регистрацию:\n{activation_link}"
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
