from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from views import *

urlpatterns = [
   url(r'^base', HelloWorld.as_view()),
   # url(r'^musiques', ListMusic.as_view(),name="listmusic"),
   # url(r'^musique/(?P<pk>\d+)$', MusicDetail.as_view(), name="detailmusic"),
   url(r'^sign-up/(?P<type>artist|user)$', RegistrationView.as_view(), name="sign-up"),
   url(r'^sign-up/thanks$',TemplateView.as_view(template_name="thanks.html"),name="thanks"),
   url(r'^comptes/activation/(?P<key>\w+)',ActivationView.as_view(), name="activation"),
   url(r'^music/add$', CreateMusicView.as_view(), name="ajout_musique")
]
