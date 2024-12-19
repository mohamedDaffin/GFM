from django import forms
from django.contrib.auth.models import User
from animaleapp.models import *

class AnimalPlanningForm(forms.ModelForm):
    animal = forms.ModelMultipleChoiceField(
        queryset = Animal.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    class Meta:
        model = AnimalPlanning
        fields = ['animal','user','motif','date_fin']
        widgets = {
            'date_fin':forms.DateTimeInput(attrs={'type':
            'datetime-local'})
        }
class PlanningTypeForm(forms.ModelForm):
    typee = forms.ModelMultipleChoiceField(
        queryset = TypeAnimal.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )
    class Meta:
        model = PlanningType
        fields = ['matin','midi','soir','typee','user']
        labels = {'typee':'troupeau'}

class EdierplanningForm(forms.ModelForm):
    class Meta:
        model = PlanningType
        fields = ['matin','midi','soir','typee','user']
        labels = {'typee':'troupeau'}



class EditerplanningForm(forms.ModelForm):
    class Meta:
        model = AnimalPlanning
        fields = ['animal','user','motif','date_fin']
        widgets = {
            'date_fin':forms.DateTimeInput(attrs={'type':
            'datetime-local'})
        }
class AlimentForm(forms.ModelForm):
    
    class Meta:
        model = Aliment
        fields = ['name_aliment','quantite']
        labels = {'name_aliment':'nom de l\'aliment'}


class EditeAlimentForm(forms.ModelForm):
   
    class Meta:
        model = Aliment
        fields = ['quantite']

class ClasseForm(forms.ModelForm):
    
    class Meta:
        model = Classe
        fields = ['name_classe']
        labels = {'name_classe':'nom de la classe'}

class AnimalForm(forms.ModelForm):
    
    class Meta:
        model = Animal
        fields = ['name_animal','naissance','sexe','typee','poids','description','date_enregistrer']
        labels = {'typee':'troupeau','name_animal':'nom de l\'animal','date_enregister':'date enregistrer'}


        widgets = {
            'date_enregistrer': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class NourritureForm(forms.ModelForm):
    
    class Meta:
        model = Nourriture
        fields = ['Type','aliment','quantite','date']
        labels = {'typee':'troupeau'}

        exclude = ['aliment']
        widgets ={
            'date':forms.DateTimeInput(attrs={'type':'datetime-local'}),
            'Type':forms.HiddenInput()
        }

class edite_animalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name_animal','sexe','typee','poids','description']
        labels = {'typee':'troupeau'}

class TypeAnimalForm(forms.ModelForm):
    aliment = forms.ModelMultipleChoiceField(
        queryset = Aliment.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )
    class Meta:
        model = TypeAnimal
        fields = ['name_type','classe','quantite','aliment']
        labels = {'name_type':'troupeau'}


class EditeAllForm(forms.ModelForm):
    aliment = forms.ModelMultipleChoiceField(
        queryset = Aliment.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )
    class Meta:
        model = TypeAnimal
        fields = ['name_type','classe','quantite','aliment']
        labels = {'name_type':'troupeau'}

class ClasseForm(forms.ModelForm):
    
    class Meta:
        model = Classe
        fields = ['name_classe']
        labels = {'name_classe':'nom de la classe'}




class Register_manyForm(forms.ModelForm):
    quantite = forms.IntegerField(label="Entrer le nombre d'animaux a enregistrer",min_value=1, required=False)

    class Meta:
        model = Animal
        fields = ['name_animal','naissance','typee']
        labels = {'typee':'troupeau','name_animal':'nom de l\'animal'}
        
class Delete_manyForm(forms.ModelForm):
    quantite = forms.IntegerField(label="Entrer le nombre d'animaux a vendre",min_value=1, required=False)
    class Meta:
        model = Animal
        fields = ['typee','vente']
        labels = {'typee':'troupeau'}

    
     