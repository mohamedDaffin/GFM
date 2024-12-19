from django.core.mail import send_mail
from .models import AnimalPlanning,PlanningType
from celery import shared_task
from django.db.models import Q
@shared_task
def aller_veterinaire():
    plannings = AnimalPlanning.objects.filter(do_animal=False)
    for planning in plannings:
        notifier = planning.notifier_planning()

@shared_task
def alimenter():
    plannings = PlanningType.objects.filter(Q(do_matin = False)|Q(do_midi = False)|Q(do_soir = False))
    print(plannings)
    for planning in plannings:
       
        notifiers = planning.nourrir_animal()
        for notifier in notifiers:
            if notifier["type"] == "matin" and planning.do_matin == False:
                confirm_link = f"http://127.0.0.1:8000/animal/done_matin/{planning.id}/"
                send_mail(
                    notifier["texte"],
                    f"Veillez cliquer sur le lien pour (matinal) marquer la tache comme effectuer {confirm_link}",
                    'mohamedyakeri@gmail.com',
                    [planning.user.email],
                    fail_silently = False
                )
            elif notifier["type"] == "midi" and planning.do_midi == False:
                confirm_link = f"http://127.0.0.1:8000/animal/done_midi/{planning.id}/"

                send_mail(
                    notifier["texte"],
                    f"veillez cliquer sur le lien pour (midi) marquer la tache comme effectuer {confirm_link}",
                    'mohamedyakeri@gmail.com',
                    [planning.user.email],
                    # [planning.user.email],
                    fail_silently = False

                )
            elif notifier["type"] == "soir" and planning.do_soir == False:
                confirm_link = f"http://127.0.0.1:8000/animal/done_soir/{planning.id}/"
                send_mail(
                    notifier["texte"],
                    f"veillez cliquer sur le lien pour (soir) marquer la tache comme effectuer {confirm_link}",
                    'mohamedyakeri@gmail.com',
                    [planning.user.email],

                    # [planning.user.email],
                    fail_silently = False
                )



@shared_task
def repos():
    plannings = PlanningType.objects.filter(Q(do_matin = True)|Q(do_midi = True)|Q(do_soir = True))
    for planning in plannings:
        notif = planning.ok()
        print(notif)
