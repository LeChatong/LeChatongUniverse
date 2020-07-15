from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import requests

# Create your views here.
from lcu.form import ConnexionForm, ConnectionError, MovieForm
from django.contrib.auth.models import User
from lcu.models import member as Member
from lcu.models import movie_detail as Movie
from lcu.models import tv_detail as Tv
from lcu.models import comment as Comment


def authentification(request):
    if request.method == "POST":
        form = ConnexionForm(request.POST, error_class=ConnectionError)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                message_success = _('message_success')
                context = {
                    'message_success': message_success
                }
                return redirect(dashboard)
            else:
                message_error = _('message_error')
    else:
        form = ConnexionForm()
    return render(request, 'authentification/login.html',locals())
def disconnect(request):
    logout(request)
    return redirect(reverse(authentification))

def dashboard(request):
    all_user = User.objects.all()
    all_member = Member.objects.all()
    all_movie = Movie.objects.all().order_by('id_movie').distinct('id_movie')
    all_tv_show = Tv.objects.all().order_by('id_tv').distinct('id_tv')
    all_eps_tv_show = Tv.objects.all()
    all_comment = Comment.objects.all()
    context = {
        'nb_user': len(all_user),
        'nb_member': len(all_member),
        'nb_movie': len(all_movie),
        'nb_tv_show': len(all_tv_show),
        'nb_eps_tv_show': len(all_eps_tv_show),
        'nb_comment': len(all_comment)
    }
    return render(request, 'dashboard/dashboard.html',context)

def init_all_movie():
    all_movie = Movie.objects.all()
    list_movies = []
    counting = 0
    for elt in all_movie:
        counting = counting + 1
        member = Member.objects.get(id=elt.member.id)
        list_movies.append(
            [
                counting,
                elt.id_movie,
                elt.title_movie,
                elt.link_download,
                elt.voice_language,
                elt.created_at,
                member.username
            ]
        )
    return list_movies


def list_movie(request):
    list_movies = init_all_movie()
    context = {
        'all_movie': list_movies,
    }
    return render(request, 'movies/list_movie.html', context)

def add_movie(request):
    form = MovieForm()
    return render(request, 'movies/edit_movie.html', locals())

def save_movie(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            try:
                movie = Movie()
                response_movie = requests.get(
                    'https://api.themoviedb.org/3/movie/' + request.POST['id_movie'] + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
                m = response_movie.json()

                title_movie     = m['title']
                id_movie        = request.POST['id_movie']
                link_download   = request.POST['link_download']
                language        = request.POST['language']
                quality         = request.POST['quality']

                movie.id_movie      = id_movie
                movie.title_movie   = title_movie
                movie.link_download = link_download
                movie.created_at    = timezone.now()
                movie.updated_at    = timezone.now()
                movie.member        = Member.objects.get(id = 1)
                if language == 'VF':
                    movie.voice_language    = 'FR'
                    movie.subtitle          = 'N'
                    movie.subtitle_language = 'N/A'
                elif language == 'VOSTFRJA':
                    movie.voice_language = 'JP'
                    movie.subtitle = 'Y'
                    movie.subtitle_language = 'FR'
                elif language == 'VOSTFREN':
                    movie.voice_language = 'EN'
                    movie.subtitle = 'Y'
                    movie.subtitle_language = 'FR'

                if quality == 'HIGH':
                    movie.quality_audio = 'GD'
                    movie.quality_video = 'GD'
                elif quality == 'MEDIUM':
                    movie.quality_audio = 'PASS'
                    movie.quality_video = 'PASS'
                elif quality == 'LOW':
                    movie.quality_audio = 'BAD'
                    movie.quality_video = 'BAD'
                movie.save()
                list_movies = init_all_movie()
                success_message = _('movie_save_with_success')
                context = {
                    'all_movie': list_movies,
                    'success_message': success_message
                }
                return render(request, 'movies/list_movie.html', context)
            except:
                redirect(add_movie)
        form = MovieForm()
        return render(request, 'movies/edit_movie.html', locals())