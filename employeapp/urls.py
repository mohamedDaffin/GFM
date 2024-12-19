from django.urls import path 
from .views import *

urlpatterns = [
    # path("accounts/profile/", profile, name='profile'),

    path("login/",connecter, name="login"),
    # path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logOut, name="logout"),
    path("list_detail/<int:group_id>/", list_detail, name="list_detail"),
    path("delete_group/<int:group_id>/", delete_group, name="delete_group"),
    path("create_group/",create_group, name="create_group"),
    path("list_group/",list_group, name="list_group"),
    path("edite_manage_permission/<int:group_id>/", edite_manage_permission, name="edite_manage_permission"),
    path("edite_manage_permission_retire/<int:group_id>/", edite_manage_permission_retire, name="edite_manage_permission_retire"),

    path("edite_user/<int:employe_id>/",edite_user, name="edite_user"),
    path("delte_user/<int:employe_id>/",delete_user, name="delete_user"),
    path("afficher/",afficher, name="afficher"),
    path("edite_user/<int:employe_id>/",edite_user, name="edite_user"),
    path("index/",index, name="index")
]
