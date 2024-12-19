from django.db import models
from django.contrib.auth.models import User
class Employe(User):
    numero = models.CharField(max_length=50)
    image = models.ImageField(null =True,blank=True)
    def __str__(self):
        return self.username


    