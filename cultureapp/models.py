from django.db import models
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import reverse
class Champ(models.Model):
    name_champ = models.CharField( max_length=50)
    def __str__(self):
        return self.name_champ
    def get_absolute_url(self):
        return reverse("show_culture_detail", kwargs={"id": self.pk})
    

class Culture(models.Model):
    name_culture = models.CharField(max_length=50)
    date_plante = models.DateTimeField( auto_now=False, auto_now_add=False)
    date_recolte = models.DateTimeField(auto_now=False, auto_now_add=False)
    # date_arroser = models.DateTimeField(auto_now=True, auto_now_add=True)
    champ = models.ForeignKey(Champ, on_delete=models.CASCADE)


    def __str__(self):
        return self.name_culture

    def envoyer_notification(self,message):
        send_mail(
            'Rappel de Récolte',
            message,
            'mohamedyakeri@gmail.com',
            ['mohamedyakeri@gmail.com'],
            fail_silently = False,
        )

    def notifier_recolte(self):
        today = datetime.now().date()
        message = "okml"
        if isinstance(self.date_recolte, datetime):
            self.date_recolte = self.date_recolte.date()

        if today >= self.date_recolte:
            message = f"Notification: Il est temps de recolter {self.name_culture}  du champ {self.champ}!"
            self.envoyer_notification(message)
            return message
        elif (self.date_recolte - today).days <= 3:
            message = f"Rappel : La recolte de {self.name_culture} sera dans {(self.date_recolte - today).days} jours."
            self.envoyer_notification(message)
            return message
      
        return message
        
class Arroser(models.Model):
    matin_culture = models.BooleanField(default=False)
    midi_culture = models.BooleanField(default=False)
    soir_culture = models.BooleanField(default=False)
    date_arroser = models.DateTimeField( auto_now=False, auto_now_add=False )
    culture = models.ForeignKey( Culture, on_delete=models.CASCADE )
    do_culture = models.BooleanField( default=False )
    champ = models.ForeignKey( Champ,on_delete=models.CASCADE )
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)
    def envoyer_notification(self,message):
        send_mail(
            'Rappel de Récolte',
            message,
            'mohamedyakeri@gmail.com',
            ['mohamedyakeri@gmail.com'],
            fail_silently = False,
        )

    def notifier_arroser(self):
        message=""
        if datetime.now().hour == 16 and self.matin:
            message = f"Notification: Rappel matinal il est temps d\'arroser {self.culture} du champ {self.name_champ}"
            self.envoyer_notification(message)
            return message

        elif datetime.now().hour == 16 and self.midi:
            message = f'Notification: Rappel de midi il est temps d\'arroser {self.culture} du champ {self.name_champ}'
            self.envoyer_notification(message)
            return message

        elif datetime.now().hour == 18  and self.soir:
            message = f'Notification: Rappel du soir il est temps d\'arroser {self.culture } du champ {self.name_champ}'
            self.envoyer_notification(message)
            return message
        return message


    def remise_a_zero(self):
        if datetime.now().hour == 17:
            return True
        return False

class Production(models.Model):
    quantite_produit = models.IntegerField(default=0)
    entre = models.BooleanField(default=0)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.quantite_produit
    

class Historique(models.Model):
    quantite_sorti = models.IntegerField(default = 0) 
    date_sorti = models.DateTimeField( auto_now=True, auto_now_add=False)
    quantite_entre = models.IntegerField(default = 0)
    tolal = models.IntegerField(default=0)
    date_entre = models.DateTimeField(auto_now=True, auto_now_add=False)
    culture = models.ForeignKey(Culture, on_delete=models.CASCADE)
    


# Create your models here.
