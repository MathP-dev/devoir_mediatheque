from django.shortcuts import render
from gestion_bibliotheque.models import Livre, DVD, CD, JeuDePlateau

def liste_medias_consultation(request):
    livres = Livre.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    jeux = JeuDePlateau.objects.all()
    return render(request, 'liste_medias.html', {
        'livres': livres,
        'dvds': dvds,
        'cds': cds,
        'jeux': jeux
    })

def home(request):
    return render(request, 'home.html')