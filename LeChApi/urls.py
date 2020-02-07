from django.conf.urls import url

from LeChApi import views

urlpatterns = (
    url(r'^movies/$', views.list_all_movies_avaible),
)