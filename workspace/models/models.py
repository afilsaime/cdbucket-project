# coding: utf8
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import os

# Create your models here.
class Registration(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return "{0}:{1}".format(self.user.username,self.key)


class Tag(models.Model):
    intitule = models.CharField(max_length=100)

    def __str__(self):
        return self.intitule

def renomage(instance,name):
    username = instance.auteur.username
    album = instance.album.titre
    date_publication = instance.album.date_publication
    date_str = "{0}-{1}-{2}".format(date_publication.day,date_publication.month,date_publication.year)

    return os.path.join(username,album,date_str,name)

class Music(models.Model):
    titre = models.CharField(max_length=100)
    duree = models.DurationField()
    album = models.ForeignKey('Album')
    tag = models.ForeignKey('Tag')
    auteur = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    path = models.FileField(upload_to=renomage,max_length=100)

    def __str__(self):
        return "{0} de {1} duree: {2}".format(self.titre,self.auteur.username, self.duree)

class Signalement(models.Model):
    artiste = models.ForeignKey(User)
    music = models.ForeignKey(Music)
    traite = models.BooleanField(default = False)
    creation = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        if self.traite:
            traitement = "oui"
        else:
            traitement = "non"
        return "titre '{0}' signalé par {1}, traité: {2}".format(self.music, self.artiste, traitement)

class Album(models.Model):
    ALBUM = 'AL'
    PLAYLIST = 'PL'
    SINGLE = 'SI'

    TYPE_ALBUM_CHOICES = (
        (ALBUM,'Album'),
        (PLAYLIST,'Playlist'),
        (SINGLE,'Single'),
    )

    titre = models.CharField(max_length=100)
    artiste = models.ForeignKey(User)
    date_publication = models.DateField()
    type_album = models.CharField(max_length=2,choices=TYPE_ALBUM_CHOICES,default=ALBUM)

    def liste_musique(self):
        return self.music_set.all()

    def duree_totale(self):
        total_duration = timedelta()
        q = self.music_set.all()
        for music in q:
            total_duration += music.duree

        minutes = (total_duration.days*3600*24)

        return "{0} min {1}".format(minutes,total_duration.seconds)

    def liste_tag(self):
        q = self.music_set.all()
        taglist = {}
        for music in q:
            if taglist[music.tag]:
                taglist[music.tag] += 1
            else:
                taglist[music.tag] = 0
        return taglist

    def __str__(self):
        return "{0} de {1}".format(self.titre,self.artiste)
