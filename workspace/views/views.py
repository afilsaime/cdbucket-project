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
from django.db.models import Count, ExpressionWrapper, F, FloatField, Q
import random
import json
import datetime
import uuid



# Create your views here.
#Vue de la page d'accueil
class HomeView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():

            #Calcul de score pour recommandations
            ecoutes = MusicListen.objects.filter(user=self.request.user)
            ddl = MusicDownloads.objects.filter(user=self.request.user)
            likes_music = LikeMusic.objects.filter(user=self.request.user)
            likes_album = LikeAlbum.objects.filter(user=self.request.user)

            tag_score = {}

            ecoute_score= ecoutes.values('music__tag__intitule').annotate(nb_tag=ExpressionWrapper(Count('music__tag__intitule')*0.05,output_field=FloatField())).order_by('-nb_tag')
            ddl_score = ddl.values('music__tag__intitule').annotate(nb_tag=ExpressionWrapper(Count(F('music__tag__intitule'))*0.5,output_field=FloatField())).order_by('-nb_tag')

            for obj in ecoute_score:
                if obj['music__tag__intitule'] in tag_score:
                    tag_score[obj['music__tag__intitule']] += obj['nb_tag']
                else:
                    tag_score[obj['music__tag__intitule']] = obj['nb_tag']

            for obj in ddl_score:
                if obj['music__tag__intitule'] in tag_score:
                    tag_score[obj['music__tag__intitule']] += obj['nb_tag']
                else:
                    tag_score[obj['music__tag__intitule']] = obj['nb_tag']

            for obj in likes_album:
                for sub in obj.album.liste_tag():
                    if sub in tag_score:
                        tag_score[sub] += obj.album.liste_tag()[sub]*0.30
                    else:
                        tag_score[sub] = obj.album.liste_tag()[sub]*0.30

            for obj in likes_music:
                if obj.music.tag.intitule in tag_score:
                    tag_score[obj.music.tag.intitule] += 0.15
                else:
                    tag_score[obj.music.tag.intitule] = 0.15

            all_albums = Album.objects.all()
            ordered_tag_score = sorted(tag_score.iteritems(), key=lambda (k,v): (v,k),reverse=True)
            album_select = []

            for album in all_albums:
                current_tags = sorted(album.liste_tag().iteritems(), key=lambda (k,v): (v,k),reverse=True)
                print(ordered_tag_score)
                print(current_tags[0][0])
                if current_tags[0][0] in ordered_tag_score[0]:

                    album_select.append(album)

            #recherche des nouveautés
            nouveautes = Album.objects.filter(Q(type_album='AL')|Q(type_album='SI')).order_by('-date_publication')[:5]
            au_hazard = nouveautes[random.randint(0, len(nouveautes)-1)]

            context['recommandations'] = album_select[:4]
            context['nouveautes'] = nouveautes
            context['au_hazard'] = au_hazard
        return context

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
    #users_in_group = Group.objects.get(name="Artistes").user_set.all()

    def get_context_data(self,**kwargs):
        context = super(monCompte, self).get_context_data(**kwargs)

        try:
            groupes = self.request.user.groups.get(name="Artistes")
            context['group'] = groupes.name

            now = datetime.datetime.now()

            this_mth = now.month
            this_year = now.year

            if this_mth == 1:
                lst_mth = 12
                last_year = this_year - 1
            else:
                lst_mth = now.month - 1
                last_year = this_year

            ecoutes = MusicListen.objects.filter(music__auteur=self.request.user)
            ddl = MusicDownloads.objects.filter(music__auteur=self.request.user)
            likes_music = LikeMusic.objects.filter(music__auteur=self.request.user)
            likes_album = LikeAlbum.objects.filter(album__artiste=self.request.user)

            tag_score = {}
            tag_score_last_month = {}
            tag_score_this_month = {}
            ecoute_score= ecoutes.values('music__tag__intitule').annotate(nb_tag=ExpressionWrapper(Count('music__tag__intitule')*0.05,output_field=FloatField())).order_by('-nb_tag')
            ddl_score = ddl.values('music__tag__intitule').annotate(nb_tag=ExpressionWrapper(Count(F('music__tag__intitule'))*0.5,output_field=FloatField())).order_by('-nb_tag')

            ecoute_score_this_month= ecoutes.filter(date__month=this_mth,date__year=this_year).values('music__tag__intitule').annotate(nb_tag=ExpressionWrapper(Count('music__tag__intitule')*0.05,output_field=FloatField())).order_by('-nb_tag')
            ddl_score_this_month = ddl.filter(date__month=this_mth,date__year=this_year).values('music__tag__intitule').annotate(nb_tag=ExpressionWrapper(Count(F('music__tag__intitule'))*0.5,output_field=FloatField())).order_by('-nb_tag')

            ecoute_score_last_month = ecoutes.filter(date__month=lst_mth,date__year=last_year).values('music__tag__intitule').annotate(nb_tag=ExpressionWrapper(Count('music__tag__intitule')*0.05,output_field=FloatField())).order_by('-nb_tag')
            ddl_score_last_month = ddl.filter(date__month=lst_mth,date__year=last_year).values('music__tag__intitule').annotate(nb_tag=ExpressionWrapper(Count(F('music__tag__intitule'))*0.5,output_field=FloatField())).order_by('-nb_tag')

            ordered_tag_score = sorted(tag_score.iteritems(), key=lambda (k,v): (v,k),reverse=True)

            for obj in ecoute_score:
                if obj['music__tag__intitule'] in tag_score:
                    tag_score[obj['music__tag__intitule']] += obj['nb_tag']
                else:
                    tag_score[obj['music__tag__intitule']] = obj['nb_tag']

            for obj in ecoute_score_last_month:
                if obj['music__tag__intitule'] in tag_score_last_month:
                    tag_score_last_month[obj['music__tag__intitule']] += obj['nb_tag']
                else:
                    tag_score_last_month[obj['music__tag__intitule']] = obj['nb_tag']

            for obj in ecoute_score_this_month:
                if obj['music__tag__intitule'] in tag_score_this_month:
                    tag_score_this_month[obj['music__tag__intitule']] += obj['nb_tag']
                else:
                    tag_score_this_month[obj['music__tag__intitule']] = obj['nb_tag']

            print(tag_score)
            for obj in ddl_score:
                if obj['music__tag__intitule'] in tag_score:
                    tag_score[obj['music__tag__intitule']] += obj['nb_tag']
                else:
                    tag_score[obj['music__tag__intitule']] = obj['nb_tag']

            for obj in ddl_score_last_month:
                if obj['music__tag__intitule'] in tag_score_last_month:
                    tag_score_last_month[obj['music__tag__intitule']] += obj['nb_tag']
                else:
                    tag_score_last_month[obj['music__tag__intitule']] = obj['nb_tag']

            for obj in ddl_score_this_month:
                if obj['music__tag__intitule'] in tag_score_this_month:
                    tag_score_this_month[obj['music__tag__intitule']] += obj['nb_tag']
                else:
                    tag_score_this_month[obj['music__tag__intitule']] = obj['nb_tag']


            print(tag_score)

            for obj in likes_album:
                for sub in obj.album.liste_tag():
                    if sub in tag_score:
                        tag_score[sub] += obj.album.liste_tag()[sub]*0.30
                    else:
                        tag_score[sub] = obj.album.liste_tag()[sub]*0.30

            for obj in likes_album.filter(date__month=lst_mth,date__year=last_year):
                for sub in obj.album.liste_tag():
                    if sub in tag_score_last_month:
                        tag_score_last_month[sub] += obj.album.liste_tag()[sub]*0.30
                    else:
                        tag_score_last_month[sub] = obj.album.liste_tag()[sub]*0.30

            for obj in likes_album.filter(date__month=this_mth,date__year=this_year):
                for sub in obj.album.liste_tag():
                    if sub in tag_score_this_month:
                        tag_score_this_month[sub] += obj.album.liste_tag()[sub]*0.30
                    else:
                        tag_score_this_month[sub] = obj.album.liste_tag()[sub]*0.30

            print(tag_score)

            for obj in likes_music:
                if obj.music.tag.intitule in tag_score:
                    tag_score[obj.music.tag.intitule] += 0.15
                else:
                    tag_score[obj.music.tag.intitule] = 0.15

            for obj in likes_music.filter(date__month=lst_mth,date__year=last_year):
                if obj.music.tag.intitule in tag_score_last_month:
                    tag_score_last_month[obj.music.tag.intitule] += 0.15
                else:
                    tag_score_last_month[obj.music.tag.intitule] = 0.15

            for obj in likes_music.filter(date__month=this_mth,date__year=this_year):
                if obj.music.tag.intitule in tag_score_this_month:
                    tag_score_this_month[obj.music.tag.intitule] += 0.15
                else:
                    tag_score_this_month[obj.music.tag.intitule] = 0.15

            print(tag_score)
            ordered_tag_score = sorted(tag_score.iteritems(), key=lambda (k,v): (v,k),reverse=True)
            ordered_tag_score_last_month = sorted(tag_score_last_month.iteritems(), key=lambda (k,v): (v,k),reverse=True)
            ordered_tag_score_this_month = sorted(tag_score_this_month.iteritems(), key=lambda (k,v): (v,k),reverse=True)
            print(ordered_tag_score)

            if len(ordered_tag_score) > 0:
                best_tag_all_time = ordered_tag_score[0][0]
            else:
                best_tag_all_time = 'N/A'

            if len(ordered_tag_score_last_month) > 0:
                best_tag_last_month = ordered_tag_score_last_month[0][0]
            else:
                best_tag_last_month = 'N/A'

            if len(ordered_tag_score_this_month) > 0:
                best_tag_this_month = ordered_tag_score_this_month[0][0]
            else:
                best_tag_this_month = 'N/A'

            best_music_last_month = ecoutes.filter(date__month=lst_mth,date__year=last_year).values('music__titre').annotate(nb_ecoutes=Count('music__titre')).order_by('-nb_ecoutes')
            if best_music_last_month.count() > 0:
                best_music_last_month = best_music_last_month[0]['music__titre']
            else:
                best_music_last_month = 'N/A'

            best_music_this_month = ecoutes.filter(date__month=this_mth,date__year=this_year).values('music__titre').annotate(nb_ecoutes=Count('music__titre')).order_by('-nb_ecoutes')
            if best_music_this_month.count() > 0:
                best_music_this_month = best_music_this_month[0]['music__titre']
            else:
                best_music_this_month = 'N/A'

            best_music_all_time = ecoutes.values('music__titre').annotate(nb_ecoutes=Count('music__titre')).order_by('-nb_ecoutes')
            if best_music_all_time.count() > 0:
                best_music_all_time = best_music_all_time[0]['music__titre']
            else:
                best_music_all_time = 'N/A'

            most_ddl_last_month = ddl.filter(date__month=lst_mth,date__year=last_year).values('music__titre').annotate(nb_ddl=Count('music__titre')).order_by('-nb_ddl')
            if most_ddl_last_month.count() > 0:
                most_ddl_last_month = most_ddl_last_month[0]['music__titre']
            else:
                most_ddl_last_month = 'N/A'

            most_ddl_this_month = ddl.filter(date__month=this_mth,date__year=this_year).values('music__titre').annotate(nb_ddl=Count('music__titre')).order_by('-nb_ddl')
            if most_ddl_this_month.count() > 0:
                most_ddl_this_month = most_ddl_this_month[0]['music__titre']
            else:
                most_ddl_this_month = 'N/A'

            most_ddl_all_time = ddl.values('music__titre').annotate(nb_ddl=Count('music__titre')).order_by('-nb_ddl')
            if most_ddl_all_time.count() > 0:
                most_ddl_all_time = most_ddl_all_time[0]['music__titre']
            else:
                most_ddl_all_time = 'N/A'

            context['ecoutes'] = ecoutes.count()
            context['ecoutes_lst_mth'] = ecoutes.filter(date__month=lst_mth,date__year=last_year).count()
            context['ecoutes_this_mth'] = ecoutes.filter(date__month=this_mth,date__year=this_year).count()
            context['best_m'] = best_music_all_time
            context['best_m_last_mth'] = best_music_last_month
            context['best_m_this_mth'] = best_music_this_month
            context['ddl'] = ddl.count()
            context['ddl_lst_mth'] = ddl.filter(date__month=lst_mth,date__year=last_year).count()
            context['ddl_this_mth'] = ddl.filter(date__month=this_mth,date__year=this_year).count()
            context['best_d'] = most_ddl_all_time
            context['best_d_last_mth'] = most_ddl_last_month
            context['best_d_this_mth'] = most_ddl_this_month
            context['likes_m'] = likes_music.count()
            context['likes_m_this_month'] = likes_music.filter(date__month=this_mth,date__year=this_year).count()
            context['likes_m_last_month'] = likes_music.filter(date__month=lst_mth,date__year=last_year).count()
            context['likes_a'] = likes_album.count()
            context['likes_a_this_month'] = likes_album.filter(date__month=this_mth,date__year=this_year).count()
            context['likes_a_last_month'] = likes_album.filter(date__month=lst_mth,date__year=last_year).count()
            context['best_tag'] = best_tag_all_time
            context['best_tag_last_month'] = best_tag_last_month
            context['best_tag_this_month'] = best_tag_this_month

        except ObjectDoesNotExist:
            context['group'] = "User"

        return context



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

    def get(self, request, *args, **kwargs):
        form = SearchForm(self.request.GET or None)
        if form.is_valid():
            return self.form_valid(form)




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

def add_music_listen(request):
    if request.method == 'POST':
        idmusic = request.POST.get('music')
        response_data = {}
        music = Music.objects.get(id=idmusic)
        user = request.user

        musicListen = MusicListen(user=user,music=music)
        musicListen.save()
        response_data['status'] = 'listen added'
        response_data['listenpk'] = musicListen.id
        response_data['user'] = musicListen.user.username
        response_data['date'] = "{0}/{1}/{2}".format(musicListen.date.day,musicListen.date.month,musicListen.date.year)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def add_music_download(request):
    if request.method == 'POST':
        idmusic = request.POST.get('music')
        response_data = {}
        music = Music.objects.get(id=idmusic)
        user = request.user

        musicDownloads = MusicDownloads(user=user,music=music)
        musicDownloads.save()
        response_data['status'] = 'download added'
        response_data['downloadpk'] = musicDownloads.id
        response_data['user'] = musicDownloads.user.username
        response_data['date'] = "{0}/{1}/{2}".format(musicDownloads.date.day,musicDownloads.date.month,musicDownloads.date.year)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

class MyAlbumsView(TemplateView):
    template_name = "mes_albums.html"

    def get_context_data(self, **kwargs):
        context = super(MyAlbumsView,self).get_context_data(**kwargs)

        context['albums'] = Album.objects.filter(artiste=self.request.user)
        return context

class playlist_accueil(TemplateView):
    template_name = "playlist_accueil.html"
