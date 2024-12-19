from django import forms
from django.contrib.auth.models import Group, User,Permission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes.models import ContentType
from .models import Employe
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class EmployeCreationForm(UserCreationForm):
    
    class Meta:
        model = Employe
        fields = ['username']
        labels = {
            'username':'Nom d\'utilisateur',
        }
        
    def __init__(self, *args, **kwargs):
        super(EmployeCreationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class Edite_EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['username','first_name','last_name','email','numero','image']
        labels = {
            'username':'Nom d\'utilisateur',
            'first_name':'Nom',
            'last_name':'Prenom',
        }
       

    def __init__(self, *args, **kwargs):
        super(Edite_EmployeForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = None


    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if not numero.isdigit():
            raise ValidationError('Votre numero doit contenir des chiffres')
        if len(numero) !=8:
            raise ValidationError('Votre numero doit content 8 chiffres')
        return numero


class UserConnectionForm(AuthenticationForm):
    class Meat:
        model = User
        fields = [
            'username',
            'password'
        ]
        labels = {
            'username':'Nom d\'utilisateur',
            'password':'Mot de passe',
        }