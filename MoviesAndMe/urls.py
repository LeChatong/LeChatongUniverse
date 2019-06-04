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
    url(r'^actor/tv/(?P<id>[0-9]+)/$', views.tvs_on_actor, name='tvs_on_actor'),
    url(r'^movie/actors/(?P<id>[0-9]+)/$', views.actors_on_movie, name='actors_on_movie'),
    url(r'^movie/home/$', views.home_movie, name='home_movie'),
    url(r'^movie/popular/(?P<page>[0-9]+)/$', views.popular_movie, name='popular_movie'),
    url(r'^movie/upcoming/(?P<page>[0-9]+)/$', views.upcoming_movie, name='upcoming_movie'),
    url(r'^tv/home/$', views.home_tv, name='home_tv'),
    url(r'^tv/popular/(?P<page>[0-9]+)/$', views.popular_tv, name='popular_tv'),
    url(r'^tv/details/(?P<id>[0-9]+)/$', views.details_tv, name='details_tv'),
    url(r'^tv/details/(?P<id>[0-9]+)/season/(?P<season>[0-9]+)$', views.details_season_tv, name='details_tv_season'),
]