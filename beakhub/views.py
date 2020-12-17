from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
import hashlib
# Create your views here.

def init_password(request):
    context = {}
    return render(request, 'init-password.html', context)

#View for API
def get_api_response(code, message, data):
    APIResponse.CODE = code
    APIResponse.MESSAGE = message
    APIResponse.DATA = data
    serializerAPI = APIResponseSerialiser(APIResponse)
    return serializerAPI.data

EVENT_TYPE = {
    'COMMENT',
    'LIKE',
    'VIEW'
}

@api_view(['GET','POST'],)
def account_list(request):
    if request.method == 'GET':
        accounts = BhAccount.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    elif request.method == 'POST':
        try:
            password_crypt = hashlib.sha1(request.data['password'].encode('utf-8')).hexdigest()
        except MultiValueDictKeyError:
            password_crypt = None
        request.data['password']= password_crypt
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_201_CREATED, "Account created with success !", serializer.data))
        return Response(get_api_response(status.HTTP_208_ALREADY_REPORTED, "This account already exist !", serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def account_details(request, id):
    try:
        account = BhAccount.objects.get(pk=id)
    except BhAccount.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "Account not found", None))

    if request.method == 'GET':
        #password_crypt = hashlib.sha1(account.password.encode('utf-8')).hexdigest()
        #account.password = password_crypt
        #account.save()

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
        password = hashlib.sha1(password_crypt.encode('utf-8')).hexdigest()

    data = BhAccount.objects.get(username=username, password=password)
    print(data)
    try:
        data.last_login = datetime.now()
        data.save()
        serializer = AccountSerializer(data)
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
            return Response(get_api_response(status.HTTP_201_CREATED, "User created with success", serializer.data))
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
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    elif request.method == 'POST':
        serializer = JobSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_201_CREATED, "Job created with success", serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Error Encored", serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def job_details(request, id):
    try:
        job = BhJob.objects.get(pk=id)
    except BhJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "Job not found", None))

    if request.method == 'GET':
        serializer = JobSerializer(job)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, None, serializer.errors))
    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_200_OK, "Job updated with success", serializer.data))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        job.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Job deleted with success", None))

@api_view(['GET'],)
def jobs_by_user(request, user_id):
    jobs = BhJob.objects.filter(user_id = user_id)
    serializer = JobSerializer(jobs, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET', 'POST'],)
def address_list(request):
    if request.method == 'GET':
        address = BhAddress.objects.all()
        serializer = AddressSerializer(address, many=True)
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    elif request.method == 'POST':
        serializer = AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_201_CREATED, "The address added with success", serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Bad Request", serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def address_details(request, id):
    try:
        address = BhAddress.objects.get(pk=id)
    except BhAddress.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "Address not found", None))

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Error Encoured", serializer.errors))

    elif request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Error Encoured", serializer.errors))

    elif request.method == 'DELETE':
        address.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Address deleted with success", None))

@api_view(['GET'],)
def address_by_job(request, job_id):
    address = BhAddress.objects.filter(job_id = job_id)
    serializer = AddressSerializer(address, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET'],)
def search_job(request):
    search = request.GET.get('query')
    jobs = BhJob.objects.filter(title__icontains=search, description__icontains=search)

    serializer = JobSerializer(jobs, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['POST'],)
def comment_add(request):
    serializer = CommentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        job = BhJob.objects.get(id = request.data['job_id'])
        user = BhUser.objects.get(account_id=request.data['user_id'])
        if job != None and user != None:
            if job.user.account_id != user.account_id:
                BhEvent(action='COMMENT', job_id=job.id, reciever_id=job.user.account_id, sender_id=user.account_id).save()
        serializer.save()
        return Response(get_api_response(status.HTTP_201_CREATED, "The comment added with success", serializer.data))
    return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Bad Request", serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def comment_id(request, id):
    try:
        comment = BhComment.objects.get(pk=id)
    except BhComment.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "Comment not found", None))

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Error Encoured", serializer.errors))

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Error Encoured", serializer.errors))

    elif request.method == 'DELETE':
        comment.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Comment deleted with success", None))

@api_view(['GET'],)
def comment_job_id(request, job_id):
    comment = BhComment.objects.filter(job_id=job_id)
    serializer = CommentSerializer(comment, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET', 'POST'],)
def like_all(request):
    if request.method == 'GET':
        userLikeJob = BhUserLikeJob.objects.all()
        serializer = BhUserLikeJobSerializer(userLikeJob, many=True)
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    elif request.method == 'POST':
        serializer = BhUserLikeJobSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            job = BhJob.objects.get(id=request.data['job_id'])
            user = BhUser.objects.get(account_id=request.data['user_id'])
            if job != None and user != None:
                if job.user.account_id != user.account_id:
                    BhEvent(action='LIKE', job_id=job.id, reciever_id=job.user.account_id,
                            sender_id=user.account_id).save()
            serializer.save()
            return Response(get_api_response(status.HTTP_201_CREATED, "The like created with success", serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Bad Request", serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def like_detail(request, like_id):
    try:
        like_job = BhUserLikeJob.objects.get(pk=like_id)
    except BhUserLikeJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "like not found", None))

    if request.method == 'GET':
        serializer = BhUserLikeJobSerializer(like_job)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Error Encoured", serializer.errors))

    elif request.method == 'PUT':
        serializer = BhUserLikeJobSerializer(like_job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_200_OK, "Like updated with success",serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, "Error Encoured", serializer.errors))

    elif request.method == 'DELETE':
        like_job.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, "like deleted with success", None))

@api_view(['GET'],)
def like_job_user(request, job_id, user_id):
    try:
        like_job = BhUserLikeJob.objects.get(job_id=job_id, user_id=user_id)
        serializer = BhUserLikeJobSerializer(like_job)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Error Encoured", serializer.errors))
    except BhUserLikeJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "like not found", None))

@api_view(['GET'],)
def likes_job(request, job_id):
    try:
        like_job = BhUserLikeJob.objects.filter(job_id=job_id)
        serializer = BhUserLikeJobSerializer(like_job, many=True)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Error Encoured", serializer.errors))
    except BhUserLikeJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "like not found", None))

@api_view(['GET'],)
def likes_user(request, user_id):
    try:
        like_job = BhUserLikeJob.objects.filter(user_id=user_id)
        serializer = BhUserLikeJobSerializer(like_job, many=True)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, "Error Encoured", serializer.errors))
    except BhUserLikeJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, "like not found", None))

@api_view(['GET'],)
def all_event(request):
    events = BhEvent.objects.all()
    serializer = BhEventSerializer(events, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET'],)
def events_by_user(request, user_id):
    events = BhEvent.objects.filter(reciever_id = user_id).order_by('-created_at')
    serializer = BhEventSerializer(events, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET'],)
def event_by_id(request, id):
    event = BhEvent.objects.get(id = id)
    serializer = BhEventSerializer(event)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['PUT'],)
def do_event_in_view(request, id):
    event = BhEvent.objects.get(id = id)
    event.is_view = True
    event.save()
    serializer = BhEventSerializer(event)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
