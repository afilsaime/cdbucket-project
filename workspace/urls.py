from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from views import *
#test de commentaire pour le commit
urlpatterns = [
   url(r'^base', HelloWorld.as_view()),
   # url(r'^musiques', ListMusic.as_view(),name="listmusic"),
   # url(r'^musique/(?P<pk>\d+)$', MusicDetail.as_view(), name="detailmusic"),
   url(r'^artist-sign-up$', ArtistRegistrationView.as_view(), name="artist-sign-up"),
   url(r'^artist-sign-up/thanks$',TemplateView.as_view(template_name="thanks.html"),name="thanks"),
   url(r'^comptes/activation/(?P<key>\w+)$',ActivationView.as_view(), name="activation"),
   url(r'^music/add$', CreateMusicView.as_view(), name="ajout_musique")
]
