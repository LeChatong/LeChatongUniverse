from datetime import datetime
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.utils.datastructures import MultiValueDictKeyError

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.utils import translation
import requests

# Create your views here.
from lcu.form import ConnexionForm, ConnectionError, MovieForm, TvForm, TvError
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
    all_movie = Movie.objects.all().order_by('title_movie').distinct('title_movie')
    list_movies = []
    counting = 0
    for elt in all_movie:
        counting = counting + 1

        list_movies.append(
            [
                counting,
                elt.id_movie,
                elt.title_movie,
                elt.id
            ]
        )
    return list_movies

def search(request):
    search = request.POST['search']
    response_search = requests.get(
        'https://api.themoviedb.org/3/search/multi?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '&query=' + search + '&&include_adult=false')
    list_elt_search = response_search.json()
    RESULT_AFTER_SEARCH = []
    for elt in list_elt_search['results']:
        if elt['media_type'] == 'person':
            pass
        else:
            title = ''
            if elt['media_type'] == 'movie':
                title = elt['title']
            elif elt['media_type'] == 'tv':
                title = elt['name']
            RESULT_AFTER_SEARCH.append(
                [
                    elt['media_type'],
                    elt['id'],
                    title,
                    elt['poster_path']
                ]
            )
    context = {
        'RESULT_AFTER_SEARCH': RESULT_AFTER_SEARCH,
        'search': search,
    }
    return render(request, 'search/search.html', context)

def detail_movie(request, id, message = None):
    response_movie = requests.get(
        'https://api.themoviedb.org/3/movie/' + id + '?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '')
    movie = response_movie.json()

    all_link_movie = Movie.objects.filter(id_movie=movie['id']).order_by('updated_at')
    list_link_movie = []
    counting = 0
    for elt in all_link_movie:
        counting = counting + 1
        member = Member.objects.get(id=elt.member.id)
        list_link_movie.append(
            [
                counting,
                elt.id_movie,
                elt.title_movie,
                elt.link_download,
                elt.voice_language,
                elt.created_at,
                member.username,
                elt.id
            ]
        )
    form = MovieForm()
    context = {
        'id'                : movie['id'],
        'title'             : movie['title'],
        'original_title'    : movie['original_title'],
        'overview'          : movie['overview'],
        'poster_path'       : movie['poster_path'],
        'release_date'      : datetime.strptime(movie['release_date'], "%Y-%m-%d").date(),
        'vote_average'      : movie['vote_average'],
        'list_link_movie'   : list_link_movie,
        'form'              : form,
        'message'           : message
    }
    return render(request, 'movies/detail_movie.html', context)

def detail_tv_show(request, id):
    response_tv = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '')
    tv = response_tv.json()
    SEASONS = []
    for season in tv['seasons']:
        SEASONS.append(
            [
                season['id'],
                season['name'],
                season['poster_path'],
                season['season_number']
            ]
        )
    try:
        fad = datetime.strptime(tv['first_air_date'], "%Y-%m-%d").date()
    except TypeError:
        fad = None

    context = {
        'id': tv['id'],
        'name': tv['name'],
        'original_name': tv['original_name'],
        'poster_path': tv['poster_path'],
        'homepage': tv['homepage'],
        'overview': tv['overview'],
        'vote_average': tv['vote_average'],
        'genres': tv['genres'],
        'seasons': SEASONS,
        'first_air_date': fad,
        'number_of_episodes': tv['number_of_episodes'],
        'number_of_seasons': tv['number_of_seasons'],
        'production_companies': tv['production_companies']
    }
    return render(request, 'tv_shows/detail_tv.html', context)

def detail_season_tv_show(request, id, number_season):
    response_tv = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '')
    tv = response_tv.json()

    response_season = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '/season/' + number_season + '?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '')
    saison = response_season.json()
    EPISODES = []
    if saison['air_date']:
        saison['air_date'] = datetime.strptime(saison['air_date'], "%Y-%m-%d").date()
    for eps in saison['episodes']:
        TV_DETAILS = []
        t_detail = Tv.objects.filter(id_tv=id, nb_season=number_season, nb_episode=eps['episode_number'])
        if not t_detail.exists():
            TV_DETAILS = None
        else:
            for elt in t_detail:
                member = Member.objects.get(id=elt.member.id)
                TV_DETAILS.append(
                    [
                        elt.id,
                        elt.voice_language,
                        elt.link_download,
                        elt.quality_video,
                        elt.quality_audio,
                        elt.subtitle,
                        elt.subtitle_language,
                        member.username,
                        elt.created_at,
                        elt.id_tv,
                        elt.nb_season
                    ]
                )

        EPISODES.append(
            [
                eps['id'],
                eps['name'],
                eps['air_date'],
                eps['episode_number'],
                eps['overview'],
                eps['still_path'],
                TV_DETAILS
            ]
        )
    context = {
        'id': tv['id'],
        'name_tv': tv['name'],
        'name_season': saison['name'],
        'poster_path': saison['poster_path'],
        'overview': saison['overview'],
        'air_date': saison['air_date'],
        'EPISODES': EPISODES,
        'season_number': saison['season_number'],
        'nb_episode': len(EPISODES)
    }
    return render(request, 'tv_shows/detail_season.html', context)

def add_link_tv_show(request, id_tv = None, number_season = None, id = None, message = None):
    response_tv = requests.get(
        'https://api.themoviedb.org/3/tv/' + id_tv + '?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '')
    tv = response_tv.json()
    name_tv = tv['name']

    response_season = requests.get(
        'https://api.themoviedb.org/3/tv/' + id_tv + '/season/' + number_season + '?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '')
    saison = response_season.json()
    name_season = saison['name']

    if id != None:
        tv = Tv.objects.get(id=id)

        LANGUAGE = ''
        QUALITY = ''
        if tv.voice_language == 'FR' and tv.subtitle == 'N' and tv.subtitle_language == 'N/A':
            LANGUAGE = 'VF'
        elif tv.voice_language == 'JP' and tv.subtitle == 'Y' and tv.subtitle_language == 'FR':
            LANGUAGE = 'VOSTFRJA'
        elif tv.voice_language == 'EN' and tv.subtitle == 'Y' and tv.subtitle_language == 'FR':
            LANGUAGE = 'VOSTFREN'

        if tv.quality_audio == 'GD' and tv.quality_video == 'GD':
            QUALITY = 'HIGH'
        elif tv.quality_audio == 'PASS' and tv.quality_video == 'PASS':
            QUALITY = 'MEDIUM'
        elif tv.quality_audio == 'BAD' and tv.quality_video == 'BAD':
            QUALITY = 'LOW'

        data = {
            'link_download': tv.link_download,
            'number_episode': tv.nb_episode,
            'quality': QUALITY,
            'language': LANGUAGE
        }
        form = TvForm(data)
    else:
        form = TvForm(request.POST, error_class=TvError)

    context = {
        'id_tv': id_tv,
        'id': id,
        'number_season': number_season,
        'name_tv': name_tv,
        'name_season': name_season,
        'message': message,
        'form': form
    }
    return  render(request, 'tv_shows/add_link_tv_show.html', context)

def edit_link_tv_show(request, id):
    tv = Tv.objects.get(id=id)

    LANGUAGE = ''
    QUALITY = ''
    if tv.voice_language == 'FR' and tv.subtitle == 'N' and tv.subtitle_language == 'N/A':
        LANGUAGE = 'VF'
    elif tv.voice_language == 'JP' and tv.subtitle == 'Y' and tv.subtitle_language == 'FR':
        LANGUAGE = 'VOSTFRJA'
    elif tv.voice_language == 'EN' and tv.subtitle == 'Y' and tv.subtitle_language == 'FR':
        LANGUAGE = 'VOSTFREN'

    if tv.quality_audio == 'GD' and tv.quality_video == 'GD':
        QUALITY = 'HIGH'
    elif tv.quality_audio == 'PASS' and tv.quality_video == 'PASS':
        QUALITY = 'MEDIUM'
    elif tv.quality_audio == 'BAD' and tv.quality_video == 'BAD':
        QUALITY = 'LOW'

    data = {
        'link_download': tv.link_download,
        'id_movie': tv.id_movie,
        'number_episode': tv.nb_episode,
        'quality': QUALITY,
        'language': LANGUAGE
    }
    form = TvForm(data)

    return render(request, 'tv_shows/add_link_tv_show.html', locals())

def save_link_tv(request):
    if request.method == "POST":
        form = TvForm(request.POST)
        if form.is_valid():
            try:
                try:
                    if request.POST['id']:
                        tv = Tv()
                    else:
                        tv = Tv.objects.get(id = request.POST['id'])
                except MultiValueDictKeyError:
                    tv = Tv()
                response_tv = requests.get(
                    'https://api.themoviedb.org/3/tv/' + request.POST['id_tv'] + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
                t = response_tv.json()

                title_tv        = t['name'] + ' saison ' + request.POST['number_season'] + ' episode ' + request.POST['number_episode']
                id_tv           = request.POST['id_tv']
                link_download   = request.POST['link_download']
                language        = request.POST['language']
                quality         = request.POST['quality']
                number_season   = request.POST['number_season']
                number_episode  = request.POST['number_episode']

                tv.id_tv            = id_tv
                tv.title_tv         = title_tv
                tv.link_download    = link_download
                tv.nb_episode       = number_episode
                tv.nb_season        = number_season
                tv.created_at       = timezone.now()
                tv.updated_at       = timezone.now()
                tv.member           = Member.objects.get(id = 1)
                if language == 'VF':
                    tv.voice_language    = 'FR'
                    tv.subtitle          = 'N'
                    tv.subtitle_language = 'N/A'
                elif language == 'VOSTFRJA':
                    tv.voice_language = 'JP'
                    tv.subtitle = 'Y'
                    tv.subtitle_language = 'FR'
                elif language == 'VOSTFREN':
                    tv.voice_language = 'EN'
                    tv.subtitle = 'Y'
                    tv.subtitle_language = 'FR'

                if quality == 'HIGH':
                    tv.quality_audio = 'GD'
                    tv.quality_video = 'GD'
                elif quality == 'MEDIUM':
                    tv.quality_audio = 'PASS'
                    tv.quality_video = 'PASS'
                elif quality == 'LOW':
                    tv.quality_audio = 'BAD'
                    tv.quality_video = 'BAD'
                tv.save()
                return redirect(add_link_tv_show, id_tv = id_tv, number_season = number_season, id = None, message = 'success')
            except:
                if request.POST['id']:
                    return redirect(add_link_tv_show, id_tv = request.POST['id_tv'],
                                    number_season = request.POST['number_season'], id = request.POST['id'], message = 'error')
                else:
                    return redirect(add_link_tv_show, id_tv=request.POST['id_tv'],
                                    number_season=request.POST['number_season'], id = None, message='error')

    return redirect(detail_season_tv_show, id_tv = request.POST['id_tv'], number_season=request.POST['number_season'])

def list_movie(request):
    list_movies = init_all_movie()
    context = {
        'all_movie': list_movies,
    }
    return render(request, 'movies/list_movie.html', context)

def add_link_movie(request, id_movie=None):
    form = MovieForm()
    context = {
        'id_movie'  : id_movie,
        'form'      : form
    }
    return render(request, 'movies/add_link_movie.html', context)

def modify_movie(request, id):
    movie = Movie.objects.get(id=id)


    LANGUAGE = ''
    QUALITY = ''
    if movie.voice_language == 'FR' and movie.subtitle == 'N' and movie.subtitle_language == 'N/A':
        LANGUAGE = 'VF'
    elif movie.voice_language == 'JP' and movie.subtitle == 'Y' and movie.subtitle_language == 'FR':
        LANGUAGE = 'VOSTFRJA'
    elif movie.voice_language == 'EN' and movie.subtitle == 'Y' and movie.subtitle_language == 'FR':
        LANGUAGE = 'VOSTFREN'

    if movie.quality_audio == 'GD' and movie.quality_video == 'GD':
        QUALITY = 'HIGH'
    elif movie.quality_audio == 'PASS' and movie.quality_video == 'PASS':
        QUALITY = 'MEDIUM'
    elif movie.quality_audio == 'BAD' and movie.quality_video == 'BAD':
        QUALITY = 'LOW'

    data = {
       'link_download' : movie.link_download,
        'id_movie': movie.id_movie,
        'quality' : QUALITY,
        'language': LANGUAGE
    }
    form = MovieForm(data)

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
                #message_success = _('link_save_with_success')
                return redirect(detail_movie,id=id_movie, message = 'success')
            except:
                redirect(detail_movie, id = request.POST['id_movie'], message = 'error')
    return redirect(detail_movie,id=request.POST['id_movie'])

def delete_link_movie(request):
    if request.method == "POST":
        id_movie = request.POST['id_movie']
        id = request.POST['id']
        try:
            movie = Movie.objects.get(id=id)
            if movie.delete():
                return redirect(detail_movie, id=id_movie, message='delete')
        except:
            movie = ''

class CreateLinkMovie(CreateView):
    model = Movie
    template_name = 'movies/detail_movie.html'

class DetailLinkMovie(DetailView):
    model = Movie
    template_name = 'movies/detail_movie.html'