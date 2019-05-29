from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [

    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('search', views.search_movies, name='search_movies'),
    path('movie/details/<str:id>', views.details_movie, name='details_movie'),
    path('actor/details/<str:id>', views.details_actor, name='details_actor'),
    path('actor/movies/<str:id>', views.movies_on_actor, name='movies_on_actor'),
    path('movie/actors/<str:id>', views.actors_on_movie, name='actors_on_movie'),
    path('tv/home/<str:page>', views.home_tv, name='home_tv'),
]