from django.conf import settings
from django.core.mail import send_mail


def send_email_to_users(emails, body, subject):
    return send_mail(
        subject=subject,
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False,
        html_message=body
    )
