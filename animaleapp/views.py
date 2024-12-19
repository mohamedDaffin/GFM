from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from .forms import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,Http404
from .models import *
from django.contrib import messages
from django.db.models import Count
from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from xhtml2pdf import pisa
import random
from django.contrib.auth.models import User
from django.template.loader import render_to_string
@login_required(login_url='login')
@permission_required('animaleapp.add_animal',raise_exception=True)
def race(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_all_page')
    else:
        form = ClasseForm()
    return render(request,'Animal/race.html',{'form':form})



@login_required( login_url = 'login')
@permission_required('animaleapp.add_aliment',raise_exception=True)
def cree_aliment(request):
    if request.method == 'POST':
        name = request.POST.get('name_aliment')
        try:
            nm = get_object_or_404(Aliment,name_aliment=name)
            messages.success(request,'un aliment avec se nom existe entrez la  quabtite a ajouter')
            return redirect('edite_aliment',aliment_id =nm.id)
        except Http404:

            form = AlimentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "L'aliment a été créé avec succès.")
                return redirect('aliment')
            else:
                messages.error(request, "Erreur lors de la création de l'aliment.")
    else:
        form = AlimentForm()

    return render(request, 'Aliment/cree_aliment.html', {'form': form})
@login_required(login_url='login')
@permission_required('animaleapp.change_aliment',raise_exception=True)
def edite_aliment(request, aliment_id):
    aliment = get_object_or_404(Aliment, id=aliment_id)
    if request.method == 'POST':
        i = request.POST.get("quantite")
        aliment.quantite= aliment.quantite + int(i)
        aliment.save()
        Histoire.objects.create(aliment=aliment, entre=aliment.quantite, difference=int(i))
        messages.success(request, "L'aliment a été mis à jour avec succès.")
        return redirect('aliment')
    else:
        form = EditeAlimentForm(instance=aliment)

    return render(request, 'Aliment/edite_aliment.html', {'form': form, 'aliment': aliment})
@login_required(login_url='login')
@permission_required('animaleapp.delete_aliment',raise_exception=True)
def supprimer_aliment(request, aliment_id):
    aliment = get_object_or_404(Aliment, id=aliment_id)
    aliment.delete()
    messages.success(request, "L'aliment a été supprimé avec succès.")
    return redirect('aliment')

@login_required(login_url='login')
@permission_required('animaleapp.view_aliment',raise_exception=True)
def lister_aliments(request):
    aliments = Aliment.objects.all()  
    return render(request, 'Aliment/aliment.html', {'aliments': aliments})

@login_required(login_url='login')
@permission_required('animaleapp.view_historique',raise_exception=True)
def afficher_historique(request):
    historique = Histoire.objects.all().order_by('-date')
    return render(request, 'Aliment/historique.html', {'historique': historique})

@login_required( login_url = 'login')
@permission_required('animaleapp.add_animal',raise_exception=True)   
def animal(request,slug):
    typee = TypeAnimal.objects.get(slug=slug)
    form = AnimalForm()

    if request.method == 'POST':
        name = request.POST.get('name_animal')
        if typee.id == int(request.POST.get('typee')):

            try:
                nm = get_object_or_404(Animal,name_animal=name)
                messages.error(request,'un animal avec ce nom existe')
                return redirect('animal',slug=slug)
            except Http404:
                n = Animal.objects.all()
                form = AnimalForm(request.POST)
                if form.is_valid():
                    form.nombre = n.count()
                    animal = form.save(commit=False)
                    animal.user = request.user
                    animal.save()
                    form.save()
                    messages.success(request,'Animal enregistrer avec success')
                    return redirect('show_all_page')
        else:
            messages.error(request,'L\'Animal doit appartenir au même Troupeau')
            return redirect('animal',slug=slug)
    else:
        form = AnimalForm(initial = {
            'typee':typee.name_type,
        })
    return render(request,'Animal/animal.html',{'form':form})




@login_required( login_url = 'login')
@permission_required('animaleapp.add_animal',raise_exception=True)    
def animal_solo(request):
    form = AnimalForm()
    if request.method == 'POST':
        name = request.POST.get('name_animal')
        try:
            nm = get_object_or_404(Animal,name_animal=name)
            
            messages.success(request,'un animal avec ce nom existe')
            return redirect('animal_solo')
        except Http404:
            form = AnimalForm(request.POST)
            if form.is_valid():
                animal = form.save(commit=False)
                animal.user = request.user
                animal.save()
                form.save()
                messages.success(request,'enregisrement reussit')
                return redirect('show_all_page')
    else:
        form = AnimalForm()
    return render(request,'Animal/animal.html',{'form':form})



@login_required(login_url='login')
@permission_required('animalapp.view_animalplanning',raise_exception=True)
def list_planning_sante(request):
    list_plannings = AnimalPlanning.objects.all()
    return render(request,'Animal/list_planning_sante.html',{'list_plannings':list_plannings})

@login_required(login_url='login')
@permission_required('animaleapp.view_planningtype',raise_exception=True)
def list_planning_nourrir(request):
    list_plannings = PlanningType.objects.all()
    return render(request,'Animal/list_planning_nourrir.html',{'list_plannings':list_plannings})







@login_required( login_url = 'login')
@permission_required('animaleapp.delete_animal',raise_exception=True)
def delete_animal(request, id):
    animal = get_object_or_404(Animal, id=id)
    if request.method == 'POST':
        historique ,created = Historique.objects.get_or_create(animal=animal,Type=animal.typee)
        historique.deces +=1
        historique.save()
        animal.delete()
        messages.success(request, "L'animal a été supprimé avec succès.")
        return redirect('show_all_page')
    return render(request, 'Animal/supprime_animal.html', {'animal': animal})


@login_required( login_url = 'login')
@permission_required('animaleapp.delete_animal',raise_exception=True) 
def delete_animal_vente(request, id):
    animal = get_object_or_404(Animal, id=id)
    if request.method == 'POST':
        historique ,created = Historique.objects.get_or_create(animal=animal,Type=animal.typee)
        historique.vente +=1
        historique.save()
        animal.delete()
        messages.success(request, "Animal vendu avec succès.")
        return redirect('show_all_page')
    return render(request, 'Animal/vendre_animal.html', {'animal': animal})

@login_required( login_url = 'login')
@permission_required('animaleapp.change_animal',raise_exception=True) 
def editer_animal(request,id):
    tache = Animal.objects.get(id=id)
    if request.method == 'POST':
        form = edite_animalForm(request.POST,instance = tache)
        if form.is_valid():
            form.save()
            return redirect('show_animal')
    else:
        form = edite_animalForm(instance = tache)
    return render(request,'Animal/editer.html',{'form':form})

@login_required( login_url = 'login')
@permission_required('animaleapp.add_animalplanning',raise_exception=True)
def animal_planning(request):
    form = AnimalPlanningForm()
    if request.method == 'POST':
        motif = request.POST.get('motif')
        date = request.POST.get('date_fin')
        user = request.POST.get('user')
        animal_ids = request.POST.getlist('animal')
        list_animal = Animal.objects.filter(id__in=animal_ids)
        for animal in list_animal:
            if not AnimalPlanning.objects.filter(animal=animal).exists():
                nw_planning = AnimalPlanning.objects.create(
                    motif=motif,
                    date_fin=date,
                    user=get_object_or_404(User , id=user)
                )
                nw_planning.animal.set([animal])
        messages.success(request,'enregistrement reussit')
        return redirect('list_planning_sante')
    return render(request,'planning/animal_planning.html',{'form':form})

@login_required(login_url='login')
@permission_required('animaleapp.view_animal',raise_exception=True)
def show_detail_animal(request,id):
    animal = Animal.objects.get(id=id)
    l = TypeAnimal.objects.get(name_type=animal.typee)
    return render(request,'Animal/show_detail.html',{'animal':animal,
    'items':l.aliment.all()
    })
@login_required(login_url='login')
@permission_required('animaleapp.add_typeanimal',raise_exception=True)
def ajoute_all(request):
    form = TypeAnimalForm()
    if request.method == 'POST':
        name = request.POST.get('name_type')
        try:
            nm = get_object_or_404(TypeAnimal,name_type = name)
            messages.error(request,'Ce Troupeau existe deja')
            return redirect('ajoute_all')
        except:
            form = TypeAnimalForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Enregistrement Troupeau reussit !! enregistrer le planning')
                return redirect('type_planning')
    return render(request,'Animal/ajoute_all.html',{'form':form})
@login_required(login_url='login')
@permission_required('animaleapp.change_typeanimal',raise_exception=True)
def editer_all(request,slug):
    obj = TypeAnimal.objects.get(slug=slug)
    if request.method =='POST':
        form = EditeAllForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Modification reussit')
            return redirect('show_all_page')
    form_all = EditeAllForm(instance=obj)
    return render(request,'Animal/editer_all.html',{'form_all':form_all})

@login_required(login_url='login')
@permission_required('animaleapp.view_typeanimal',raise_exception=True)
def show_all_page(request):
    typee =TypeAnimal.objects.annotate(animal_count=Count("animal"))
    return render(request,'Animal/show_all_page.html',{'type':typee})

@login_required(login_url='login')
@permission_required('animaleapp.view_typeanimal',raise_exception=True)
def show_all_detail(request,id):
    detail = Animal.objects.filter(typee_id=id)
    items = TypeAnimal.objects.filter(id=id)
    return render(request,'Animal/show_animal.html',{
        'detail':detail,
        'items':items
        })

@login_required(login_url='login')
@permission_required('animaleapp.delete_typeanimal',raise_exception=True)
def delete_all(request,id):
    detail = Animal.objects.filter(typee_id=id)
    if detail.count()!=0:
        messages.success(request,'le troupeau contient des animaux')
        return redirect('show_all_detail',id=id)
    else:
        delet = TypeAnimal.objects.filter(id=id)
        delet.delete()
    messages.success(request,'Suppression reussit')
    return redirect('show_all_page')

@login_required(login_url='login')
@permission_required('animale.add_planningtype',raise_exception=True)
def type_planning(request):
    form = PlanningTypeForm()
    if request.method == 'POST':
        matin = request.POST.get('matin')
        midi = request.POST.get('midi')
        soir = request.POST.get('soir')
        user = request.POST.get('user')
        if not matin:
            matin = False
        else:
            matin = True
        if not midi:
            midi = False
        else:
            midi = True
        if not soir:
            soir = False
        else:
            soir = True
        type_ids = request.POST.getlist('typee')
        list_type = TypeAnimal.objects.filter(id__in = type_ids)
        for type_animal in list_type:
            if not PlanningType.objects.filter(typee=type_animal).exists():
                nw_planning = PlanningType.objects.create(
                    matin=matin,
                    midi = midi,
                    soir = soir,
                    user = get_object_or_404(User,id=user),
                )
                nw_planning.typee.set([type_animal])
                messages.success(request,'Enregistrement planning reussit')
                return redirect('list_planning_nourrir')
    return render(request,'planning/planning.html',{'form':form})

@login_required( login_url = 'login')
@permission_required('animaleapp.add_nourriture',raise_exception=True)
def nourrir(request,id):
    Type = TypeAnimal.objects.get(id=id)
    ali = Type.aliment.all()
    if request.method == 'POST':
        form = NourritureForm(request.POST)
        quantite = request.POST.get('quantite')
        aliment_id = request.POST.get('aliment')
        aliment = Aliment.objects.get(id=aliment_id)
        if form.is_valid():
            safe = form.save(commit=False)
            if aliment.quantite < int(quantite):
                send_mail(
                        'Rappel sur le stock',
                        f'Stock de { aliment } faible',
                        'mohamedyakeri@gmail.com',
                        [request.user.email],
                        fail_silently=False,
                        )    
                return redirect('aliment')
            else:
                aliment.quantite -= int(quantite)
                aliment.save()
                
                n = form.save(commit=False)
                n.user = request.user
                n.aliment=aliment
                n.save()
                Histoire.objects.create(aliment=aliment, entre=aliment.quantite, sortie=int(quantite))
                messages.success(request, "L'aliment a été mis à jour avec succès.")
                return redirect('show_all_page')
    form = NourritureForm(initial={'Type':Type,
    'aliment':ali
    })                 
    return render(request,'Animal/nourrir.html',{'form':form,
    'aliments':ali
    })

@login_required(login_url='login')
@permission_required('animaleapp.view_historique',raise_exception=True)
def alles(request):
    form = Historique.objects.all()
    deces_t = 0
    naissance_t = 0
    vente_t = 0
    achat_t = 0
    entre_t = 0
    sortie_t = 0
    table= {}
    for f in form: 
        # Si le type d'animal n'est pas déjà dans le dictionnaire, l'ajouter
        if f.Type not in table:
            table[f.Type] = {
                'deces': 0,
                'vente': 0,
                'achat': 0,
                'naissance': 0,
                'entre_ali':0,
                'sortie_ali':0,
            }
        
        #  Permet d'ajouter les données à la somme correspondante
        table[f.Type]['deces'] += f.deces
        table[f.Type]['vente'] += f.vente
        table[f.Type]['achat'] += f.achat
        table[f.Type]['naissance'] += f.naissance
        deces_t += f.deces
        vente_t += f.vente
        achat_t += f.achat
        naissance_t  += f.naissance
    return render(request, 'Animal/alles.html', {
        'table': table,
        'total_deces':deces_t,
        'total_vente':vente_t,
        'total_naissance':naissance_t,
        'total_achat':achat_t,
    })
    
def custom_403_view(request,exception):
    return render(request,'pages-error-404.html',status=403)

def done_matin(request,id):
    planning = get_object_or_404(PlanningType,id=id)
    planning.do_matin = True
    planning.save()
    return redirect('index')

def done_midi(request,id):
    planning = get_object_or_404(PlanningType,id=id)
    planning.do_midi = True
    planning.save()
    return redirect('index')

def done_soir(request,id):
    planning = get_object_or_404(PlanningType,id=id)
    planning.do_soir = True
    planning.save()
    return redirect('index')
    
@login_required(login_url='login')
@permission_required('aniamleapp.delete_animal',raise_exception=True)
def delete_bcp_animals(request):
    if request.method == 'POST':
        selects  = request.POST.getlist('selected_animals')
        for select in selects:
            if select:
                animal =get_object_or_404(Animal,id=select)
                historique ,created = Historique.objects.get_or_create(animal=animal,Type=animal.typee)
                historique.vente +=1
                historique.save()
                animal.delete()
            else:
                messages.warning(request, "Aucun animal sélectionné.")
        messages.success(request, f"{len(selects)} animaux ont été vendus avec succès.")
        
    return redirect('show_all_page')

def stats_animal(request):
    form = Historique.objects.all()
    table= {}
    for f in form: 
        # Si le type d'animal n'est pas déjà dans le dictionnaire, l'ajouter
        if f.Type not in table:
            table[f.Type] = {
                'deces': 0,
                'vente': 0,
                'achat': 0,
                'naissance': 0,
                'entre_ali':0,
                'sortie_ali':0,
            }
        
        #Permet d'ajouter les données à la somme correspondante
        table[f.Type]['deces'] += f.deces
        table[f.Type]['vente'] += f.vente
        table[f.Type]['achat'] += f.achat
        table[f.Type]['naissance'] += f.naissance
        
    return render(request, 'Animal/stats_animal.html', {
        'table': table,
        
    })



def planning_vente(request):
    form = Historique.objects.all()
    return render(request,'Animal/planning_vente.html',{'form':form})
def planning_achat(request):
    form = Historique.objects.all()
    return render(request,'Animal/planning_achat.html',{'form':form})
def planning_deces(request):
    form = Historique.objects.all()
    return render(request,'Animal/planning_deces.html',{'form':form})
def planning_naissance(request):
    form = Historique.objects.all()
    return render(request,'Animal/planning_naissance.html',{'form':form})



def show_historique(request):
    histoire = Histoire.objects.all()
    return render(request,'Animal/show_historique.html',{'historique':historique})


def pdf_historique_create(request):
    historique = Histoire.objects.all()
    template_path = 'PDF/historique_aliment.html'
    context = {'historique': historique}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="raport_historique.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html,
       dest=response,
    )

    if pisa_status.err:
       return HttpResponse('Comment <pre>' + html + '</pre>')

    return response

def pdf_code(request,id):
    code = Animal.objects.get(id=id)
    code = code.code
    template_path ='PDF/code.html'
    context = {'code':code}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename = "code.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
    )
    if pisa_status.err:
        return HttpResponse('Comment <pre>' + html + '</pre>')

    return response



def show_alles(request):
    historique = Historique.objects.all()
    return render(request,'Animal/show_alles.html',{'form':form})

def pdf_alles_create(request):
    form = Historique.objects.all()
    deces_t = 0
    naissance_t = 0
    vente_t = 0
    achat_t = 0
    entre_t = 0
    sortie_t = 0
    table= {}
    for f in form: 
        # Si le type d'animal n'est pas déjà dans le dictionnaire, l'ajouter
        if f.Type not in table:
            table[f.Type] = {
                'deces': 0,
                'vente': 0,
                'achat': 0,
                'naissance': 0,
               
            }
        
        #  Permet d'ajouter les données à la somme correspondante
        table[f.Type]['deces'] += f.deces
        table[f.Type]['vente'] += f.vente
        table[f.Type]['achat'] += f.achat
        table[f.Type]['naissance'] += f.naissance
        deces_t += f.deces
        vente_t += f.vente
        achat_t += f.achat
        naissance_t  += f.naissance
    template_path = 'PDF/alles.html'
    context = {
        'table': table,
        'total_deces':deces_t,
        'total_vente':vente_t,
        'total_naissance':naissance_t,
        'total_achat':achat_t,
        }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="raport_animal.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html,
       dest=response,
       
    )
    if pisa_status.err:
       return HttpResponse('Comment <pre>' + html + '</pre>')

    return response

@login_required(login_url='login')
@permission_required('animaleapp.add_animal',raise_exception=True)
def many_register(request):
    if request.method == 'POST':
        form = Register_manyForm(request.POST)
        if form.is_valid():
            quantite = form.cleaned_data['quantite']
            name = form.cleaned_data['name_animal']
            typee = form.cleaned_data['typee']
            naissance = form.cleaned_data['naissance']
            animals = [Animal(name_animal=f"{name} {i+1}",poids=random.randint(50,200)) for i in range(quantite)]
            if naissance:
                for animal in animals:
                    animal.user = request.user
                    animal.typee = typee
                    animal.naissance = True
                    animal.save()
            else:
                for animal in animals:
                    animal.user = request.user
                    animal.typee = typee
                    animal.save()
            messages.success(request, "Enregistrement effectuer avec succès.")
            return redirect('show_all_page')
    else:
        form = Register_manyForm()
    return render(request,'Animal/register_many.html',{'form':form})

@login_required(login_url='login')
@permission_required('animaleapp.delete_animal',raise_exception=True)
def many_delete(request):
    i=0
    if request.method == 'POST':
        form = Delete_manyForm(request.POST)
        if form.is_valid():
            comptes = form.cleaned_data['quantite']
            typee = form.cleaned_data['typee']
            choix = form.cleaned_data['vente']
            animals = Animal.objects.filter(typee=typee)
            compte = animals.count()
            if choix:
                if compte > comptes:
                    for animal in animals:
                        if i < comptes:
                            historique ,created = Historique.objects.get_or_create(animal=animal,Type=animal.typee)
                            historique.vente +=1
                            historique.save()
                            animal.delete()
                            i = i + 1
                    messages.error(request, "Supression reussit")
                    return redirect('show_all_page')
                else:
                    messages.error(request, "Pas assez d'animaux")
                    form = Delete_manyForm()
                return render(request,'Animal/delete_many.html',{'form':form})
            else:
                if compte > comptes:
                    for animal in animals:
                        if i < comptes:
                            historique ,created = Historique.objects.get_or_create(animal=animal,Type=animal.typee)
                            historique.deces +=1
                            historique.save()
                            animal.delete()
                            i = i + 1
                    messages.error(request, "Supression reussit")
                    return redirect('show_all_page')
                else:
                    messages.error(request, "Pas assez d'animaux")
                    form = Delete_manyForm()
                return render(request,'Animal/delete_many.html',{'form':form})
    else:
        form = Delete_manyForm()
    return render(request,'Animal/delete_many.html',{'form':form})


@login_required(login_url='login')
@permission_required('animaleapp.change_planningtype',raise_exception=True)
def editer_type_planning(request,id):
    tp= get_object_or_404(PlanningType,id=id)
    form = EdierplanningForm(instance=tp)
    if request.method == 'POST':
        form = EdierplanningForm(request.POST,instance=tp)
        if form.is_valid():
            form.save()
            messages.success(request,'modification reussit')
            return redirect('list_planning_nourrir')
        
    return render(request,'planning/editer_planning.html',{'form':form})

@login_required(login_url='login')
@permission_required('animaleapp.change_animalplanning',raise_exception=True)
def editer_animal_planning(request,id):
    tp= get_object_or_404(AnimalPlanning,id=id)
    form = EditerplanningForm(instance=tp)
    if request.method == 'POST':
        form = EditerplanningForm(request.POST,instance=tp)
        if form.is_valid():
            form.save()
            messages.success(request,'modification reussit')
            return redirect('list_planning_sante')
    return render(request,'planning/edier_planning.html',{'form':form})

@login_required(login_url='login')
@permission_required('animaleapp.delete_planningtype',raise_exception=True)
def delete_type_planning(request,id):
    Tp = get_object_or_404(PlanningType,id=id)
    Tp.delete()
    return redirect('list_planning_nourrir')

@login_required(login_url='login')
@permission_required('animaleapp.delete_animalplanning',raise_exception=True)
def delete_animal_planning(request,id):
    Ap = get_object_or_404(AnimalPlanning,id=id)
    Ap.delete()
    return redirect('list_planning_sante')
# Create your views here.




@permission_required('user.is_superuser',raise_exception=True)    
def update_nombre_type_animal(request, id):
    type_animal = get_object_or_404(TypeAnimal, id=id)
    print("premier sans le post ")

    if request.method == "POST":
        try:
            nouveau_nombre = int(request.POST.get('nombre', type_animal.nombre))
            if nouveau_nombre >= 0:
                type_animal.nombre = nouveau_nombre
                type_animal.save()
                messages.success(request, "Le nombre d'animaux a été mis à jour avec succès.")
                return redirect("show_all_page")
            else:
                messages.error(request, "Le nombre doit être supérieur ou égal à 0.")
        except ValueError:
            messages.error(request, "Veuillez entrer un nombre valide.")
        return redirect('Animal/update_nombre_type_animal',id=id)

    return render(request, 'Animal/update_nombre_type_animal.html', {'type_animal': type_animal})

