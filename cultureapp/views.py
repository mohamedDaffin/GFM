from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.template.loader import get_template
from xhtml2pdf import pisa
@login_required( login_url = 'login')
@permission_required('cultureapp.add_culture',raise_exception=True)  
def culture(request):
    form = CultureForm()
    if request.method == 'POST':
        p=request.POST.get('name_culture')
        try:
            pa = get_object_or_404(Culture,name_culture=p)
            messages.error(request,'cette culture exist apporter modification')
            return redirect('edite_culture',id=pa.id)
        except Http404:
        
            form =CultureForm(request.POST)
            if form.is_valid():
                culture = form.save()
                return redirect('arroser',id=culture.id)
    return render(request,'culture/culture.html',{'form':form})

@login_required(login_url='login')
@permission_required('cultureapp.change_culture',raise_exception=True)
def edite_culture(request,id):
    culture = get_object_or_404(Culture,id=id)
    form = EditeCultureForm(instance=culture)
    if request.method == 'POST':
        form = EditeCultureForm(request.POST,instance=culture)
        if form.is_valid():
            form.save()
            messages.success(request,'modification reussit')
            return redirect('show_all_culture')
        else:
            print(form.errors)
    return render(request,'culture/edite_culture.html',{'form':form})




@login_required(login_url='login')
@permission_required('cultureapp.add_culture',raise_exception=True)
def champ(request):
    form = ChampForm()
    if request.method == 'POST':
        form = ChampForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_all_culture')
    return render(request,'culture/champ.html',{'form':form})

@login_required(login_url='login')
@permission_required('cultureapp.add_arroser',raise_exception=True)
def arroser(request,id):
    culture_instance = get_object_or_404(Culture,id=id)
    form = ArroserForm(initial ={
        'culture':culture_instance
    })
    if request.method == 'POST':
        form = ArroserForm(request.POST)
        if form.is_valid():
            arrose = form.save(commit=False)
            arrose.culture = culture_instance
            arrose.save()
            messages.success(request,'enregistrement reussit , passé planning arrosage')
            return redirect('list_planning')
    return render(request,'culture/arroser.html',{
        'form':form,
        'culture':culture_instance
        })
@login_required(login_url='login')
@permission_required('cultureapp.change_arroser',raise_exception=True)
def edite_arrose(request,id):
    arrose_instance = get_object_or_404(Arroser,id=id)
    form = EditeArroseForm(instance=arrose_instance)
    if request.method == 'POST':
        form = EditeArroseForm(request.POST,instance=arrose_instance)
        if form.is_valid():
            form.save()
            messages.success(request,'modification reussit')
            return redirect('list_planning')
    
    return render(request,'culture/edite_arroser.html',{'form':form})
@login_required(login_url='login')
@permission_required('cultureapp.delete_arroser',raise_exception=True)
def delete_arrose(request,id):
    arrose_instance = get_object_or_404(Arroser,id=id)
    if request.method == 'POST':
        arrose_instance.delete()
        messages.success(request,"suppression reussit")
        return redirect('list_planning')
    return render(request,'culture/delete_arrose.html',{'arrose':arrose_instance})

@login_required(login_url='login')
@permission_required('ciltureapp.view_arroser',raise_exception=True)
def list_planning(request):
    arroses = Arroser.objects.all()
    return render(request,'culture/list_planning.html',{'arroses':arroses})


def done(request, id):
    culture = get_object_or_404(Culture, id=id)
    culture.is_do = True
    culture.save()
    return HttpResponse('Travail effectuer')
   
def culture_list(request):
    cultures = Culture.objects.all()
    return render(request,'culture/culture_list.html',{'form':cultures})

@login_required(login_url='login')
@permission_required('cultureapp.add_production',raise_exception=True)
def production(request):
    form = ProductionForm()
    if request.method == 'POST':
        form = ProductionForm(request.POST)
        culture = request.POST.get('culture')
        try:
            culture = get_object_or_404(Production,culture=culture)
            messages.error(request,'le produit existe Entrer la quantite a enregistrer !!!')
            return redirect('produit_entre',id=culture.id)
        except Http404:
            if form.is_valid():
                form.save()
                messages.success(request,'enregistrement reussit')
                return redirect('list')
    return render(request,'production/production.html',{
            'form':form,
            })

@login_required(login_url='login')
@permission_required('cultureapp.delete_production',raise_exception=True)
def produit_vente(request,id):
    product = get_object_or_404(Production,id=id)
    form = ProductionventeForm(instance= product)
    if request.method == 'POST':
        quantite = request.POST.get('quantite_produit')
        if int(quantite) < int(product.quantite_produit):
            form = ProductionventeForm(request.POST)
            if form.is_valid():
                product.quantite_produit = int(product.quantite_produit) - int(quantite)
                Historique.objects.create(culture=product.culture,date_sorti = datetime.now ,quantite_sorti = int(quantite) ,tolal = product.quantite_produit)
                product.save() 
                messages.success(request ,'produit vendu avec succes')
                return redirect('list')
            else:
                print(form.errors)
        else:
            messages.success(request ,'stock de production faible')
            return redirect('list')

    form = ProductionventeForm(instance= product)
    return render(request,'production/vente.html',{'form':form})
    
@login_required(login_url='login')
@permission_required('cultureapp.change_production',raise_exception=True)
def produit_entre(request,id):
    product = get_object_or_404(Production,id=id)
    if request.method == 'POST':
        quantite = request.POST.get('quantite_produit')
        product.entre = True
        product.quantite_produit = product.quantite_produit + int(quantite)
        Historique.objects.create(culture=product.culture,date_sorti = datetime.now ,quantite_entre = int(quantite) ,tolal = product.quantite_produit)
        product.save()
        messages.success(request,'Produit enregistrer avec success')
        return redirect('list')
    else:
        form = ProductionventeForm(instance= product)
    return render(request,'production/entre.html',{'form':form})

@login_required(login_url='login')
@permission_required('cultureapp.view_production',raise_exception=True)
def liste_all(request):
    lists = Historique.objects.all().order_by('-date_entre')
    return render(request,'production/historique.html',{'items':lists})

@login_required(login_url='login')
@permission_required('cultureapp.view_production',raise_exception=True)
def liste_produit(request):
    productions = Production.objects.all()
    return render(request, 'production/lists.html', {
        'productions': productions,
    })
  
@login_required(login_url='login')
@permission_required('cultureapp.view_culture',raise_exception=True)
def show_all_culture(request):
    typee =Champ.objects.all()
    return render(request,'culture/show_all_culture.html',{'type':typee})

@login_required(login_url='login')
@permission_required('cultureapp.view_culture',raise_exception=True)
def show_culture_detail(request,id):
    detail = Culture.objects.filter(champ_id = id)
    return render(request,'culture/show_culture.html',{'detail':detail})

def pagenotfound(request , exception):
    return render(request,'pages-error-404.html',status=403)



def stat_production(request):
    productions = Production.objects.all()
    return render(request, 'production/stat_production.html', {
        'productions': productions,
    })



def show_production(request):
    productions = Production.objects.all()
    return render(request,'Animal/show_production.html',{'items':lists})
 
def pdf_production_create(request):
    lists = Historique.objects.all().order_by('-date_entre')
    template_path = 'PDF/historique.html'
    context = {'items': lists}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="raport_production.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
       html,
       dest=response,
    )
    if pisa_status.err:
       return HttpResponse('Comment <pre>' + html + '</pre>')

    return response


@login_required( login_url = 'login')
@permission_required('cultureapp.add_culture',raise_exception=True)  
def many_register(request):
    if request.method == 'POST':
        form = Register_manyForm(request.POST)
        if form.is_valid():
            quantite = form.cleaned_data['quantite']
            name = form.cleaned_data['name_culture']
            date_plante = form.cleaned_data['date_plante']
            date_recolte = form.cleaned_data['date_recolte']
            champ = form.cleaned_data['champ']
            cultures = [Culture(name_culture=f"{name} {i+1}",date_plante=date_plante,date_recolte=date_recolte) for i in range(quantite)]
            for culture in cultures:
                culture.champ = champ
                culture.save()
            messages.success(request,'Enregistrement reussit')
            return redirect('lists')
    else:
        form = Register_manyForm()
    return render(request,'culture/register_many.html',{'form':form})

@login_required( login_url = 'login')
@permission_required('cultureapp.delete_culture',raise_exception=True)  
def many_delete(request):
    i=0
    if request.method == 'POST':
        form = Delete_manyForm(request.POST)
        if form.is_valid():
            comptes = form.cleaned_data['quantite']
            champ = form.cleaned_data['champ']
            cultures = Culture.objects.filter(champ=champ)
            compte = cultures.count()
            if compte > comptes:
                for culture in cultures:
                    if i < comptes:
                        culture.delete()
                        i = i + 1
                return redirect('lists')
            else:
                form = Delete_manyForm()
            return render(request,'culture/delete_many.html',{'form':form})
    else:
        form = Delete_manyForm()
    return render(request,'culture/delete_many.html',{'form':form})

def editer_parcelle(request,id):
    obj = Champ.objects.get(id=id)
    print(obj)
    if request.method =='POST':
        form = EditeForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,'Modification reussit')
            return redirect('show_all_culture')
    form_all = EditeForm(instance=obj)
    return render(request,'culture/edite.html',{'form_all':form_all})

def delete_parcelle(request,id):
    detail = Culture.objects.filter(champ_id=id)
    if detail.count()!=0:
        messages.error(request,'le champ n\'est pas vide')
        return redirect('show_culture_detail',id=id)
    else:
        delet = Champ.objects.filter(id=id)
        delet.delete()
    messages.success(request,'Suppression reussit')
    return redirect('show_all_culture')

# Create your views here.