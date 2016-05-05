from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from workspace.models import *
from workspace.forms import *
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

class CreateMusicView(FormView):
    template_name = "create_music.html"
    form_class = CreateMusicForm
    success_url = "/workspace/music/add"
    success = False

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
        self.success = True

        return super(CreateMusicView,self).form_valid(form)

    def get_context_data(self,**kwargs):
        context = super(CreateMusicView,self).get_context_data(**kwargs)
        context['success'] = self.success

        return context
