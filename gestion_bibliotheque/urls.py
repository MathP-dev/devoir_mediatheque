from django.urls import path
from . import views

urlpatterns = [
    path('medias/', views.liste_medias, name='liste_medias'),
    path('membres/', views.liste_membres, name='liste_membres'),
    path('ajouter-media/', views.ajouter_media, name='ajouter_media'),
    path('ajouter-membre/', views.ajouter_membre, name='ajouter_membre'),
    path('mettre-a-jour-membre/<int:membre_id>/', views.mettre_a_jour_membre, name='mettre_a_jour_membre'),
    path('emprunter-media/<int:media_id>/', views.emprunter_media, name='emprunter_media'),
    path('retourner-emprunt/<int:emprunt_id>/', views.retourner_emprunt, name='retourner_emprunt'),
]
