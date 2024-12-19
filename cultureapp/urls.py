from django.contrib import admin
from django.urls import path
from cultureapp.views import *
from django.conf.urls import handler403

handler403 = "cultureapp.views.pagenotfound"


urlpatterns = [
    path("produit_entre/<int:id>/", produit_entre, name="produit_entre"),
    path("production/", production, name="production"),
    path("produit_vente/<int:id>/", produit_vente, name="produit_vente"),
    path("culture/",culture, name="culture"),
    path("champ/", champ, name="champ"),
    path("list_planning/", list_planning, name="list_planning"),
    path("arroser/<int:id>/", arroser, name="arroser"),
    path("delete_arrose/<int:id>/", delete_arrose, name="delete_arrose"),
    path("edite_arrose/<int:id>/",edite_arrose, name="edite_arrose"),
    path('done/<int:culture_id>/',done, name='done'),
    path("culture_list/",culture_list, name="culture_list"),
    path("show_all_culture/", show_all_culture, name="show_all_culture"),
    path("show_culture_detail/<int:id>/",show_culture_detail, name="show_culture_detail"),
    path("list/",liste_all , name="lists"),
    path("lists/", liste_produit, name="list"),
    path("edite_culture/<int:id>/", edite_culture, name="edite_culture"),
    path("stat_production/",stat_production, name="stat_production"),
    path("editer/<int:id>/",editer_parcelle, name="editer"),

    path("show_production/",show_production, name="show_production"),
    path("pdf_production/", pdf_production_create, name="pdf_production"),
    path("delete_parcelle/<int:id>/",delete_parcelle, name="delete_parcelle"),
    path("many_register/",many_register, name="many_register"),
    path("many_delete/",many_delete, name="many_delete"),
]
