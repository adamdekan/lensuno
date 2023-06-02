from django.core.mail import send_mail


def send_email_admin(subject, body):
    send_mail(
        subject,
        body,
        "admin@lensuno.com",
        ["lensunocom@gmail.com"],
        fail_silently=True,
    )
