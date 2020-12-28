import html2text
import base64
import hashlib

from .forms import InitPasswordForm, InitPasswordErrorList

from django.core.mail import send_mail
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.db.models import Q

from django.utils.translation import ugettext_lazy as _
# Create your views here.

def init_password(request):
    global username_encrypt
    #form = InitPasswordForm(request.GET, error_class=InitPasswordErrorList)
    message = None
    success = False
    if request.method == 'POST':
        username_decrypt = base64.b64decode(request.POST['username_encrypt'].encode('ascii')).decode('ascii')

        if request.POST['password'] == request.POST['confirmPassword']:
            account = BhAccount.objects.get(username=username_decrypt)
            if account != None:
                account.password = hashlib.sha1(request.POST['password'].encode('utf-8')).hexdigest()
                account.save()
                success = True
                message = _('The password updated with success')

        else:
            success = False
            message = _('The password is not conform')

        username_encrypt = request.POST['username_encrypt']
    elif request.method == 'GET':
        username_encrypt = request.GET['u']

    context = {
        'username_encrypt': username_encrypt,
        'success': success,
        'message': message
    }
    return render(request, 'init-password.html', context)

#Methode for return data
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

#Service for API

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
            return Response(get_api_response(status.HTTP_201_CREATED, _("Account created with success !"), serializer.data))
        return Response(get_api_response(status.HTTP_208_ALREADY_REPORTED, _("This account already exist !"), serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def account_details(request, id):
    try:
        account = BhAccount.objects.get(pk=id)
    except BhAccount.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("Account not found"), None))

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
            return Response(get_api_response(status.HTTP_200_OK, _("Account updated with success"), serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, None, serializer.errors))

    elif request.method == 'DELETE':
        account.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Account deleted with success"), None))

@api_view(['GET'],)
def account_by_id_and_password(request, id, password):
    try:
        password_crypt = hashlib.sha1(password.encode('utf-8')).hexdigest()
        account = BhAccount.objects.get(pk=id, password=password_crypt)
    except BhAccount.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("Account not found"), None))

    serializer = AccountSerializer(account)
    if serializer.data != None:
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    else:
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, "No Content", serializer.errors))

@api_view(['PUT'],)
def account_change_password(request, id):
    try:
        account = BhAccount.objects.get(pk=id)

        password_crypt = hashlib.sha1(request.data['password'].encode('utf-8')).hexdigest()
        request.data['password'] = password_crypt

        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_200_OK, _("Password changed"), serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, None, serializer.errors))
    except BhAccount.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("Account not found"), None))

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

    try:
        data = BhAccount.objects.get(username=username, password=password)
        data.last_login = datetime.now()
        data.save()
        serializer = AccountSerializer(data)
        return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
    except IndexError:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("Username or password incorrect"), None))
    except BhAccount.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("Username or password incorrect"), None))

@api_view(['GET'])
def send_mail_for_init_password(request):
    h = html2text.HTML2Text()
    h.ignore_links = True
    try:
        user = BhUser.objects.get(email = request.GET.get('mail'))
    except BhUser.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("This email does not belong to a user"), None))
    #print(settings.EMAIL_HOST_USER)
    if user != None:
        account = BhAccount.objects.get(id = user.account_id)

        username_encrypt = base64.b64encode(account.username.encode('ascii')).decode('ascii')

        init_link = "http://lechatonguniverse.herokuapp.com/en/beakhub/accounts/init/password?u="+ username_encrypt
        message = "<b>BeakHub</b>" \
                  "<br/>" \
                  "<p>Hello<b>" + account.username + "</b>,</p>"\
                  "<p>Click on this link for init your password :</p>" + init_link + "" \
                  "<p>BeakHub Team</p>"

        send_mail(
            _('Password renewal'),
            h.handle(message),
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=True,
        )

        return Response(get_api_response(status.HTTP_200_OK, _("Email has been sended with succes"), message))
    else:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("This email does not belong to a user"), None))

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
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("User not found"), None))

    if request.method == 'GET':
        serializer = UserSerializer(user)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Error Encoured"), serializer.errors))

    elif request.method == 'PUT':
        try:
            IMG = request.FILES['profile_picture']
        except MultiValueDictKeyError:
            IMG = None
        user.profile_picture = IMG
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_200_OK, _("User updated with success"),serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, _("Error Encoured"), serializer.errors))

    elif request.method == 'DELETE':
        user.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("User deleted with success"), None))

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
            return Response(get_api_response(status.HTTP_201_CREATED, _("Job created with success"), serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, _("Error Encored"), serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def job_details(request, id):
    try:
        job = BhJob.objects.get(pk=id)
    except BhJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("Job not found"), None))

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
            return Response(get_api_response(status.HTTP_200_OK, _("Job updated with success"), serializer.data))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        job.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Job deleted with success"), None))

@api_view(['GET'],)
def jobs_by_user(request, user_id):
    jobs = BhJob.objects.filter(user_id = user_id)
    serializer = JobSerializer(jobs, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET'],)
def jobs_by_category(request, category_id):
    jobs = BhJob.objects.filter(category_id=category_id)
    serializer = JobSerializer(jobs, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET'],)
def jobs_fav_by_user(request, user_id):
    jobs = BhJob.objects.filter(bhuserlikejob__user_id=user_id)
    serializer = JobSerializer(jobs, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET'],)
def jobs_most_sollicited(request):
    jobs = BhJob.objects.raw('SELECT job.*, '
                             '(SELECT count(fav.id) FROM beakhub_bhuserlikejob as fav where fav.job_id = job.id) AS NB_FAV,'
                             '(SELECT count(cm.id) FROM beakhub_bhcomment as cm where cm.job_id = job.id) AS NB_CM  '
                             'FROM beakhub_bhjob as job ORDER BY NB_FAV DESC, NB_CM DESC')
    serializer = JobSerializer(jobs, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET'],)
def jobs_comment_by_user(request, user_id):
    jobs = BhJob.objects.filter(bhcomment__user__account_id= user_id)
    serializer = JobSerializer(jobs, many=True)
    return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))

@api_view(['GET'],)
def search_job(request):
    search = request.GET.get('query')
    jobs = BhJob.objects.filter(Q(title__icontains=search) | Q(description__icontains=search) |
                                Q(user__account__username__icontains=search) | Q(user__first_name__icontains=search) |
                                Q(user__last_name__icontains=search) | Q(category__title__icontains=search), is_active=True)

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
            return Response(get_api_response(status.HTTP_201_CREATED, _("The address added with success"), serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, _("Bad Request"), serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def address_details(request, id):
    try:
        address = BhAddress.objects.get(pk=id)
    except BhAddress.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("Address not found"), None))

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Error Encoured"), serializer.errors))

    elif request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, _("Error Encoured"), serializer.errors))

    elif request.method == 'DELETE':
        address.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Address deleted with success"), None))

@api_view(['GET'],)
def address_by_job(request, job_id):
    address = BhAddress.objects.filter(job_id = job_id)
    serializer = AddressSerializer(address, many=True)
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
        return Response(get_api_response(status.HTTP_201_CREATED, _("The comment added with success"), serializer.data))
    return Response(get_api_response(status.HTTP_400_BAD_REQUEST, _("Bad Request"), serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def comment_id(request, id):
    try:
        comment = BhComment.objects.get(pk=id)
    except BhComment.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("Comment not found"), None))

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Error Encoured"), serializer.errors))

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, _("Error Encoured"), serializer.errors))

    elif request.method == 'DELETE':
        comment.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Comment deleted with success"), None))

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
            return Response(get_api_response(status.HTTP_201_CREATED, _("The like created with success"), serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, _("Bad Request"), serializer.errors))

@api_view(['PUT','DELETE', 'GET'],)
def like_detail(request, like_id):
    try:
        like_job = BhUserLikeJob.objects.get(pk=like_id)
    except BhUserLikeJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("like not found"), None))

    if request.method == 'GET':
        serializer = BhUserLikeJobSerializer(like_job)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Error Encoured"), serializer.errors))

    elif request.method == 'PUT':
        serializer = BhUserLikeJobSerializer(like_job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(get_api_response(status.HTTP_200_OK, _("Like updated with success"),serializer.data))
        return Response(get_api_response(status.HTTP_400_BAD_REQUEST, _("Error Encoured"), serializer.errors))

    elif request.method == 'DELETE':
        like_job.delete()
        return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("like deleted with success"), None))

@api_view(['GET'],)
def like_job_user(request, job_id, user_id):
    try:
        like_job = BhUserLikeJob.objects.get(job_id=job_id, user_id=user_id)
        serializer = BhUserLikeJobSerializer(like_job)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Error Encoured"), serializer.errors))
    except BhUserLikeJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("like not found"), None))

@api_view(['GET'],)
def likes_job(request, job_id):
    try:
        like_job = BhUserLikeJob.objects.filter(job_id=job_id)
        serializer = BhUserLikeJobSerializer(like_job, many=True)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Error Encoured"), serializer.errors))
    except BhUserLikeJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("like not found"), None))

@api_view(['GET'],)
def likes_user(request, user_id):
    try:
        like_job = BhUserLikeJob.objects.filter(user_id=user_id)
        serializer = BhUserLikeJobSerializer(like_job, many=True)
        if serializer.data != None:
            return Response(get_api_response(status.HTTP_200_OK, None, serializer.data))
        else:
            return Response(get_api_response(status.HTTP_204_NO_CONTENT, _("Error Encoured"), serializer.errors))
    except BhUserLikeJob.DoesNotExist:
        return Response(get_api_response(status.HTTP_404_NOT_FOUND, _("like not found"), None))

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
def events_not_see_by_user(request, user_id):
    events = BhEvent.objects.filter(reciever_id = user_id, is_view=False).order_by('-created_at')
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
