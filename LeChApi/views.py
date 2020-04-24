from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from .serializers import *
import hashlib

#FUNCTIONS FOR THE API BY TCHATONG ULRICH ARMEL

#Displays a user in accordance with their username and email
@api_view(['POST','GET'],)
def user_by_username_mail(request):
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['email']
    elif request.method == 'GET':
        username = request.GET.get('username')
        mail = request.GET.get('email')
    data = User.objects.filter(username=username, email=mail)
    serializer = UserSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

#List the user
@api_view(['GET',])
def list_all_user(request):
    data = User.objects.all()
    serializer = UserSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

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
    data = movie_detail.objects.filter(title_movie__icontains=search).order_by('title_movie')
    serializer = MovieSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET',])
def seach_tvs(request):
    search = request.GET.get('query')
    data = tv_detail.objects.filter(title_tv__icontains=search).distinct('id_tv').order_by('id_tv','title_tv')
    serializer = SerieSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['GET',])
def all_tv_episode(request):
    idTV = request.GET.get('id_tv')
    data = tv_detail.objects.filter(id_tv=idTV).order_by('title_tv')
    serializer = SerieSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(['POST', 'GET'])
def login_member(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password_crypt = hashlib.sha1(request.POST['password'].encode('utf-8')).hexdigest()
        except MultiValueDictKeyError:
            username = None
            password_crypt = None
        password = password_crypt
    elif request.method == 'GET':
        username = request.GET.get('username')
        try:
            password_crypt = hashlib.sha1(request.GET.get('password').encode('utf-8')).hexdigest()
        except MultiValueDictKeyError:
            password_crypt = None
        password = password_crypt
    data = member.objects.filter(username=username, password=password)
    serializer = MembeSerializer(data, context={'request': request}, many=True)
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