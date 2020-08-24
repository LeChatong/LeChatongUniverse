from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from . import views

urlpatterns = (
    url(r'^$', views.login),
    url(r'^login/$', views.authentification, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^search/$', views.search, name='search'),
    url(r'^list/movie/$', views.list_movie, name='list_movie'),
    url(r'^detail/movie/(?P<id>[0-9]+)/$', views.detail_movie, name='detail_movie'),
    url(r'^detail/movie/(?P<id>[0-9]+)/(?P<message>[a-z]+)/$', views.detail_movie, name='detail_movie'),
    url(r'^detail/tv/(?P<id>[0-9]+)/$', views.detail_tv_show, name='detail_tv'),
    url(r'^detail/tv/season/(?P<id>[0-9]+)/(?P<number_season>[0-9]+)/$', views.detail_season_tv_show, name='detail_season'),
    url(r'^add/tv/link/(?P<id_tv>[0-9]+)/(?P<number_season>[0-9]+)/$', views.add_link_tv_show, name='add_tv_link'),
    url(r'^edit/tv/link/(?P<id_tv>[0-9]+)/(?P<number_season>[0-9]+)/(?P<id>[0-9]+)/$', views.add_link_tv_show, name='edit_tv_link'),
    url(r'^add/tv/link/(?P<id_tv>[0-9]+)/(?P<number_season>[0-9]+)/(?P<message>[a-z]+)/$', views.add_link_tv_show, name='add_tv_link'),
    url(r'^add/tv/link/(?P<id_tv>[0-9]+)/(?P<number_season>[0-9]+)/(?P<id>[0-9]+)/(?P<message>[a-z]+)/$', views.add_link_tv_show, name='add_tv_link'),
    url(r'^save/link/tv/', views.save_link_tv, name='save_link_tv'),
    url(r'^add/movie/link/(?P<id_movie>[0-9]+)/$', views.add_link_movie, name='add_link_movie'),
    url(r'^edit/movie/(?P<id>[0-9]+)/$', views.modify_movie, name='edit_movie'),
    url(r'^delete/movie/$', views.delete_link_movie, name='delete_movie'),
    url(r'^save/movie/', views.save_movie, name='save_movie'),
    url(r'^logout', views.disconnect, name='logout')
)