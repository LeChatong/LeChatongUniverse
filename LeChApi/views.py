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
