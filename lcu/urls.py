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
    url(r'^add/movie/', views.add_movie, name='add_movie'),
    url(r'^edit/movie/(?P<id>[0-9]+)/$', views.modify_movie, name='edit_movie'),
    url(r'^save/movie/', views.save_movie, name='save_movie'),
    url(r'^logout', views.disconnect, name='logout')
)