from django.urls import path
from . import views
from django.conf.urls import handler403
from animaleapp.views import custom_403_view

handler403 = custom_403_view


urlpatterns = [
    path('animal_solo/', views.animal_solo, name='animal_solo'),
    path('animal/<slug:slug>/', views.animal, name='animal'),
    path("delete_animal/<int:id>/", views.delete_animal, name="delete_animal"),

    path("delete_animal_vente/<int:id>",views.delete_animal_vente , name="delete_animal_vente"),
    path("alles/",views.alles, name="alles"),
    path("edite_aliment/",views.edite_aliment, name="edite_aliment"),
    path("aliment/",views.lister_aliments, name="aliment"),
    path('cree/', views.cree_aliment, name='cree_aliment'),
    path('edite/<int:aliment_id>/', views.edite_aliment, name='edite_aliment'),
    path('supprime<int:aliment_id>/', views.supprimer_aliment, name='supprime_aliment'),
    path("historique/", views.afficher_historique, name="historique"),



    path("planning_vente/",views.planning_vente, name="planning_vente"),
    path("planning_achat/",views.planning_achat, name="planning_achat"),
    path("planning_deces/",views.planning_deces, name="planning_deces"),
    path("planning_naissance/",views.planning_naissance, name="planning_naissance"),


   

    path("editer_animal/<int:id>/", views.editer_animal, name="editer_animal"),
    path("show_detail_animal/<int:id>/", views.show_detail_animal, name="show_detail_animal"),
    path("ajoute_all/", views.ajoute_all, name="show_all"),
    path('show_all_page/',views.show_all_page,name="show"),
    path("race/", views.race, name="race"),
    path("show_all_page/", views.show_all_page, name="show_all_page"),
    path("show_all_detail/<int:id>/", views.show_all_detail, name="show_all_detail"),
   
    path("delete_all/<int:id>/", views.delete_all, name="delete_all"),
    path("editer_all/<slug:slug>/", views.editer_all, name="editer_all"),
    path("nourrir/<int:id>/",views.nourrir, name="nourrir"),

    path("type_planning/",views.type_planning, name="type_planning"),
    path("animal_planning//",views.animal_planning, name="animal_planning"),
    path('animals/delete_bcp_animals/', views.delete_bcp_animals, name='delete_bcp_animals'),

    path("stats_animal/",views.stats_animal, name="stats_animal"),

    path("list_planning_sante/",views.list_planning_sante, name="list_planning_sante"),
    path("list_planning_nourrir/",views.list_planning_nourrir, name="list_planning_nourrir"),

    path("done_matin/<int:id>/", views.done_matin, name="done_matin"),
    path("done_midi/<int:id>/", views.done_midi, name="done_midi"),
    path("done_soir/<int:id>/", views.done_soir, name="done_soir"),

    path("custom_403_view/",custom_403_view, name="custom_403_view"),

    path("editer_type_planning/<int:id>/",views.editer_type_planning, name="editer_type_planning"),
    path("editer_animal_planning/<int:id>/",views.editer_animal_planning, name="editer_animal_planning"),
    path("delete_animal_planning/<int:id>/",views.delete_animal_planning, name="delete_animal_planning"),
    path("delete_type_planning/<int:id>/",views.delete_type_planning, name="delete_type_planning"),


    path("pdf_alles/",views.pdf_alles_create, name="pdf_alles"),
    path("pdf_code/<int:id>/",views.pdf_code, name="pdf_code"),
    path("show_alles/",views.show_alles, name="show_alles"),

    path("pdf_historique/", views.pdf_historique_create, name="pdf_historique"),
    path("show_historique/",views.show_historique, name="show_historique"),


    path("many_register_animal/",views.many_register, name="many_register_animal"),
    path("many_delete_animal/",views.many_delete, name="many_delete_animal"),





    path("update/<int:id>",views.update_nombre_type_animal, name="update"),
]
