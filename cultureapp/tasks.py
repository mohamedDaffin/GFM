
from celery import shared_task
from .models import Culture,Arroser
from django.core.mail import send_mail

@shared_task
def envoyer_notifications():
    cultures = Culture.objects.all()
    for culture in cultures:
        notification = culture.notifier_recolte()
        
            


@shared_task
def envoyer_notification_arroser():
    arroses = Arroser.objects.filter(do_culture=False)
    for arrose in arroses:
        notification = arrose.notifier_arroser()
        if notification:
            confirmation_link = f"http://127.0.0.1:8000/done/{arrose.culture.id}/"
            send_mail(
                f"Notification pour {arrose.culture.name}",
                f"Veuillez cliquer sur ce lien pour marquer la tâche comme effectuée : {confirmation_link}",
                'mohamedyakeri@gmail.com',
                [arrose.user.email],
                fail_silently=False,
            )

@shared_task
def remise_a_zero():
    arroses = Arroser.objects.filter(do_culture=True)
    for arrose in arroses:
        notification = arrose.remise_a_zero()
        if notification:
            arrose.do_culture = False
            arrose.save()