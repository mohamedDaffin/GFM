from django import forms
from .models import *

class ChampForm(forms.ModelForm):
    
    class Meta:
        model = Champ
        fields = ['name_champ']
        labels = {'name_champ':'nom de la parcelle'}
class EditeForm(forms.ModelForm):
    class Meta:
        model = Champ
        fields = ['name_champ']
        labels = {'name_champ':'nom de la parcelle'}
    


class CultureForm(forms.ModelForm):
    
    class Meta:
        model = Culture
        fields = ['champ','name_culture','date_plante','date_recolte']
        widgets = {
            'date_plante':forms.DateTimeInput(attrs = {'type':'datetime-local'}),
            'date_recolte':forms.DateTimeInput(attrs = {'type':'datetime-local'})
        }
        labels = {'champ':'parcelle','name_culture':'nom de la culture','date_plante':'date planté','date_recolte':'date recolté'}

class EditeCultureForm(forms.ModelForm):
    
    class Meta:
        model = Culture
        fields = ['champ','name_culture','date_plante','date_recolte']
        widgets = {
            'date_plante':forms.DateTimeInput(attrs = {'type':'datetime-local'}),
            'date_recolte':forms.DateTimeInput(attrs = {'type':'datetime-local'}),
            'champ':forms.HiddenInput(),
            'name':forms.HiddenInput(),
        }
        labels = {'champ':'nom de la parcelle','name_culture':'nom de la culture','date_plante':'date planté','date_recolte':'date a recolté'}


class ArroserForm(forms.ModelForm):
    
    class Meta:
        model = Arroser
        fields = ['matin_culture','midi_culture','soir_culture','date_arroser','culture','champ','user']
        widgets = {
            'date_arroser':forms.DateTimeInput(attrs = {'type':'datetime-local'}),
            'culture':forms.HiddenInput()
        }
        labels ={'matin_culture':'Arrose matin','midi_culture':'Arrose midi','soir_culture':'Arrose soir','date_arroser':'Date Enregister','champ':'nom de la parcelle'}
class EditeArroseForm(forms.ModelForm):
    
    class Meta:
        model = Arroser
        fields = ['matin_culture','midi_culture','soir_culture','date_arroser','culture','champ','user']
        widgets = {
            'date_arroser':forms.DateTimeInput(attrs = {'type':'datetime-local'}),
            'culture':forms.HiddenInput(),
            'champ':forms.HiddenInput(),
        }
        labels ={'matin_culture':'Arrose matin','midi_culture':'Arrose midi','soir_culture':'Arrose soir','date_arroser':'Date Enregister','champ':'nom de la parcelle'}
        

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields =['quantite_produit','culture']
        labels = {'quantite_produit':'quantite produite'}

class ProductionventeForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['quantite_produit','culture']
        labels = {'quantite_produit':'quantite produite'}

    

    def __init__(self,*args, **kwargs):
        super(ProductionventeForm,self).__init__(*args, **kwargs)
        self.fields['culture'].widget = forms.HiddenInput()

class Register_manyForm(forms.ModelForm):
    quantite = forms.IntegerField(label="Entrer le nombre d'animaux a enregistrer",min_value=1, required=False)

    class Meta:
        model = Culture
        fields = ['champ','name_culture','date_plante','date_recolte']
        widgets = {
            'date_plante':forms.DateTimeInput(attrs = {'type':'datetime-local'}),
            'date_recolte':forms.DateTimeInput(attrs = {'type':'datetime-local'})
        }
        labels = {'champ':'nom de la parcelle','name_culture':'nom de la culture','date_plante':'date planté','date_recolte':'date a recolté'}


class Delete_manyForm(forms.ModelForm):
    quantite = forms.IntegerField(label="Entrer le nombre d'animaux a retirer",min_value=1, required=False)
    class Meta:
        model = Culture
        fields = ['champ']
        labels = {'champ':'nom de la parcelle'}



class Register_manyProForm(forms.ModelForm):
    quantite = forms.IntegerField(label="Entrer le nombre d'animaux a enregistrer",min_value=1, required=False)

    class Meta:
        model = Culture
        fields = ['champ','name_culture','date_plante','date_recolte']
        widgets = {
            'date_plante':forms.DateTimeInput(attrs = {'type':'datetime-local'}),
            'date_recolte':forms.DateTimeInput(attrs = {'type':'datetime-local'})
        }
        labels = {'champ':'nom de la parcelle','name_culture':'nom de la culture','date_plante':'date planté','date_recolte':'date à recolté'}



class Delete_manyProForm(forms.ModelForm):
    quantite = forms.IntegerField(label="Entrer le nombre d'animaux a retirer",min_value=1, required=False)
    class Meta:
        model = Culture
        fields = ['champ']
        labels = {'champ':'nom de la parcelle'}