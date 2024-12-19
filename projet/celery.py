import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE','projet.settings')
app = Celery('projet')
app.autodiscover_tasks(['animaleapp','cultureapp'])
app.config_from_object('django.conf:settings',namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule ={
    'Rapppel-Soins':{
        'task':'animaleapp.tasks.aller_veterinaire',
        'schedule':crontab(minute="*/2"),
    },
    'Aliment-matin':{
        'task':'animaleapp.tasks.alimenter',
        'schedule':crontab(minute="*/2"),
    },
    'Aliment-soir':{
        'task':'animaleapp.tasks.alimenter',
        'schedule':crontab(minute="*/2"),
    },
    'Aliment-midi':{
        'task':'animaleapp.tasks.alimenter',
        'schedule':crontab(minute="*/2"),
    },
    'Aliment-repos':{
        'task':'animaleapp.tasks.repos',
        'schedule':crontab(minute="*/2"),
    },
    'envoyer-notifications-toutes-les-24-heures': {
        'task': 'cultureapp.tasks.envoyer_notifications',
        'schedule':crontab(minute="*/2"),
    },

    'envoyer-notification-pour arrosage':{
        'task':'cultureapp.tasks.envoyer_notification_arroser',
        'schedule':crontab(minute="*/2"),
    },

    'envoyer-notification-matin':{
        'task':'cultureapp.tasks.envoyer_notification_arroser',
        'schedule':crontab(minute="*/2"),
    },
    'envoyer-notification-midi':{
        'task':'cultureapp.tasks.envoyer_notification_arroser',
        'schedule':crontab(minute="*/2"),
    },
    'envoyer-notification-soir':{
        'task':'cultureapp.tasks.envoyer_notification_arroser',
        'schedule':crontab(minute="*/2"),
    },
    'envoyer-notification-soir':{
        'task':'cultureapp.tasks.envoyer_notification_arroser',
        'schedule':crontab(minute="*/2"),
    },
    'envoyer-notification-soir':{
        'task':'cultureapp.tasks.envoyer_notification_arroser',
        'schedule':crontab(minute="*/2"),
    },
    'envoyer-notification-soir':{
        'task':'cultureapp.tasks.envoyer_notification_arroser',
        'schedule':crontab(minute="*/2"),
    },
    'reinitialisation':{
        'task':'cultureapp.tasks.remise_a_zero',
        'schedule':crontab(minute="*/2"),
     },
    
}