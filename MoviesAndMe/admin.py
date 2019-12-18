from django.contrib import admin
from .models import movie_detail, tv_detail
import requests
from django.core import serializers
from django.http import HttpResponse
# Register your models here.

class movie_detailAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('title_movie', 'link_telegram')
    search_fields = ('title_movie',)
    fieldsets = (
        ('Général', {
            'classes': ['wide', 'extrapretty'],
            'fields': ('id_movie', 'link_telegram',
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
    list_display = ('title_tv', 'link_telegram')
    search_fields = ('title_tv',)
    fieldsets = (
        ('Général', {
            'classes': ['wide', 'extrapretty'],
            'fields': ('id_tv', 'nb_season', 'nb_episode', 'link_telegram',
                       'voice_language', 'quality_video', 'quality_audio',
                       'subtitle', 'subtitle_language')
        }),
    )
    exclude = ('title_tv',)
    def save_model(self, request, obj, form, change):
        response_tv = requests.get(
            'https://api.themoviedb.org/3/tv/' + str(obj.id_tv) + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
        tv = response_tv.json()
        obj.title_tv = tv['name']+' S '+str(obj.nb_season)+' EPS '+str(obj.nb_episode)
        super().save_model(request, obj, form, change)

def export_as_json(ModelAdmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

admin.site.register(movie_detail, movie_detailAdmin)
admin.site.register(tv_detail, tv_detailAdmin)
admin.site.add_action(export_as_json)