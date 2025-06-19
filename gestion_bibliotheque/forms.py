from django import forms
from .models import Emprunteur, Media, Emprunt

class MembreForm(forms.ModelForm):
    class Meta:
        model = Emprunteur
        fields = ['name']

class MediaForm(forms.Form):
    TYPE_CHOICES = [
        ('livre', 'Livre'),
        ('dvd', 'DVD'),
        ('cd', 'CD'),
        ('jeu', 'Jeu de Plateau'),
    ]

    type_media = forms.ChoiceField(choices=TYPE_CHOICES)
    name = forms.CharField(max_length=255)
    auteur = forms.CharField(max_length=255, required=False)
    realisateur = forms.CharField(max_length=255, required=False)
    artiste = forms.CharField(max_length=255, required=False)
    createur = forms.CharField(max_length=255, required=False)

class EmpruntForm(forms.ModelForm):
    class Meta:
        model = Emprunt
        fields = ['emprunteur']
