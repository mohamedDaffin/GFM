from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Animal,Historique

@receiver(post_save,sender=Animal)
def naiss_vente(sender,instance,created,*args, **kwargs):
    if created:
        historique,created = Historique.objects.get_or_create(animal=instance,Type=instance.typee)
        if instance.naissance:
            historique.naissance += 1
        else:
            historique.achat += 1
        historique.save()





@receiver(post_save,sender=Animal)
def update_animal(sender,instance,created,*args, **kwargs):
    if created:
        type_animal = instance.typee
        if type_animal:
            type_animal.nombre +=1
            type_animal.save()



@receiver(post_delete,sender=Animal)
def delete_animal(sender,instance,*args, **kwargs):
    
    type_animal = instance.typee
    if type_animal:
        type_animal.nombre -=1
        type_animal.save()
