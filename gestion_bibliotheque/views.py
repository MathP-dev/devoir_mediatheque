from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .forms import MembreForm, MediaForm
from .models import Livre, DVD, CD, JeuDePlateau, Emprunteur, Emprunt, Media
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required()
def profile(request):
    return render(request, 'gestion_bibliotheque/profile.html')

@login_required()
def liste_medias(request):
    livres = Livre.objects.all()
    dvds = DVD.objects.all()
    cds = CD.objects.all()
    jeux = JeuDePlateau.objects.all()
    return render(request, 'gestion_bibliotheque/liste_medias.html', {'livres': livres, 'dvd': dvds, 'cd': cds, 'jeux': jeux})

@login_required()
def liste_membres(request):
    membres = Emprunteur.objects.all()
    return render(request, 'gestion_bibliotheque/liste_membres.html', {'membres': membres})

@login_required
def ajouter_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            type_media = form.cleaned_data['type_media']
            name = form.cleaned_data['name']

            if type_media == 'livre':
                auteur = form.cleaned_data['auteur']
                Livre.objects.create(name=name, auteur=auteur)
            elif type_media == 'dvd':
                realisateur = form.cleaned_data['realisateur']
                DVD.objects.create(name=name, realisateur=realisateur)
            elif type_media == 'cd':
                artiste = form.cleaned_data['artiste']
                CD.objects.create(name=name, artiste=artiste)
            elif type_media == 'jeu':
                createur = form.cleaned_data['createur']
                JeuDePlateau.objects.create(name=name, createur=createur)

            return redirect('liste_medias')
    else:
        form = MediaForm()

    return render(request, 'gestion_bibliotheque/ajouter_media.html', {'form': form})

@login_required
def ajouter_membre(request):
    if request.method == 'POST':
        form = MembreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')
    else:
        form = MembreForm()

    return render(request, 'gestion_bibliotheque/ajouter_membre.html', {'form': form})

@login_required
def mettre_a_jour_membre(request, membre_id):
    membre = get_object_or_404(Emprunteur, id=membre_id)
    if request.method == 'POST':
        form = MembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('liste_membres')
    else:
        form = MembreForm(instance=membre)
    return render(request, 'gestion_bibliotheque/mettre_a_jour_membre.html', {'form': form})

@login_required
def emprunter_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    medias_disponibles = Media.objects.filter(disponible=True)
    emprunteurs = Emprunteur.objects.all()

    if request.method == 'POST':
        emprunteur_id = request.POST.get('emprunteur')
        emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)

        if emprunteur.peut_emprunter():
            Emprunt.objects.create(media=media, emprunteur=emprunteur)
            media.disponible = False
            media.save()
            messages.success(request, "Le média a été emprunté avec succès.")
            return redirect('profile')
        else:
            messages.error(request, "L'emprunteur ne peut pas emprunter ce média.")

    return render(request, 'gestion_bibliotheque/emprunter_media.html', {
        'media': media,
        'medias_disponibles': medias_disponibles,
        'emprunteurs': emprunteurs
    })

@login_required
def retourner_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)

    if request.method == 'POST':
        emprunt.date_retour = timezone.now()
        emprunt.media.disponible = True
        emprunt.media.save()
        emprunt.save()
        messages.success(request, "L'emprunt a été retourné avec succès.")
        return redirect('profile')

    return render(request, 'gestion_bibliotheque/retourner_emprunt.html', {'emprunt': emprunt})
