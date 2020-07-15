from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from . import views

urlpatterns = (
    url(r'^$', views.login),
    url(r'^login/$', views.authentification, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^list/movie/$', views.list_movie, name='list_movie'),
    url(r'^add/movie/', views.add_movie, name='add_movie'),
    url(r'^save/movie/', views.save_movie, name='save_movie'),
    url(r'^logout', views.disconnect, name='logout')
)