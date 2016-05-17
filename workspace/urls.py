from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from views import *

urlpatterns = [
   url(r'^base', HelloWorld.as_view()),
   # url(r'^musiques', ListMusic.as_view(),name="listmusic"),
   # url(r'^musique/(?P<pk>\d+)$', MusicDetail.as_view(), name="detailmusic"),
   url(r'^sign-up/(?P<type>artist|user)$', RegistrationView.as_view(), name="sign-up"),
   url(r'^sign-up/thanks$',TemplateView.as_view(template_name="thanks.html"),name="thanks"),
   url(r'^home/$',TemplateView.as_view(template_name="base.html"),name="home"),
   url(r'^comptes/activation/(?P<key>\w+)',ActivationView.as_view(), name="activation"),
   url(r'^music/add$', CreateMusicView.as_view(), name="ajout_musique"),
   url(r'^music/listen/(?P<pk>\d+)$',AccessMusicView.as_view(),name="ecouter_musique"),
   url(r'^connexion/$', ConnexionView, name="connexion"),
   url(r'^deconnexion/$', deconnexion, name="deconnexion"),
   url(r'^mon_compte/$', monCompte.as_view(), name="mon_compte"),
   url(r'^new_mdp/$', login_required(NewMDP.as_view()), name="new_mdp"),
   url(r'^new_email/$', login_required(NewEmail.as_view()), name="new_email"),
   url(r'^suppr_compte/$', login_required(SupprCompte.as_view()), name="suppr_compte"),
]
