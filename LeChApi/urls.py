from django.conf.urls import url

from LeChApi import views, bot

urlpatterns = (
    url(r'^movies/$', views.list_all_movies_avaible),
    url(r'^series/$', views.list_all_series_avaible),
    url(r'^search_movies/$', views.seach_movies),
    url(r'^search_series/$', views.seach_tvs),
    url(r'^auth/$', views.authentification),
    url(r'^user_data', views.user_data, name='user_data'),
)