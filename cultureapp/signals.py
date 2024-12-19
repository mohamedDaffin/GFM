from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models  import Historique,Production
from datetime import datetime


@receiver(post_save , sender=Production)
def entre_produit(sender,instance,created,*args, **kwargs):
    if created:
        Historique.objects.create(culture=instance.culture,date_entre = datetime.now,quantite_entre = instance.quantite_produit,tolal = instance.quantite_produit)
