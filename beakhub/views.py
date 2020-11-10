import json
from datetime import datetime

from django.shortcuts import render
import requests
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
# Create your views here.

def get_api_response(code, message, data):
    APIResponse.CODE = code
    APIResponse.MESSAGE = message
    APIResponse.DATA = data
    serializerAPI = APIResponseSerialiser(APIResponse)
    return serializerAPI.data

@api_view(['GET','POST'],)
def account_list(request):
    if request.method == 'GET':
        accounts = BhAccount.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    elif request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_201_CREATED, "Account create with success !", serializer.data))
        return Response(get_api_response(status.HTTP_208_ALREADY_REPORTED, "Error Encoured", serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def account_details(request, id):
    try:
        account = BhAccount.objects.get(pk=id)
    except BhAccount.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "Account not found", None))

    if request.method == 'GET':
        serializer = AccountSerializer(account)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, "No Content", serializer.errors))

    elif request.method == 'PUT':
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_200_OK, "Account updated with success",serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, None, serializer.errors))

    elif request.method == 'DELETE':
        account.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Account deleted with success", None))

@api_view(['GET', 'POST'],)
def account_login(request):
    global username, password
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password_crypt = request.POST['password']
        except MultiValueDictKeyError:
            username = None
            password_crypt = None
        password = password_crypt
    elif request.method == 'GET':
        username = request.GET.get('username')
        try:
            password_crypt = request.GET.get('password')
        except MultiValueDictKeyError:
            password_crypt = None
        password = password_crypt

    data = BhAccount.objects.filter(username=username, password=password)
    print(data)
    try:
        data[0].last_login = datetime.now()
        print(data[0])
        data[0].save()
        serializer = AccountSerializer(data, many=True)
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    except IndexError:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "Username or password incorrect", None))

@api_view(['GET', 'POST'],)
def user_list(request):
    if request.method == 'GET':
        users = BhUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_201_CREATED, "User create with success", serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Error Encoured", serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def user_details(request, id):
    try:
        user = BhUser.objects.get(pk=id)
    except BhUser.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "User not found", None))

    if request.method == 'GET':
        serializer = UserSerializer(user)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Error Encoured", serializer.errors))

    elif request.method == 'PUT':
        try:
            IMG = request.FILES['profile_picture']
        except MultiValueDictKeyError:
            IMG = None
        user.profile_picture = IMG
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_200_OK, "User updated with success",serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Error Encoured", serializer.errors))

    elif request.method == 'DELETE':
        user.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, "User deleted with success", None))

@api_view(['GET', 'POST'],)
def category_list(request):
    if request.method == 'GET':
        categories = BhCategory.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','DELETE', 'GET'],)
def category_details(request, id):
    try:
        category = BhCategory.objects.get(pk=id)
    except BhCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        if serializer.data != None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'],)
def job_list(request):
    if request.method == 'GET':
        jobs = BhJob.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print(request.data)
        serializer = JobSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','DELETE', 'GET'],)
def job_details(request, id):
    try:
        job = BhJob.objects.get(pk=id)
    except BhJob.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JobSerializer(job)
        if serializer.data != None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'],)
def jobs_by_user(request, user_id):
    jobs = BhJob.objects.filter(user_id = user_id)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'],)
def address_list(request):
    if request.method == 'GET':
        address = BhAddress.objects.all()
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print(request.data)
        serializer = AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','DELETE', 'GET'],)
def address_details(request, id):
    try:
        address = BhAddress.objects.get(pk=id)
    except BhAddress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        if serializer.data != None:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'],)
def address_by_job(request, job_id):
    address = BhAddress.objects.filter(job_id = job_id)
    serializer = AddressSerializer(address, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)