from django.contrib import admin
from workspace.models import *
# Register your models here.

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('key','user')
    search_fields = ('key','user')

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titre','artiste','date_publication','type_album')
    search_fields = ('titre','artiste')
    list_filter = ('type_album',)

class MusicAdmin(admin.ModelAdmin):
    list_display = ('titre','auteur','album','duree','tag','path')
    list_filter = ('tag','auteur')

admin.site.register(Registration,RegistrationAdmin)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Music,MusicAdmin)
admin.site.register(LikeMusic)
admin.site.register(Tag)
