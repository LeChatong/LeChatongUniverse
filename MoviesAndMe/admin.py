from django.contrib import admin
from .models import movie_detail, tv_detail
# Register your models here.

admin.site.register(movie_detail)
admin.site.register(tv_detail)