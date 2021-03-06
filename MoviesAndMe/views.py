from datetime import datetime

import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.translation import ugettext_lazy as _

from .forms import CommentForm
from lcu.models import comment as Comment
#from client import client

from lcu.models import movie_detail, tv_detail

language = settings.LANGUAGE_CODE
# Create your views here.

def change_language(request, lang):
    translation.activate(lang)
    print(translation.get_language())
    return redirect(home)

def home(request):
    #loop = asyncio.get_event_loop()
    #loop.create_task(channel_message())
    #print(client.get_me().stringify())
    # La liste des films les plus populaires
    response_top = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page=1')
    list_movie_on_top = response_top.json()
    RESULT_ON_TOP = list_movie_on_top['results']
    TOP_MOVIES_4 = []

    list_movie_new_add = movie_detail.objects.all().order_by('created_at')
    # La liste des tendances Hebdomadaires
    response_top_rated = requests.get('https://api.themoviedb.org/3/trending/movie/week?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page=1')

    list_movie_top_rated = response_top_rated.json()
    RESULT_TOP_RATED = list_movie_top_rated['results']
    TOP_MOVIES_6 = []

    # La liste des séries du moment
    response_top_tv = requests.get('https://api.themoviedb.org/3/tv/on_the_air?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page=1')

    list_tv_top = response_top_tv.json()
    RESULT_TOP_TV = list_tv_top['results']
    TOP_TVS_6 = []

    for j in (0,1,2,3):
        if RESULT_ON_TOP[j]['backdrop_path'] == None:
            pass
        else:
            TOP_MOVIES_4.append(
                [
                    RESULT_ON_TOP[j]['id'],
                    RESULT_ON_TOP[j]['title'],
                    RESULT_ON_TOP[j]['overview'],
                    RESULT_ON_TOP[j]['poster_path'],
                    RESULT_ON_TOP[j]['backdrop_path'],
                    datetime.strptime(RESULT_ON_TOP[j]['release_date'], "%Y-%m-%d").date(),
                    j
                ]
            )

    if len(list_movie_new_add) != 0:
        i = 0
        for link_movie in list_movie_new_add:
            i = i + 1
            response_movie = requests.get(
                'https://api.themoviedb.org/3/movie/' + str(link_movie.id_movie) + '?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '')
            movie = response_movie.json()
            #movie = movie_detail.objects.filter(id_movie=RESULT_TOP_RATED[i]['id']).exists();
            TOP_MOVIES_6.append(
                [
                    movie['id'],
                    movie['title'],
                    movie['overview'],
                    movie['poster_path'],
                    movie['backdrop_path'],
                    datetime.strptime(movie['release_date'], "%Y-%m-%d").date(),
                    movie['vote_average'],
                    movie,
                    link_movie.voice_language
                ]
            )

    for i in (0,1,2,3,4,5):
        tv = tv_detail.objects.filter(id_tv=RESULT_TOP_TV[i]['id']).exists();
        TOP_TVS_6.append(
            [
                RESULT_TOP_TV[i]['id'],
                RESULT_TOP_TV[i]['name'],
                RESULT_TOP_TV[i]['overview'],
                RESULT_TOP_TV[i]['poster_path'],
                RESULT_TOP_TV[i]['backdrop_path'],
                datetime.strptime(RESULT_TOP_TV[i]['first_air_date'], "%Y-%m-%d").date(),
                RESULT_TOP_TV[i]['vote_average'],
                tv
            ]
        )


    return render(request, 'index.html', locals())

def search_movies(request):
    search = request.GET.get('query')
    if search == '':
        return redirect(page_error)
    else:
        response_search = requests.get('https://api.themoviedb.org/3/search/multi?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&query='+search+'&&include_adult=false')
        list_movie_elt_search = response_search.json()

        RESULT_AFTER_SEARCH = []
        TOTAL_RESULT = []
        TOTAL_PAGE = []
        paginator = Paginator(list_movie_elt_search['results'], 15)
        page = request.GET.get('page')

        try:
            pagination = paginator.page(page)
        except PageNotAnInteger:
            pagination = paginator.page(1)
        except EmptyPage:
            pagination = paginator.page(paginator.num_pages)

        if pagination.object_list:
            for elt in pagination.object_list:
                if elt['media_type'] == 'movie':
                    try:
                        try:
                            movie = movie_detail.objects.filter(id_movie=elt['id']).exists();
                            RESULT_AFTER_SEARCH.append(
                                [
                                    elt['media_type'],
                                    elt['id'],
                                    elt['title'],
                                    elt['poster_path'],
                                    elt['overview'],
                                    elt['vote_average'],
                                    movie
                                ]
                            )
                        except ValueError:
                            pass
                    except KeyError:
                        pass
                else:
                    if elt['media_type'] == 'tv':
                        try:
                            try:
                                tv = tv_detail.objects.filter(id_tv=elt['id']).exists();
                                RESULT_AFTER_SEARCH.append(
                                    [
                                        elt['media_type'],
                                        elt['id'],
                                        elt['name'],
                                        elt['poster_path'],
                                        elt['overview'],
                                        elt['vote_average'],
                                        tv
                                    ]
                                )
                            except ValueError:
                                pass
                        except KeyError:
                            pass
                    else:
                        if elt['media_type'] == 'person':
                            RESULT_AFTER_SEARCH.append(
                                [
                                    elt['media_type'],
                                    elt['id'],
                                    elt['name'],
                                    elt['profile_path'],
                                ]
                            )
        else:
            return redirect(page_not_found)

        context = {
            'RESULT_AFTER_SEARCH':  RESULT_AFTER_SEARCH,
            'search':               search,
            'pagination':            pagination
        }
        return render(request, 'search_result.html', context)

def page_not_found(request):
    return render(request, 'page-not-found.html')

def page_error(request):
    return render(request, 'page_error.html')

def details_movie(request, id):
    message_return = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        NAME = None
        EMAIL = None
        MESSAGE = None
        try:
            NAME = request.POST['name_sender']
            MESSAGE = request.POST['message']
        except MultiValueDictKeyError:
            NAME = None
            EMAIL = None
            MESSAGE = None

        IS_REPLY = False
        try:
            COMMENT_PARENT_ID = request.POST['comment_parent_id']
            IS_REPLY = True
        except MultiValueDictKeyError:
            COMMENT_PARENT_ID = None
            IS_REPLY = False

        CREATED_AT = datetime.now()
        UPDATED_AT = datetime.now()

        comment = Comment(
            message=MESSAGE, email_sender=EMAIL, name_sender=NAME, is_delete=False, is_locked=False, is_reply=IS_REPLY,
            id_tv=None, comment_parent_id=COMMENT_PARENT_ID,
            member_id=None, id_movie=id, created_at = CREATED_AT, updated_at=UPDATED_AT
        )
        comment.save()
        message_return = _('enregistrement_effectue_avec_succes')
        try:
            if request.POST['save_in_browser']:
                request.session['NAME_USER']=NAME
                #request.session['EMAIL_USER'] = EMAIL

        except MultiValueDictKeyError:
            pass
        form = CommentForm
    else:
        form = CommentForm
    response_movie = requests.get('https://api.themoviedb.org/3/movie/'+id+'?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    movie = response_movie.json()

    response_actors = requests.get('https://api.themoviedb.org/3/movie/'+id+'/credits?api_key='+settings.API_KEY_MOVIE+'')
    list_actors = response_actors.json()
    LIST_ACTORS_CREDIT = []
    LIST_SIMILAR_MOVIES = []


    response_similar_movie = requests.get('https://api.themoviedb.org/3/movie/'+id+'/similar?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page=1')
    list_similar_movies = response_similar_movie.json()
    L_SIMILAR_MOVIES = list_similar_movies['results']
    b = len(list_similar_movies['results'])
    if b != 0:
        for i in (0, 1, 2, 3, 4, 5):
            movie_is_save = movie_detail.objects.filter(id_movie=L_SIMILAR_MOVIES[i]['id']).exists();
            if not L_SIMILAR_MOVIES[i]['id']:
                pass
            LIST_SIMILAR_MOVIES.append(
                [
                    L_SIMILAR_MOVIES[i]['id'],
                    L_SIMILAR_MOVIES[i]['title'],
                    L_SIMILAR_MOVIES[i]['poster_path'],
                    movie_is_save
                ]
            )
            if (b - 1) == i:
                break

    a = len(list_actors['cast'])
    LIST_ACTORS = list_actors['cast']
    if a > 5:
        for i in (0,1,2,3,4):
            LIST_ACTORS_CREDIT.append(
                [
                    LIST_ACTORS[i]['id'],
                    LIST_ACTORS[i]['name'],
                    LIST_ACTORS[i]['profile_path'],
                    LIST_ACTORS[i]['character'],
                ]
            )
    else:
        for elt in LIST_ACTORS:
            LIST_ACTORS_CREDIT.append(
                [
                    elt['id'],
                    elt['name'],
                    elt['profile_path'],
                    elt['character'],
                ]
            )

    M_DETAILS = []
    try:
        m_details = movie_detail.objects.filter(id_movie = id)
        if not m_details.exists():
            M_DETAILS = None
        else:
            for elt in m_details:
                M_DETAILS.append(
                    [
                        elt.id,
                        elt.voice_language,
                        elt.link_download,
                        elt.quality_video,
                        elt.quality_audio,
                        elt.subtitle,
                        elt.subtitle_language
                    ]
                )
    except movie_detail.DoesNotExist:
        m_details = None

    L_COMMENTS = []

    try:
        comments = Comment.objects.filter(id_movie = id, is_reply=False)
        if not comments.exists():
            L_COMMENTS = None
        else:
            for elt in comments:
                L_COMMENTS.append(
                    [
                        elt.id,
                        elt.message,
                        elt.name_sender,
                        elt.email_sender,
                        elt.created_at,
                        Comment.objects.filter(id_movie=id, is_reply=True, comment_parent_id=elt.id)
                    ]
                )
    except Comment.DoesNotExist:
        comments = None
    try:
        name_cookie = request.session['NAME_USER']
        email_cookie = request.session['EMAIL_USER']
    except KeyError :
        name_cookie = None
        email_cookie =  None

    response_videos = requests.get('https://api.themoviedb.org/3/movie/'+id+'/videos?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    list_video = response_videos.json()
    L_VIDEOS = list_video['results']
    VIDEOS = []
    if L_VIDEOS:
        for i in range(0, len(L_VIDEOS)-1):
            VIDEOS.append(
                [
                    L_VIDEOS[i]['key'],
                    L_VIDEOS[i]['name'],
                    L_VIDEOS[i]['site'],
                    L_VIDEOS[i]['type'],
                    i,
                    L_VIDEOS[i]['size'],
                ]
            )
    context = {
        'id':                   movie['id'],
        'title':                movie['title'],
        'original_title':       movie['original_title'],
        'overview':             movie['overview'],
        'poster_path':          movie['poster_path'],
        'backdrop_path':        movie['backdrop_path'],
        'release_date':         datetime.strptime(movie['release_date'], "%Y-%m-%d").date(),
        'vote_average':         movie['vote_average'],
        'homepage':             movie['homepage'],
        'production_companies': movie['production_companies'],
        'genres':               movie['genres'],
        'list_actor':           LIST_ACTORS_CREDIT,
        'LIST_SIMILAR_MOVIES':  LIST_SIMILAR_MOVIES,
        'VIDEOS':               VIDEOS,
        'COUNTEUR':             [1,2,3,4,5,6,7,8,9,10],
        'm_details':             M_DETAILS,
        'form':                 form,
        'comments':             L_COMMENTS,
        'message_return':       message_return,
        'name_cookie':          name_cookie,
        'email_cookie':         email_cookie,
    }
    return render(request, 'details_movie.html', context)

def details_actor(request, id):
    response_actor = requests.get(
        'https://api.themoviedb.org/3/person/' + id + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    actor = response_actor.json()

    response_actor_movies = requests.get(
        'https://api.themoviedb.org/3/person/'+ id + '/movie_credits?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    actor_movies = response_actor_movies.json()

    response_actor_tvs = requests.get(
        'https://api.themoviedb.org/3/person/'+ id + '/tv_credits?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    actor_tvs = response_actor_tvs.json()

    LIST_MOVIES_ACTOR = []
    LIST_TV_ACTOR = []
    L_MOVIES_ACTOR = actor_movies['cast']
    L_TV_ACTOR = actor_tvs['cast']

    a = len(actor_movies['cast'])
    b = len(actor_tvs['cast'])

    if a != 0:
        for i in (0, 1, 2, 3, 4):
            release_date = ''
            if not L_MOVIES_ACTOR[i]['id']:
                pass
            if 'release_date' in L_MOVIES_ACTOR[i]:
                if not L_MOVIES_ACTOR[i]['release_date']:
                    release_date = None
                else:
                    release_date = datetime.strptime(L_MOVIES_ACTOR[i]['release_date'], "%Y-%m-%d").date()
            else:
                pass
            movie_is_save = movie_detail.objects.filter(id_movie=L_MOVIES_ACTOR[i]['id']).exists();
            LIST_MOVIES_ACTOR.append(
                [
                    L_MOVIES_ACTOR[i]['id'],
                    L_MOVIES_ACTOR[i]['title'],
                    L_MOVIES_ACTOR[i]['poster_path'],
                    L_MOVIES_ACTOR[i]['character'],
                    L_MOVIES_ACTOR[i]['overview'],
                    release_date,
                    movie_is_save
                ]
            )
            if (a-1) == i:
                break

    if b != 0:
        for i in (0, 1, 2, 3, 4):
            if not L_TV_ACTOR[i]['id']:
                pass
            try:
                first_air_date = datetime.strptime(L_TV_ACTOR[i]['first_air_date'], "%Y-%m-%d").date()
            except ValueError:
                first_air_date = '...'
            tv = tv_detail.objects.filter(id_tv=L_TV_ACTOR[i]['id']).exists();
            LIST_TV_ACTOR.append(
                [
                    L_TV_ACTOR[i]['id'],
                    L_TV_ACTOR[i]['name'],
                    L_TV_ACTOR[i]['poster_path'],
                    L_TV_ACTOR[i]['character'],
                    L_TV_ACTOR[i]['overview'],
                    first_air_date,
                    tv
                ]
            )
            if (b-1) == i:
                break

    if actor['deathday'] != None:
        actor['deathday'] = datetime.strptime(actor['deathday'], "%Y-%m-%d").date()
    if actor['birthday'] != None:
        actor['birthday'] = datetime.strptime(actor['birthday'], "%Y-%m-%d").date()

    context = {
        'id':                   actor['id'],
        'name':                 actor['name'],
        'profile_path':         actor['profile_path'],
        'birthday':             actor['birthday'],
        'biography':            actor['biography'],
        'deathday':             actor['deathday'],
        'place_of_birth':       actor['place_of_birth'],
        'homepage':             actor['homepage'],
        'LIST_MOVIES_ACTOR':    LIST_MOVIES_ACTOR,
        'LIST_TV_ACTOR':        LIST_TV_ACTOR
    }
    return render(request, 'details_actor.html', context)

def movies_on_actor(request, id):
    response_actor = requests.get(
        'https://api.themoviedb.org/3/person/' + id + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    actor = response_actor.json()

    response_actor_movies = requests.get(
        'https://api.themoviedb.org/3/person/' + id + '/movie_credits?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    actor_movies = response_actor_movies.json()

    LIST_MOVIES_ACTOR = []
    L_MOVIES_ACTOR = actor_movies['cast']
    for elt in L_MOVIES_ACTOR:
        try:
            try:
                try:
                    release_date = datetime.strptime(elt['release_date'], "%Y-%m-%d").date()
                except KeyError:
                    release_date = None
            except ValueError:
                release_date = None
        except TypeError:
            release_date = None

        try:
            character = elt['character']
        except TypeError:
            character = None

        if elt['id'] == None or elt['title'] == None or not elt['character'] == None:
            pass
        movie_is_save = movie_detail.objects.filter(id_movie=elt['id']).exists();
        LIST_MOVIES_ACTOR.append(
            [
                elt['id'],
                elt['title'],
                elt['poster_path'],
                character,
                release_date,
                movie_is_save
            ]
        )
    context = {
        'id':                   actor['id'],
        'name':                 actor['name'],
        'profile_path':         actor['profile_path'],
        'LIST_MOVIES_ACTOR':    LIST_MOVIES_ACTOR
    }
    return render(request, 'movies_on_actor.html', context)

def tvs_on_actor(request, id):
    response_actor = requests.get(
        'https://api.themoviedb.org/3/person/' + id + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    actor = response_actor.json()

    response_actor_tvs = requests.get(
        'https://api.themoviedb.org/3/person/'+ id + '/tv_credits?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    actor_tvs = response_actor_tvs.json()

    LIST_TVS_ACTOR = []
    L_TVS_ACTOR = actor_tvs['cast']
    for elt in L_TVS_ACTOR:
        try:
            try:
                try:
                    first_air_date = datetime.strptime(elt['first_air_date'], "%Y-%m-%d").date()
                except KeyError:
                    first_air_date = None
            except ValueError:
                first_air_date = None
        except TypeError:
            first_air_date = None

        try:
            character = elt['character']
        except TypeError:
            character = None
        tv = tv_detail.objects.filter(id_tv=elt['id']).exists();
        LIST_TVS_ACTOR.append(
            [
                elt['id'],
                elt['name'],
                elt['poster_path'],
                character,
                elt['overview'],
                first_air_date,
                tv
            ]
        )
    context = {
        'id':                   actor['id'],
        'name':                 actor['name'],
        'profile_path':         actor['profile_path'],
        'LIST_TVS_ACTOR':       LIST_TVS_ACTOR
    }
    return render(request, 'tvs_on_actor.html', context)

def actors_on_movie(request, id):
    response_genre = requests.get(
        'https://api.themoviedb.org/3/genre/movie/list?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    list_genre = response_genre.json()
    LIST_GENDER = []
    for elt in list_genre['genres']:
        LIST_GENDER.append(
            [
                elt['id'],
                elt['name']
            ]
        )
    response_movie = requests.get(
        'https://api.themoviedb.org/3/movie/' + id + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    movie = response_movie.json()
    response_actors = requests.get(
        'https://api.themoviedb.org/3/movie/' + id + '/credits?api_key='+settings.API_KEY_MOVIE+'')
    list_actors = response_actors.json()
    LIST_ACTORS = list_actors['cast']
    LIST_ACTORS_CREDIT = []
    for elt in LIST_ACTORS:
        LIST_ACTORS_CREDIT.append(
            [
                elt['id'],
                elt['name'],
                elt['profile_path'],
                elt['character'],
            ]
        )
    context = {
        'id': movie['id'],
        'title': movie['title'],
        'original_title': movie['original_title'],
        'list_actor': LIST_ACTORS_CREDIT,
        'LIST_GENDER': LIST_GENDER,
    }
    return render(request, 'actors_on_movie.html', context)

def actors_on_tv(request, id):
    response_tv = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    tv = response_tv.json()
    response_actors = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '/credits?api_key='+settings.API_KEY_MOVIE+'')
    list_actors = response_actors.json()
    LIST_ACTORS = list_actors['cast']
    LIST_ACTORS_CREDIT = []
    for elt in LIST_ACTORS:
        LIST_ACTORS_CREDIT.append(
            [
                elt['id'],
                elt['name'],
                elt['profile_path'],
                elt['character'],
            ]
        )
    context = {
        'id': tv['id'],
        'title': tv['name'],
        'original_title': tv['original_name'],
        'list_actor': LIST_ACTORS_CREDIT,
    }
    return render(request, 'actors_on_tv.html', context)

def home_tv(request):
    # La liste des séries & animes les plus populaires du moment
    response_pop = requests.get(
        'https://api.themoviedb.org/3/tv/airing_today?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page=1')
    list_tv_pop = response_pop.json()
    RESULT_POPULAR_ON_TV = list_tv_pop['results']
    POPULAR_ON_TV = []

    for elt in RESULT_POPULAR_ON_TV:
        tv = tv_detail.objects.filter(id_tv=elt['id']).exists();
        POPULAR_ON_TV.append(
            [
                elt['id'],
                elt['name'],
                elt['overview'],
                elt['poster_path'],
                datetime.strptime(elt['first_air_date'], "%Y-%m-%d").date(),
                elt['vote_average'],
                tv,
            ]
        )

    context = {
        'POPULAR_ON_TV':    POPULAR_ON_TV,
    }
    return render(request, 'home_tv.html', context)

def popular_tv(request, page=1):
    # La liste des séries & animes les plus populaires du moment
    response_pop = requests.get(
        'https://api.themoviedb.org/3/tv/popular?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page='+page)
    list_tv_pop = response_pop.json()
    RESULT_POPULAR_ON_TV = list_tv_pop['results']
    TOTAL_PAGES = int(list_tv_pop['total_pages'])
    POPULAR_ON_TV = []
    COUNTER = []
    page = int(page)
    page_next = page + 1
    page_prev = page - 1

    for elt in RESULT_POPULAR_ON_TV:
        tv = tv_detail.objects.filter(id_tv=elt['id']).exists();
        POPULAR_ON_TV.append(
            [
                elt['id'],
                elt['name'],
                elt['overview'],
                elt['poster_path'],
                datetime.strptime(elt['first_air_date'], "%Y-%m-%d").date(),
                elt['vote_average'],
                tv
            ]
        )

    TOTAL_PAGES = TOTAL_PAGES - 1
    if page > 10:
        if page == TOTAL_PAGES:
            COUNTER = [page - 9, page - 8, page - 7, page - 6, page - 5, page - 4, page - 3, page - 2, page - 1, page]
        else:
            COUNTER = [page - 8, page - 7, page - 6, page - 5, page - 4, page - 3, page - 2, page - 1, page, page + 1]
    elif page == 10:
        COUNTER = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    elif page < 10:
        COUNTER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    context = {
        'page':             page,
        'POPULAR_ON_TV':    POPULAR_ON_TV,
        'TOTAL_PAGES':      TOTAL_PAGES,
        'COUNTER':          COUNTER,
        'page_next':        page_next,
        'page_prev':        page_prev
    }
    return render(request, 'popular_tv.html', context)

def home_movie(request):
    # La liste des séries & animes les plus récent du moment
    response_top = requests.get(
        'https://api.themoviedb.org/3/movie/now_playing?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page=1')
    list_movie_top = response_top.json()
    RESULT_TOP_MOVIES = list_movie_top['results']
    TOP_MOVIES = []

    for elt in RESULT_TOP_MOVIES:
        movie = movie_detail.objects.filter(id_movie=elt['id']).exists();
        TOP_MOVIES.append(
            [
                elt['id'],
                elt['title'],
                elt['overview'],
                elt['poster_path'],
                datetime.strptime(elt['release_date'], "%Y-%m-%d").date(),
                elt['vote_average'],
                movie,
            ]
        )

    context = {
        'TOP_MOVIES':   TOP_MOVIES,
    }
    return render(request, 'home_movie.html', context)

def popular_movie(request, page=1):
    # La liste des films les plus populaires du moment
    response_pop = requests.get(
        'https://api.themoviedb.org/3/movie/popular?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page='+page)
    list_movie_pop = response_pop.json()
    RESULT_POPULAR_MOVIES = list_movie_pop['results']
    TOTAL_PAGES = int(list_movie_pop['total_pages'])
    POPULAR_MOVIES = []
    COUNTER = []
    page = int(page)
    page_next = page + 1
    page_prev = page - 1
    for elt in RESULT_POPULAR_MOVIES:
        movie_is_save = movie_detail.objects.filter(id_movie=elt['id']).exists();
        POPULAR_MOVIES.append(
            [
                elt['id'],
                elt['title'],
                elt['overview'],
                elt['poster_path'],
                datetime.strptime(elt['release_date'], "%Y-%m-%d").date(),
                elt['vote_average'],
                movie_is_save
            ]
        )
    TOTAL_PAGES = TOTAL_PAGES - 1
    if page > 10:
        if page == TOTAL_PAGES:
            COUNTER = [page - 9, page - 8, page - 7, page - 6, page - 5, page - 4, page - 3, page - 2, page - 1, page]
        else:
            COUNTER = [page - 8, page - 7, page - 6, page - 5, page - 4, page - 3, page - 2, page - 1, page, page + 1]
    elif page == 10:
        COUNTER = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    elif page < 10:
        COUNTER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    context = {
        'page':             page,
        'POPULAR_MOVIES':   POPULAR_MOVIES,
        'TOTAL_PAGES':      TOTAL_PAGES,
        'COUNTER':          COUNTER,
        'page_next':        page_next,
        'page_prev':        page_prev
    }
    return render(request, 'popular_movie.html', context)

def upcoming_movie(request, page=1):
    # La liste des séries & animes les plus populaires du moment
    response_upcoming = requests.get(
        'https://api.themoviedb.org/3/movie/upcoming?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page='+page+'&region=FR')
    list_movie_upcoming = response_upcoming.json()
    RESULT_UPCOMING_MOVIES = list_movie_upcoming['results']
    TOTAL_PAGES = int(list_movie_upcoming['total_pages'])
    UPCOMING_MOVIES = []
    COUNTER = []
    page = int(page)
    page_next = page + 1
    page_prev = page - 1
    for elt in RESULT_UPCOMING_MOVIES:
        UPCOMING_MOVIES.append(
            [
                elt['id'],
                elt['title'],
                elt['overview'],
                elt['poster_path'],
                datetime.strptime(elt['release_date'], "%Y-%m-%d").date(),
                elt['vote_average'],
            ]
        )
    TOTAL_PAGES = TOTAL_PAGES - 1
    if page > 10:
        if page == TOTAL_PAGES:
            COUNTER = [page - 9, page - 8, page - 7, page - 6, page - 5, page - 4, page - 3, page - 2, page - 1, page]
        else:
            COUNTER = [page - 8, page - 7, page - 6, page - 5, page - 4, page - 3, page - 2, page - 1, page, page + 1]
    elif page == 10:
        COUNTER = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    elif page < 10:
        COUNTER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    context = {
        'page':             page,
        'UPCOMING_MOVIES':   UPCOMING_MOVIES,
        'TOTAL_PAGES':      TOTAL_PAGES,
        'COUNTER':          COUNTER,
        'page_next':        page_next,
        'page_prev':        page_prev
    }
    return render(request, 'upcoming_movie.html', context)

def details_tv(request, id):
    message_return = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        NAME = None
        EMAIL = None
        MESSAGE = None
        try:
            NAME = request.POST['name_sender']
            MESSAGE = request.POST['message']
        except MultiValueDictKeyError:
            NAME = None
            EMAIL = None
            MESSAGE = None

        IS_REPLY = False
        try:
            COMMENT_PARENT_ID = request.POST['comment_parent_id']
            IS_REPLY = True
        except MultiValueDictKeyError:
            COMMENT_PARENT_ID = None
            IS_REPLY = False

        CREATED_AT = datetime.now()
        UPDATED_AT = datetime.now()

        comment = Comment(
            message=MESSAGE, email_sender=EMAIL, name_sender=NAME, is_delete=False, is_locked=False, is_reply=IS_REPLY,
            id_tv=id, comment_parent_id=COMMENT_PARENT_ID,
            member_id=None, id_movie=None, created_at=CREATED_AT, updated_at=UPDATED_AT
        )
        comment.save()
        message_return = _('enregistrement_effectue_avec_succes')
        try:
            if request.POST['save_in_browser']:
                request.session['NAME_USER'] = NAME
                # request.session['EMAIL_USER'] = EMAIL

        except MultiValueDictKeyError:
            pass
        form = CommentForm
    else:
        form = CommentForm

    response_tv = requests.get(
        'https://api.themoviedb.org/3/tv/'+id+'?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    tv = response_tv.json()

    response_actors = requests.get(
        'https://api.themoviedb.org/3/tv/'+id+'/credits?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    list_actors = response_actors.json()

    LIST_ACTORS_CREDIT = []
    LIST_SIMILAR_TV = []

    a = len(list_actors['cast'])
    LIST_ACTORS = list_actors['cast']
    if a > 5:
        for i in (0, 1, 2, 3, 4):
            LIST_ACTORS_CREDIT.append(
                [
                    LIST_ACTORS[i]['id'],
                    LIST_ACTORS[i]['name'],
                    LIST_ACTORS[i]['profile_path'],
                    LIST_ACTORS[i]['character'],
                ]
            )
    else:
        for elt in LIST_ACTORS:
            LIST_ACTORS_CREDIT.append(
                [
                    elt['id'],
                    elt['name'],
                    elt['profile_path'],
                    elt['character'],
                ]
            )

    response_similar_tv = requests.get(
        'https://api.themoviedb.org/3/tv/'+id+'/similar?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'&page=1')
    list_similar_tv = response_similar_tv.json()
    L_SIMILAR_TV = list_similar_tv['results']
    b = len(list_similar_tv['results'])
    if b != 0:
        for i in (0, 1, 2, 3, 4, 5):
            tv_is_save = tv_detail.objects.filter(id_tv=L_SIMILAR_TV[i]['id']).exists();
            if not L_SIMILAR_TV[i]['id']:
                pass
            LIST_SIMILAR_TV.append(
                [
                    L_SIMILAR_TV[i]['id'],
                    L_SIMILAR_TV[i]['name'],
                    L_SIMILAR_TV[i]['poster_path'],
                    tv_is_save
                ]
            )
            if (b - 1) == i:
                break
    SEASONS = []
    AUTHORS = []
    for season in tv['seasons']:
        if season['season_number'] == 0:
            pass
        season_is_save = tv_detail.objects.filter(id_tv=tv['id'], nb_season=season['season_number']).exists();
        SEASONS.append(
            [
                season['id'],
                season['name'],
                season['poster_path'],
                season['season_number'],
                season_is_save
            ]
        )
    for author in tv['created_by']:
        AUTHORS.append(
            [
                author['id'],
                author['name'],
                author['credit_id']
            ]
        )
    try:
        fad = datetime.strptime(tv['first_air_date'], "%Y-%m-%d").date()
    except TypeError:
        fad = None

    L_COMMENTS = []

    try:
        comments = Comment.objects.filter(id_tv=id, is_reply=False)
        if not comments.exists():
            L_COMMENTS = None
        else:
            for elt in comments:
                L_COMMENTS.append(
                    [
                        elt.id,
                        elt.message,
                        elt.name_sender,
                        elt.email_sender,
                        elt.created_at,
                        Comment.objects.filter(id_tv=id, is_reply=True, comment_parent_id=elt.id)
                    ]
                )
    except Comment.DoesNotExist:
        comments = None
    try:
        name_cookie = request.session['NAME_USER']
        email_cookie = request.session['EMAIL_USER']
    except KeyError:
        name_cookie = None
        email_cookie = None
    response_videos = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '/videos?api_key=' + settings.API_KEY_MOVIE + '&language=' + translation.get_language() + '')
    list_video = response_videos.json()
    L_VIDEOS = list_video['results']
    VIDEOS = []
    if L_VIDEOS:
        for i in range(0, len(L_VIDEOS) - 1):
            VIDEOS.append(
                [
                    L_VIDEOS[i]['key'],
                    L_VIDEOS[i]['name'],
                    L_VIDEOS[i]['site'],
                    L_VIDEOS[i]['type'],
                    i,
                    L_VIDEOS[i]['size'],
                ]
            )
    context = {
        'id':                   tv['id'],
        'name':                 tv['name'],
        'backdrop_path':        tv['backdrop_path'],
        'homepage':             tv['homepage'],
        'overview':             tv['overview'],
        'vote_average':         tv['vote_average'],
        'genres':               tv['genres'],
        'created_by':           AUTHORS,
        'seasons':              SEASONS,
        'first_air_date':       fad,
        'number_of_episodes':   tv['number_of_episodes'],
        'number_of_seasons':    tv['number_of_seasons'],
        'production_companies': tv['production_companies'],
        'list_actor':           LIST_ACTORS_CREDIT,
        'LIST_SIMILAR_TV':      LIST_SIMILAR_TV,
        'VIDEOS':               VIDEOS,
        'COUNTEUR':             [1,2,3,4,5,6,7,8,9,10],
        'form':                 form,
        'comments':             L_COMMENTS,
        'message_return':       message_return,
        'name_cookie':          name_cookie,
        'email_cookie':         email_cookie,
    }
    return render(request, 'details_tv.html', context)

def details_season_tv(request, id, season):
    response_tv = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    tv = response_tv.json()

    response_season = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '/season/' + season + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
    saison = response_season.json()
    EPISODES = []
    for eps in saison['episodes']:
        TV_DETAILS = []
        t_detail = tv_detail.objects.filter(id_tv=id, nb_season=season, nb_episode=eps['episode_number'])
        if not t_detail.exists():
            TV_DETAILS = None
        else:
            for elt in t_detail:
                TV_DETAILS.append(
                    [
                        elt.id,
                        elt.voice_language,
                        elt.link_download,
                        elt.quality_video,
                        elt.quality_audio,
                        elt.subtitle,
                        elt.subtitle_language
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

    AIR_DATE = ""
    if saison['air_date']:
        saison['air_date'] = datetime.strptime(saison['air_date'], "%Y-%m-%d").date()

    context = {
        'id':               tv['id'],
        'name_tv':          tv['name'],
        'name_season':      saison['name'],
        'poster_path':      saison['poster_path'],
        'overview':         saison['overview'],
        'air_date':         saison['air_date'],
        'EPISODES':         EPISODES,
        'season_number':    saison['season_number'],
        'nb_episode':       len(EPISODES)
    }
    return render(request, 'details_tv_season.html', context)

def donwload_movie_content(request):
    if request.method == 'POST':
        search = request.POST['query']
        if search == '':
            movies = movie_detail.objects.all().order_by('title_movie', 'id_movie').distinct('title_movie')
        else:
            movies = movie_detail.objects.filter(title_movie__contains=search).order_by('title_movie', 'id_movie').distinct('title_movie')
    else:
        movies = movie_detail.objects.all().order_by('title_movie', 'id_movie').distinct('title_movie')
    list_movie = []
    for elt in movies:
        id = str(elt.id_movie)
        response_movie = requests.get(
            'https://api.themoviedb.org/3/movie/' + id + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
        movie = response_movie.json()

        try:
            overview = movie['overview']
            name = movie['title']
        except KeyError:
            overview = '...'
            name = '...'

        list_movie.append(
            [
                elt.id_movie,
                elt.link_download,
                elt.title_movie,
                overview,
                movie['poster_path'],
                movie['backdrop_path'],
                elt.subtitle,
                elt.subtitle_language,
                elt.voice_language
            ]
        )

    context = {
        'list_movie': list_movie,
        'nb_movie'  : len(list_movie),
        'descrption' : _(' films disponibles en téléchargement gratuit sur LeChatongUniverse')
    }
    return render(request, 'donwload_movie_content.html', context)

def downloable_tv_content(request):

    tvs = tv_detail.objects.all().order_by('id_tv', 'title_tv').distinct('id_tv')

    list_tvs = []
    for elt in tvs:
        id = str(elt.id_tv)
        response_tv = requests.get(
            'https://api.themoviedb.org/3/tv/' + id + '?api_key='+settings.API_KEY_MOVIE+'&language='+translation.get_language()+'')
        tv = response_tv.json()
        try:
            overview = tv['overview'],
            name = tv['name']
        except KeyError:
            overview = '...'
            name = '...'

        list_tvs.append(
            [
                elt.id_tv,
                elt.title_tv,
                overview,
                name,
                tv['poster_path'],
                tv['backdrop_path'],
                elt.subtitle,
                elt.subtitle_language,
                elt.voice_language
            ]
        )
    context = {
        'list_tvs': list_tvs,
        'nb_tv': len(list_tvs),
        'descrption': _(' Séries et animes disponibles en téléchargement gratuit sur LeChatongUniverse')
    }
    return render(request, 'download_tv_content.html', context)

