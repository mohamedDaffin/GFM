from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from django.utils.text import slugify
from datetime import datetime
from django.core.mail import send_mail



class Aliment(models.Model):
    name_aliment = models.CharField(max_length=50)
    quantite = models.BigIntegerField(default = 0)
    def __str__(self):
        return self.name_aliment

class Classe(models.Model):
    name_classe = models.CharField(max_length=50)
    def __str__(self):
        return self.name_classe


class TypeAnimal(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE,null = True)
    name_type = models.CharField(max_length=50,unique =True)
    quantite = models.IntegerField(default=0)  
    aliment = models.ManyToManyField(Aliment)
    nombre = models.IntegerField(default=0)
   # enclo = models.CharField(unique = True ,default = " ",max_length=50)
    slug = models.SlugField(unique=True,blank=True)

    def __str__(self):
        return self.name_type
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_type)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("animal", kwargs={"slug": self.slug})
    

class PlanningType(models.Model):
    matin = models.BooleanField(default=False)
    midi = models.BooleanField(default=False)
    soir = models.BooleanField(default=False)
    do_type = models.BooleanField(default=False)
    do_matin = models.BooleanField(default=False)
    do_midi = models.BooleanField(default=False)
    do_soir = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    typee = models.ManyToManyField(TypeAnimal)
    def ok(self):
        alls = PlanningType.objects.all()
        for g in alls:
            g.do_matin = False
            g.do_midi = False
            g.do_soir = False
            g.save()
        return True
    def nourrir_animal(self):
        messages = []
        plans = PlanningType.objects.all()
        for plan in plans:
            types = list(plan.typee.all())

            for typee in types:
                try:
                    heure_actu = datetime.now().hour
                    if heure_actu == 15 and plan.matin:
                        message = {"type":"matin","texte":f"Notification:Rappel matinal pour nourrir les {typee.name_type}"}
                        messages.append(message)
                    if heure_actu == 15 and plan.midi:
                        message = {"type":"midi","texte":f"Notification:Rappel de midi pour nourrir les {typee.name_type}"}
                        messages.append(message)
                    if heure_actu == 14 and plan.soir: 
                        message = {"type":"soir","texte":f"Notification:Rappel du soir pour nourrir les {typee.name_type}"}
                        messages.append(message)
                except Exception as e:
                    print("Erreur:",e)
        return messages


class Animal(models.Model):
    code = models.CharField(max_length=50, blank=True)
    name_animal = models.CharField(max_length=50)
    typee = models.ForeignKey(TypeAnimal,null=True ,on_delete=models.CASCADE)
    description = models.TextField(default =" ")
    poids = models.IntegerField(default=" ")
    
    naissance = models.BooleanField(default = False)
    vente = models.BooleanField(default = False)
    deces = models.BooleanField(default = False)
    achat = models.BooleanField(default = False)

    sexe = models.CharField(max_length=2,
    choices = [
        ('M','M'),
        ('F','F'),
    ],
    default = 'M',
    
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_enregistrer = models.DateTimeField(null=True)
    def __str__(self):
        return self.name_animal
    
    def get_absolute_url(self):
        return reverse("editer_animal", kwargs={"id": self.pk})
    
    def save(self,*args, **kwargs):
        if self.code == "":
            self.code = str(uuid.uuid4()).upper()[:4]
        return super().save(*args, **kwargs)




class AnimalPlanning(models.Model):
    do_animal = models.BooleanField(default=False)
    motif = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ManyToManyField(Animal)
    date_fin = models.DateTimeField( auto_now=False, auto_now_add=False)

    def envoyer_notifier_animal(self,message):
        send_mail(
            f"Rappel sur {self.motif}",
            message,
            'mohamedyakeri@gmail.com',
            [self.user.email],
            fail_silently = False,
        )

    def notifier_planning(self):
        typee = AnimalPlanning.objects.all()
        messages = []
        animal = self.animal.all()
        for an in animal:
            message = ""
            to_day = datetime.now().date()
            if isinstance(self.date_fin , datetime):
                self.date_fin = self.date_fin.date()
            if to_day >= self.date_fin and not self.do_animal:
                message = f"Il est temps d'amener {an.name_animal} chez le veterinaire"
                messages.append(message)
                self.envoyer_notifier_animal(message)
            elif (self.date_fin - to_day).days <= 3 and not self.do_animal:
                message = f"Il reste moins de 3 jours pour la visite de {an.name_animal} chez le veterinaire."
                messages.append(message)
                self.envoyer_notifier_animal(message)
        return messages if messages else "Aucune notification a envoyer"



class Nourriture(models.Model):
    aliment = models.ForeignKey(Aliment, verbose_name=("aliment"), on_delete=models.CASCADE)
    Type = models.ForeignKey(TypeAnimal, verbose_name=("name_type"), on_delete=models.CASCADE)
    quantite = models.BigIntegerField(default=0)
    date = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return self.Quantite

    def get_absolute_url(self):
        return reverse("nourrir", kwargs={"id": self.pk})


class Historique(models.Model):

    deces = models.IntegerField(default=0)
    naissance = models.IntegerField(default=0)
    achat = models.IntegerField(default = 0)
    vente = models.IntegerField(default=0)
    animal = models.ForeignKey(Animal, on_delete=models.SET_NULL,null=True,blank=True)
    Type = models.ForeignKey(TypeAnimal, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("delete_animal_vente", kwargs={"id": self.pk})


class Histoire(models.Model):
    entre = models.IntegerField(default=0)
    sortie = models.IntegerField(default=0)
    difference = models.IntegerField(default=0)
    aliment = models.ForeignKey('Aliment', on_delete=models.SET_NULL, null=True, blank=True)
    nourrir = models.ForeignKey('Nourriture', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.aliment} - Entrée: {self.entre}, Sortie: {self.sortie}"

# Create your models here.
