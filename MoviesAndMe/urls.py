from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^search/$', views.search_movies, name='search_movies'),
    url(r'^movie/details/(?P<id>[0-9]+)/$', views.details_movie, name='details_movie'),
    url(r'^actor/details/(?P<id>[0-9]+)/$', views.details_actor, name='details_actor'),
    url(r'^actor/movies/(?P<id>[0-9]+)/$', views.movies_on_actor, name='movies_on_actor'),
    url(r'^movie/actors/(?P<id>[0-9]+)/$', views.actors_on_movie, name='actors_on_movie'),
    url(r'^movie/home/(?P<page>[0-9]+)/$', views.home_movie, name='home_movie'),
    url(r'^tv/home/(?P<page>[0-9]+)/$', views.home_tv, name='home_tv'),
]