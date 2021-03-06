"""OnlyMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth.models import User
from rest_framework import  routers, serializers, viewsets

from MoviesAndMe import views
from django.conf.urls.i18n import i18n_patterns

from OnlyMe import settings


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = i18n_patterns(

    url(r'^lechatong/', admin.site.urls),
    #url(r'^lechatongbot/', include('django_telegrambot.urls')),
    url(r'^', include('MoviesAndMe.urls')),
    url(r'^lechapi/', include('LeChApi.urls')),
    url(r'^beakhub/', include('beakhub.urls')),
    url(r'^lechatongram/', include('lcu.urls')),
    url(r'^api-authentification/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', views.home)
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
