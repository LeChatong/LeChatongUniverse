from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import *

#FUNCTIONS FOR THE API BY TCHATONG ULRICH ARMEL

@api_view(['GET',])
def list_all_movies_avaible(request):
    data = movie_detail.objects.all()
    serializer = MovieSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET',])
def list_all_series_avaible(request):
    data = tv_detail.objects.all()
    serializer = SerieSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET',])
def seach_movies(request):
    search = request.GET.get('query')
    data = movie_detail.objects.filter(title_movie__contains=search).order_by('title_movie')
    serializer = MovieSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET',])
def seach_tvs(request):
    search = request.GET.get('query')
    data = tv_detail.objects.filter(title_tv__contains=search).order_by('title_tv')
    serializer = SerieSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

def authentification(request):
    return render(request, 'auth.html')

def user_data(resquest):
    if resquest.method == 'GET':
        id = resquest.POST['id']
        first_name = resquest.POST['first_name']
        last_name = resquest.POST['last_name']
        username = resquest.POST['username']
        photo_url = resquest.POST['photo_url']
        auth_date = resquest.POST['auth_date']
        hash = resquest.POST['hash']
        return render(resquest, 'user_data.html', locals())