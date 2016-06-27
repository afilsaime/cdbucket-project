# coding: utf8
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from workspace.models import *
from workspace.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import datetime
import uuid



# Create your views here.
class HelloWorld(TemplateView):
    template_name = "base.html"

# class ListMusic(ListView):
#     template_name = "liste.html"
#     context_object_name = "Music"
#     model = Music
#
# class MusicDetail(DetailView):
#     template_name = "detail.html"
#     context_object_name = "Music"
#     model = Music

class RegistrationView(FormView):
    template_name = "registration.html"
    form_class = RegistrationForm
    success_url = "/workspace/sign-up/thanks"

    def form_valid(self,form):
        #Sauvegarde de l'utilisateur
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        new_user = User.objects.create_user(username,email,password)
        #Verifie si l'utilisateur est un artiste ou non
        monparam = self.kwargs['type']
        if monparam == 'artist':
            new_user.groups.add(Group.objects.get(name="Artistes"))

        new_user.is_active = False
        new_user.save()

        #CLE D'ENREGISTREMENT
        uniq_key = uuid.uuid1().hex
        Registration(user=new_user,key=uniq_key).save()

        #ENVOI DE MAIL
        sujet = "Activation du compte"
        titre = "<h1>Activation de votre compte</h1></br></br>"
        message = "Veuillez acceder a ce lien pour activer votre compte:</br>"
        lien = "127.0.0.1:8000/workspace/comptes/activation/{0}".format(uniq_key)
        send_mail(sujet,titre+message+lien,"site@project.com",[email])



        return super(RegistrationView,self).form_valid(form)

class ActivationView(TemplateView):
    template_name = "activation.html"

    def dispatch(self,request,*args,**kwargs):
        key = kwargs['key']
        if key:
            regobject = get_object_or_404(Registration,key=key)
            regobject.user.is_active = True
            regobject.user.save()
            regobject.delete()

        return super(ActivationView,self).dispatch(request,*args,**kwargs)

class CreateMusicView(PermissionRequiredMixin,SuccessMessageMixin,FormView):
    template_name = "create_music.html"
    form_class = CreateMusicForm
    success_url = "/workspace/music/add"
    permission_required = 'workspace.add_music'
    success_message = 'Musique ajoutée'

    def handle_no_permission(self):
        return HttpResponseForbidden()

    def get_form_kwargs(self):
        kwargs = super(CreateMusicView,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self,form):
        titre = form.cleaned_data['titre']
        duree = form.cleaned_data['duree']
        album = form.cleaned_data['album']
        tag = form.cleaned_data['tag']
        path = form.cleaned_data['path']
        #artiste = self.request.user
        auteur = User.objects.get(username=self.request.user.username)

        music = Music()
        music.titre = titre
        music.duree = duree
        music.album = album
        music.tag = tag

        music.auteur = auteur

        music.save()
        music.path = self.request.FILES['path']
        music.save()
        return super(CreateMusicView,self).form_valid(form)

class AddAlbumView(PermissionRequiredMixin,SuccessMessageMixin,FormView):
    template_name = "add_album.html"
    form_class = AddAlbumForm
    success_url = "/workspace/album/add"
    permission_required = 'workspace.add_album'
    success_message = 'Album ajouté'

    def handle_no_permission(self):
        return HttpResponseForbidden()

    def form_valid(self,form):
        titre = form.cleaned_data['titre']
        date = form.cleaned_data['date']
        type = form.cleaned_data['type']
        artiste = self.request.user

        new_album = Album(titre=titre,date_publication=date,type_album=type,artiste=artiste).save()
        return super(AddAlbumView,self).form_valid(form)

class AddPlaylistView(SuccessMessageMixin,FormView):
    template_name = "add_playlist.html"
    form_class = AddPlaylistForm
    success_url = "/workspace/playlist/add"
    success_message = 'Playliste ajoutée'

    def form_valid(self,form):
        titre = form.cleaned_data['titre']
        date = datetime.datetime.now()
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        print(date)
        print("+++++++++++++++++++++++++++++++++++++++++++++")
        type = Album.PLAYLIST
        artiste = self.request.user

        new_album = Album(titre=titre,date_publication=date,type_album=type,artiste=artiste).save()
        return super(AddPlaylistView,self).form_valid(form)

class AccessMusicView(DetailView):
    context_object_name = "music"
    model = Music
    template_name = "single_music.html"

class AccessAlbumView(DetailView):
    context_object_name = "Album"
    model = Album
    template_name = "album.html"

    def get_context_data(self, **kwargs):
        context = super(AccessAlbumView, self).get_context_data(**kwargs)
        user = self.request.user
        liked_musics = user.likemusic_set.filter(music__album=self.get_object()).values_list('music',flat=True)
        context['Liked_musics'] = liked_musics
        try:
            albums_liked = user.likealbum_set.get(album=self.get_object())
            context['is_liked'] = True
            groupes = self.request.user.groups.get(name="Artistes")
            context['group'] = groupes.name
        except ObjectDoesNotExist:
            context['is_liked'] = False
            context['group'] = "User"
        return context


class monCompte(TemplateView):
    template_name = "mon_compte.html"
    users_in_group = Group.objects.get(name="Artistes").user_set.all()

    def get_context_data(self,**kwargs):
        context = super(monCompte, self).get_context_data(**kwargs)

        try:
            groupes = self.request.user.groups.get(name="Artistes")
            context['group'] = groupes.name

        except ObjectDoesNotExist:
            context['group'] = "User"

        return context

class monCompte_artiste(TemplateView):
    template_name = "mon_compte_artiste.html"

class NewEmail(FormView):
    template_name = "new_email.html"
    form_class = NewEmail
    success_url = "/workspace/new_email"

    def form_valid(self,form):
        #Sauvegarde de l'utilisateur
        user = self.request.user
        new_email = form.cleaned_data['new_email']
        user.save()

        uniq_key = uuid.uuid1().hex
        Registration(user=user,key=uniq_key,email=new_email).save()

        #ENVOI DE MAIL
        sujet = "Mise à jours adresse email"
        titre = "<h1>Validation de votre adresse mail</h1></br></br>"
        message = "Veuillez acceder a ce lien pour activer votre nouvelle adresse email:</br>"
        lien = "127.0.0.1:8000/workspace/email_activation/{0}".format(uniq_key)
        send_mail(sujet,titre+message+lien,"site@project.com",[new_email])

        return super(NewEmail,self).form_valid(form)



class Email_Activation(FormView):
    template_name = "mon_compte.html"

    def dispatch(self,request,*args,**kwargs):
        key = kwargs['key']
        if key:
            regobject = get_object_or_404(Registration,key=key)
            regobject.user.email=regobject.email
            regobject.user.save()
            regobject.delete()

        return redirect(reverse("mon_compte"))



#deconnexion intempestive au changement de MDP !
class NewMDP(FormView):
    template_name = "new_mdp.html"
    form_class = NewPassword
    success_url = "/workspace/new_mdp"

    def form_valid(self,form):
        #Sauvegarde de l'utilisateur
        user = self.request.user
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        #ENVOI DE MAIL
        #sujet = "Nouveau mot de passe"
    #    titre = "<h1>Mis à jour mot de passe</h1></br></br>"
    #    message = "Votre nouveau mot de passe a été enregistré !:</br>"
    #    send_mail(sujet,titre+message,"site@project.com",[email])

        return super(NewMDP,self).form_valid(form)


class SupprCompte(FormView):
    template_name = "suppr_compte.html"
    form_class = SupprCompteForm
    success_url = "/workspace/home"

    def get_form_kwargs(self):
        kwargs = super(SupprCompte,self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def form_valid(self,form):
        #Sauvegarde de l'utilisateur
        user = self.request.user
        logout(self.request)
        user.is_active = False
        user.save()


        #ENVOI DE MAIL
        #sujet = "Nouveau mot de passe"
    #    titre = "<h1>Mis à jour mot de passe</h1></br></br>"
    #    message = "Votre nouveau mot de passe a été enregistré !:</br>"
    #    send_mail(sujet,titre+message,"site@project.com",[email])

        #return redirect(reverse("home"))
        return super(SupprCompte,self).form_valid(form)


class MyPlaylist(DetailView):
    context_object_name = "Album"
    model = Album
    template_name = "my_playlist.html"

    def form_valid(**kwargs):
        albums = Album.objects.filter(type_album=playlist)
        context = self.get_context_data(**kwargs)
        context['Album'] = albums
        print(albums)
        return self.render_to_response(context)

class Search(FormView):
    template_name = "search.html"
    form_class = SearchForm

    def form_valid(self,form,**kwargs):
        group = Group.objects.get(name='Artistes')
        query = form.cleaned_data['query']
        musiques = Music.objects.filter(titre__icontains=query)
        artistes = group.user_set.filter(username__icontains=query)
        albums = Album.objects.filter(titre__icontains=query)
        context = self.get_context_data(**kwargs)
        context['Albums'] = albums
        context['Artistes'] = artistes
        context['Musiques'] = musiques
        return self.render_to_response(context)


class Contact(TemplateView):
    template_name = "contact.html"

    def form_valid(self, form):
        user_email = form.cleaned_data['user_email']
        #ENVOI DE MAIL
        sujet = form.cleaned_data['sujet']
        message = form.cleaned_data['message']
        send_mail(sujet,message,"amaouch.w@live.fr",[user_email])

        #return redirect(reverse("home"))
        return super(Contact,self).form_valid(form)


class fiche_artiste(DetailView):
    context_object_name = "artiste"
    model = User
    template_name = "fiche_artiste.html"


    def get_context_data(self,**kwargs):
        context = super(fiche_artiste, self).get_context_data(**kwargs)
        utilisateur = super(fiche_artiste, self).get_object()
        albums = Album.objects.filter(artiste=utilisateur.id).exclude(type_album='PL')
        context['Albums'] = albums
        return context





def toggle_like(request):
    if request.method == 'POST':
        idmusic = request.POST.get('music')
        response_data = {}
        music = Music.objects.get(id=idmusic)
        user = request.user
        try:
            likeToDelete = user.likemusic_set.get(music=music)
            likeToDelete.delete()

            response_data['result'] = 'Like deleted!'

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        except ObjectDoesNotExist:
            like = LikeMusic(music=music, user=request.user)
            like.save()

            response_data['result'] = 'Like added!'
            response_data['likepk'] = like.id
            response_data['user'] = like.user.username

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def toggle_like_album(request):
    if request.method == 'POST':
        idalbum = request.POST.get('album')
        response_data = {}
        album = Album.objects.get(id=idalbum)
        user = request.user
        try:
            likeToDelete = user.likealbum_set.get(album=album)
            likeToDelete.delete()

            response_data['status'] = 'deleted'

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        except ObjectDoesNotExist:
            like = LikeAlbum(album=album, user=request.user)
            like.save()

            response_data['status'] = 'added'
            response_data['likepk'] = like.id
            response_data['user'] = like.user.username

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


class mes_albums(TemplateView):
    template_name = "mes_albums.html"

class playlist_accueil(TemplateView):
    template_name = "playlist_accueil.html"
