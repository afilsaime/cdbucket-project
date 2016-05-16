# coding: utf8
from django import forms
from django.contrib.auth.models import User
from workspace.models import *
import os

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2:
            if password != password2:
                msg = "Les deux mots de passe sont differents"
                self.add_error("password",msg)

            if len(password) < 8:
                msg = "La taille du mot de passe doit être d'au moins 8 caracteres"
                self.add_error("password",msg)

        if email:
            mailquery = User.objects.filter(email=email)
            if len(mailquery) != 0:
                msg = "Un utilisateur avec cet email a déja été enregistré"
                self.add_error("email",msg)

        if username:
            userquery = User.objects.filter(username=username)
            if len(userquery)!= 0:
                msg = "Ce nom d'utilisateur n'est pas disponible"
                self.add_error("username",msg)

        return cleaned_data


class MySelect(forms.Select):
    def render_option(self, selected_choices, option_value, option_label):
        # look at the original for something to start with
        return '<option data-class="icon-folder-plus" value="{0}">{1}</option>'.format(option_value,option_label);

class CreateMusicForm(forms.Form):

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user',None)
        super(CreateMusicForm,self).__init__(*args,**kwargs)

    titre = forms.CharField()
    duree = forms.DurationField()
    #album = forms.ModelChoiceField(queryset=Album.objects.filter(artiste__username=self.user.username).exclude(type_album='PL'))
    album = forms.ModelChoiceField(queryset=Album.objects.filter(artiste__username="toto").exclude(type_album='PL'),widget=MySelect(attrs={'class':'cs-select cs-skin-slide'}))
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(),widget=MySelect(attrs={'class':'cs-select cs-skin-slide'}))
    path = forms.FileField()

    def clean(self):
        possible_extension = ['.mp3','.ogg','.wav']
        cleaned_data = super(CreateMusicForm,self).clean()
        cleaned_path = cleaned_data.get('path')
        if cleaned_path:
            cleaned_name = cleaned_path.name
            extension = os.path.splitext(cleaned_name)[1]

            if extension not in possible_extension:
                msg = "Veuillez renseigner un fichier audio"
                self.add_error("path",msg)

                return cleaned_data
