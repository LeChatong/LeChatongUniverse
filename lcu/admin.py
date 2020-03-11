from django.contrib import admin
from django.contrib import admin
from .models import movie_detail, tv_detail, member
import requests
from django.core import serializers
from django.http import HttpResponse
import hashlib

# Register your models here.

# Register your models here.
class memberAdmin(admin.ModelAdmin):
    list_per_page = 30
    search_fields = ('first_name','username', 'email,''created_at', 'last_connexion', 'is_active', 'is_modarator', 'is_delete')
    list_display = ('first_name', 'username', 'email')
    fieldsets = (
        ('Général', {
            'classes': ['wide', 'extrapretty'],
            'fields': ('first_name', 'username', 'password',
                       'email', 'is_active', 'is_delete',
                       'is_modarator', 'avatar')
        }),
    )
    def save_model(self, request, obj, form, change):
        password_crypt = hashlib.sha1(obj.password.encode('utf-8')).hexdigest()
        obj.password = password_crypt
        super().save_model(request, obj, form, change)

class movie_detailAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('title_movie', 'link_download')
    search_fields = ('title_movie',)
    fieldsets = (
        ('Général', {
            'classes': ['wide', 'extrapretty'],
            'fields': ('id_movie', 'link_download',
                       'voice_language', 'quality_video', 'quality_audio',
                       'subtitle', 'subtitle_language')
        }),
    )
    exclude = ('title_movie',)
    def save_model(self, request, obj, form, change):
        response_movie = requests.get(
            'https://api.themoviedb.org/3/movie/' + str(obj.id_movie) + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
        movie = response_movie.json()
        obj.title_movie = movie['title']
        super().save_model(request, obj, form, change)

class tv_detailAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('title_tv', 'link_download')
    search_fields = ('title_tv',)
    fieldsets = (
        ('Général', {
            'classes': ['wide', 'extrapretty'],
            'fields': ('id_tv', 'nb_season', 'nb_episode', 'link_download',
                       'voice_language', 'quality_video', 'quality_audio',
                       'subtitle', 'subtitle_language')
        }),
    )
    exclude = ('title_tv',)
    def save_model(self, request, obj, form, change):
        response_tv = requests.get(
            'https://api.themoviedb.org/3/tv/' + str(obj.id_tv) + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
        tv = response_tv.json()
        obj.title_tv = tv['name']+' saison '+str(obj.nb_season)+' épisode '+str(obj.nb_episode)
        super().save_model(request, obj, form, change)

def export_as_json(ModelAdmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

admin.site.register(member, memberAdmin)
admin.site.register(movie_detail, movie_detailAdmin)
admin.site.register(tv_detail, tv_detailAdmin)
admin.site.add_action(export_as_json)