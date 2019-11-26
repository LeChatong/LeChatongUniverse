from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^research/$', views.search_movies, name='search_movies'),
    url(r'^movie/details/(?P<id>[0-9]+)/$', views.details_movie, name='details_movie'),
    url(r'^actor/details/(?P<id>[0-9]+)/$', views.details_actor, name='details_actor'),
    url(r'^actor/movies/(?P<id>[0-9]+)/$', views.movies_on_actor, name='movies_on_actor'),
    url(r'^actor/tv/(?P<id>[0-9]+)/$', views.tvs_on_actor, name='tvs_on_actor'),
    url(r'^movie/actors/(?P<id>[0-9]+)/$', views.actors_on_movie, name='actors_on_movie'),
    url(r'^tv/actors/(?P<id>[0-9]+)/$', views.actors_on_tv, name='actors_on_tv'),
    url(r'^movie/home/$', views.home_movie, name='home_movie'),
    url(r'^movie/popular/(?P<page>[0-9]+)/$', views.popular_movie, name='popular_movie'),
    url(r'^movie/upcoming/(?P<page>[0-9]+)/$', views.upcoming_movie, name='upcoming_movie'),
    url(r'^tv/home/$', views.home_tv, name='home_tv'),
    url(r'^tv/popular/(?P<page>[0-9]+)/$', views.popular_tv, name='popular_tv'),
    url(r'^tv/details/(?P<id>[0-9]+)/$', views.details_tv, name='details_tv'),
    url(r'^tv/details/(?P<id>[0-9]+)/season/(?P<season>[0-9]+)$', views.details_season_tv, name='details_tv_season'),
    url(r'^page-not-found/', views.page_not_found, name='page_not_found'),
    url(r'^page-error/', views.page_error, name='page_error'),
    url(r'^movies/downloadable/', views.donwload_movie_content, name='donwload_movie_content'),
    url(r'^tv/downloadable/', views.downloable_tv_content, name='donwload_tv_content')
]