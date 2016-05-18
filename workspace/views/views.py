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
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
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
        auteur = User.objects.get(username="toto")

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

class AccessMusicView(DetailView):
    context_object_name = "music"
    model = Music
    template_name = "single_music.html"

def ConnexionView(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)
                return redirect(reverse("home"))
                 # nous connectons l'utilisateur
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'connexion.html', locals())





def deconnexion(request):
    logout(request)
    return redirect(reverse('connexion'))



class monCompte(TemplateView):
    template_name = "mon_compte.html"


class NewEmail(FormView):
    template_name = "new_email.html"
    form_class = NewEmail
    success_url = "/workspace/new_email"

    def form_valid(self,form):
        #Sauvegarde de l'utilisateur
        user = self.request.user
        email = form.cleaned_data['new_email']
        #user.
        user.save()
        #ENVOI DE MAIL
    #    sujet = "Nouvelle adresse Email"
    #    titre = "<h1>Mis à jour Email</h1></br></br>"
    #    message = "Votre nouvelle adresse email a été enregistré !:</br>"
    #    send_mail(sujet,titre+message,"site@project.com",[email])

        return super(NewEmail,self).form_valid(form)


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
    #form_class = 
    success_url = "/workspace/home"


    def form_valid(self,form):
        #Sauvegarde de l'utilisateur
        user = self.request.user
        user.is_active = False
        user.save()


        #ENVOI DE MAIL
        #sujet = "Nouveau mot de passe"
    #    titre = "<h1>Mis à jour mot de passe</h1></br></br>"
    #    message = "Votre nouveau mot de passe a été enregistré !:</br>"
    #    send_mail(sujet,titre+message,"site@project.com",[email])

        return super(SupprCompte,self).form_valid(form)





# -> inactif renvoi faux
