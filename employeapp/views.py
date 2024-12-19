from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib.auth.models import Group,Permission,User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import logout as auth_logout ,login as auth_login,authenticate
from django.contrib.auth.decorators import login_required,permission_required



# class CustomLoginView(LoginView):
#     template_name = "login.html"
#     success_url = reverse_lazy("profile")


def connecter(request):
    if request.method=='POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        user = authenticate(request,username=username,password=password)
        if user is not None  and user.is_active:
            auth_login(request,user)
            messages.success(request,'connection reussie')
            return redirect("index")
        else:
            messages.error(request ,'Nom utilisateur ou Mot de passe incorrect')
        return render(request,'login.html')
    return render (request , 'login.html')


# def profile(request):
#     return redirect("index")
@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def manage_permissions(request):
    groups = Group.objects.all()
    permissions = Permission.objects.all()
    
    if request.method == 'POST':
        form = EmployeCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            group = Group.objects.get(id=request.POST.get('roles'))
            permissions = request.POST.getlist('permissions')
            for permission_id in permissions:
                permission = Permission.objects.get(id=permission_id)
                user.user_permissions.add(permission)
            user.groups.add(group)
            user.save()
            messages.success(request,'Enregistrement reussit')
            return redirect('list_group')
    else:
        form = EmployeCreationForm()

    return render(request, 'employe/employee_form.html', {
        'form': form,
        'groups': groups,
        'permissions': permissions,
    })
@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def list_user(request):
    users = User.objects.filter(groups__isnull=False).distinct()
    print(users)
    return render(request,'employe/list_form.html' ,{'users':users})



# def role(request):
#     print('blablablabla')
#     groups = Group.objects.all()
#     permissions = Permission.objects.all()
#     users = User.objects.all()

#     if request.method == 'POST':
#         user_id = request.POST.get('user')
#         role_id = request.POST.get('roles')
#         permission_ids = request.POST.getlist('permissions')

#         user = User.objects.get(id=user_id)
#         group = Group.objects.get(id=role_id)
#         user.groups.add(group)
#         for permission_id in permission_ids:
#             permission = Permission.objects.get(id=permission_id)
#             user.user_permissions.add(permission)
#         user.save()

#         return HttpResponse('Le rôle et les permissions ont été assignés avec succès à l\'utilisateur.')

#     return render(request, 'employe/role_modif.html', {
#         'groups': groups,
#         'permissions': permissions,
#         'users': users,
#     })


@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def edite_manage_permission_retire(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    
    group_permissions = group.permissions.all()
    if request.method == 'POST':
        permissions = request.POST.getlist('permissions')
        group.permissions.clear()  
        for permission_id in permissions:
            permission = Permission.objects.get(id=permission_id)
            group.permissions.add(permission)
        group.save()
        
        return redirect('edite_manage_permission',group_id=group_id) 
    else:
        all_permissions = Permission.objects.all()

    return render(request, 'employe/edite_manage_permission_retire.html', {
        'group': group,
        'group_permissions': group_permissions,
        'all_permissions': all_permissions,
    })


@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def list_detail(request,group_id):
    group= Group.objects.get(id=group_id)
    permission = group.permissions.all()
    return render(request , 'employe/detail.html',{
        'group':group,
        'permissions':permission,
    })
  
@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def delete_group(request,group_id):
    groupe = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        groupe.delete()
        message.success('Groupe supprimer avec success')
        return redirect('list_group')
    return render(request,'employe/supprimer_group.html',{'groupe':groupe})
    
@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def create_group(request):
    permissions = Permission.objects.all()
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        selected_permissions = request.POST.getlist('permissions')
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_id in selected_permissions:
                permission = Permission.objects.get(id=perm_id)
                group.permissions.add(permission)
            messages.success(request, f"Le groupe '{group_name}' a été créé avec succès.")
            return redirect('list_group')  
        else:
            messages.error(request, "Le nom du groupe est requis.")
    return render(request, 'employe/create_group.html', {'permissions': permissions})
    
@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def edite_manage_permission(request,group_id):
    permissions = Permission.objects.all()
    group_name = Group.objects.get(id=group_id)
    if request.method == 'POST':
        selected_permissions = request.POST.getlist('permissions')
        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_id in selected_permissions:
                permission = Permission.objects.get(id=perm_id)
                group.permissions.add(permission)
            messages.success(request, f"Le groupe '{group_name}' a été créé avec succès.")
            return redirect('list_group')  
        else:
            messages.error(request, "Le nom du groupe est requis.")
            
    return render(request, 'employe/edite_manage_permission.html', {'permissions': permissions,'group':group_name})

    












@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def list_group(request):
    groups = Group.objects.all()
    return render(request, 'employe/list_groups.html', {'groups': groups})

@login_required(login_url='login')
def logOut(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    return render(request,'index.html')



@login_required( login_url = 'login')
def edite_user(request,employe_id):
    use = get_object_or_404(Employe,id=employe_id)
    if request.method == 'POST':
        print(request.FILES)
        print(request.POST.get('image'))
        form = Edite_EmployeForm(request.POST,request.FILES,instance=use)
        if form.is_valid():
            form.save()
            messages.success(request,"Modification a été fait avec succès")
            return redirect('afficher')
    form = Edite_EmployeForm(instance=use)
    return render(request,'employe/edite_user.html',{'form':form})

@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def delete_user(request,employe_id):
    use = get_object_or_404(Employe,id=employe_id)
    use.delete()
    return redirect('afficher')

@login_required(login_url='login')
@permission_required('user.is_superuser',raise_exception=True)
def afficher(request):
    als = Employe.objects.all()
    return render (request,'employe/als.html',{'als':als})


# Create your views here.
