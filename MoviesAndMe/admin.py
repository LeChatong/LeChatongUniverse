from django.contrib import admin
from .models import movie_detail, tv_detail
# Register your models here.

class movie_detailAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('title_movie', 'link_telegram')
    search_fields = ('title_movie',)

class tv_detailAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ('title_tv', 'link_telegram')
    search_fields = ('title_tv',)

admin.site.register(movie_detail, movie_detailAdmin)
admin.site.register(tv_detail, tv_detailAdmin)