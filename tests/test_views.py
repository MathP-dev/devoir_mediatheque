import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from gestion_bibliotheque.models import Livre, DVD, CD, JeuDePlateau, Emprunteur, Emprunt, Media

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="pass")

@pytest.fixture
def client_logged(client, user):
    client.force_login(user)
    return client

@pytest.mark.django_db
def test_profile_view(client_logged):
    url = reverse('profile')
    response = client_logged.get(url)
    assert response.status_code == 200
    assert 'gestion_bibliotheque/profile.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_liste_medias_view(client_logged):
    Livre.objects.create(name="Livre1", auteur="Auteur1")
    DVD.objects.create(name="DVD1", realisateur="Realisateur1")
    CD.objects.create(name="CD1", artiste="Artiste1")
    JeuDePlateau.objects.create(name="Jeu1", createur="Createur1")
    url = reverse('liste_medias')
    response = client_logged.get(url)
    assert response.status_code == 200
    assert 'livres' in response.context
    assert 'dvd' in response.context
    assert 'cd' in response.context
    assert 'jeux' in response.context

@pytest.mark.django_db
def test_liste_membres_view(client_logged):
    Emprunteur.objects.create(name="Membre1")
    url = reverse('liste_membres')
    response = client_logged.get(url)
    assert response.status_code == 200
    assert 'membres' in response.context

@pytest.mark.django_db
def test_ajouter_media_view_get(client_logged):
    url = reverse('ajouter_media')
    response = client_logged.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_ajouter_media_view_post_livre(client_logged):
    url = reverse('ajouter_media')
    data = {
        'type_media': 'livre',
        'name': 'LivreTest',
        'auteur': 'AuteurTest'
    }
    response = client_logged.post(url, data)
    assert response.status_code == 302
    assert Livre.objects.filter(name='LivreTest').exists()

@pytest.mark.django_db
def test_ajouter_membre_view_get(client_logged):
    url = reverse('ajouter_membre')
    response = client_logged.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_ajouter_membre_view_post(client_logged):
    url = reverse('ajouter_membre')
    data = {'name': 'Membre2'}
    response = client_logged.post(url, data)
    assert response.status_code == 302
    assert Emprunteur.objects.filter(name='Membre2').exists()

@pytest.mark.django_db
def test_mettre_a_jour_membre_view_get(client_logged):
    membre = Emprunteur.objects.create(name="Membre3")
    url = reverse('mettre_a_jour_membre', args=[membre.id])
    response = client_logged.get(url)
    assert response.status_code == 200
    assert 'form' in response.context

@pytest.mark.django_db
def test_mettre_a_jour_membre_view_post(client_logged):
    membre = Emprunteur.objects.create(name="Membre4")
    url = reverse('mettre_a_jour_membre', args=[membre.id])
    data = {'name': 'Membre4_modif'}
    response = client_logged.post(url, data)
    assert response.status_code == 302
    membre.refresh_from_db()
    assert membre.name == 'Membre4_modif'

@pytest.mark.django_db
def test_emprunter_media_view_get(client_logged):
    media = Media.objects.create(name="Media1", disponible=True)
    Emprunteur.objects.create(name="Membre5")
    url = reverse('emprunter_media', args=[media.id])
    response = client_logged.get(url)
    assert response.status_code == 200
    assert 'media' in response.context

@pytest.mark.django_db
def test_emprunter_media_view_post(client_logged, mocker):
    media = Media.objects.create(name="Media2", disponible=True)
    emprunteur = Emprunteur.objects.create(name="Membre6")
    mocker.patch.object(Emprunteur, 'peut_emprunter', return_value=True)
    url = reverse('emprunter_media', args=[media.id])
    data = {'emprunteur': emprunteur.id}
    response = client_logged.post(url, data)
    assert response.status_code == 302
    media.refresh_from_db()
    assert not media.disponible
    assert Emprunt.objects.filter(media=media, emprunteur=emprunteur).exists()

@pytest.mark.django_db
def test_retourner_emprunt_view_get(client_logged):
    media = Media.objects.create(name="Media3", disponible=False)
    emprunteur = Emprunteur.objects.create(name="Membre7")
    emprunt = Emprunt.objects.create(media=media, emprunteur=emprunteur)
    url = reverse('retourner_emprunt', args=[emprunt.id])
    response = client_logged.get(url)
    assert response.status_code == 200
    assert 'emprunt' in response.context

@pytest.mark.django_db
def test_retourner_emprunt_view_post(client_logged):
    media = Media.objects.create(name="Media4", disponible=False)
    emprunteur = Emprunteur.objects.create(name="Membre8")
    emprunt = Emprunt.objects.create(media=media, emprunteur=emprunteur)
    url = reverse('retourner_emprunt', args=[emprunt.id])
    response = client_logged.post(url)
    assert response.status_code == 302
    media.refresh_from_db()
    emprunt.refresh_from_db()
    assert media.disponible
    assert emprunt.date_retour is not None