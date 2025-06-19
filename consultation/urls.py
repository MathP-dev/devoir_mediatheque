from django.urls import path
from . import views

urlpatterns = [
    path('medias/', views.liste_medias_consultation, name='liste_medias_consultation'),
]
