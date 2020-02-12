from django.conf.urls import url

from LeChApi import views, bot

urlpatterns = (
    url(r'^movies/$', views.list_all_movies_avaible),
    url(r'^auth/$', views.authentification),
    url(r'^user_data', views.user_data, name='user_data'),
    url(r'^bot', bot.main),
)