from django.shortcuts import render, redirect
from django.http import Http404
import requests
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import movie_detail, tv_detail
from twython import Twython, TwythonError

# Create your views here.


def home(request):
    # La liste des films les plus populaires
    response_top = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')
    list_movie_on_top = response_top.json()
    RESULT_ON_TOP = list_movie_on_top['results']
    TOP_MOVIES_4 = []

    # La liste des tendances Hebdomadaires
    response_top_rated = requests.get('https://api.themoviedb.org/3/trending/movie/week?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')

    list_movie_top_rated = response_top_rated.json()
    RESULT_TOP_RATED = list_movie_top_rated['results']
    TOP_MOVIES_6 = []

    # La liste des séries du moment
    response_top_tv = requests.get('https://api.themoviedb.org/3/tv/on_the_air?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')

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

    for i in (0,1,2,3,4,5):
        TOP_MOVIES_6.append(
            [
                RESULT_TOP_RATED[i]['id'],
                RESULT_TOP_RATED[i]['title'],
                RESULT_TOP_RATED[i]['overview'],
                RESULT_TOP_RATED[i]['poster_path'],
                RESULT_TOP_RATED[i]['backdrop_path'],
                datetime.strptime(RESULT_TOP_RATED[i]['release_date'], "%Y-%m-%d").date(),
                RESULT_TOP_RATED[i]['vote_average']
            ]
        )

    for i in (0,1,2,3,4,5):
        TOP_TVS_6.append(
            [
                RESULT_TOP_TV[i]['id'],
                RESULT_TOP_TV[i]['name'],
                RESULT_TOP_TV[i]['overview'],
                RESULT_TOP_TV[i]['poster_path'],
                RESULT_TOP_TV[i]['backdrop_path'],
                datetime.strptime(RESULT_TOP_TV[i]['first_air_date'], "%Y-%m-%d").date(),
                RESULT_TOP_TV[i]['vote_average']
            ]
        )

    return render(request, 'index.html', locals())

def search_movies(request):
    search = request.GET.get('query')
    if search == '':
        return redirect(page_error)
    else:
        response_search = requests.get('https://api.themoviedb.org/3/search/multi?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&query='+search+'&&include_adult=false')
        list_movie_elt_search = response_search.json()

        RESULT_AFTER_SEARCH = []
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
                    RESULT_AFTER_SEARCH.append(
                        [
                            elt['media_type'],
                            elt['id'],
                            elt['title'],
                            elt['poster_path'],
                            elt['overview'],
                            elt['vote_average'],
                        ]
                    )
                else:
                    if elt['media_type'] == 'tv':
                        RESULT_AFTER_SEARCH.append(
                            [
                                elt['media_type'],
                                elt['id'],
                                elt['name'],
                                elt['poster_path'],
                                elt['overview'],
                                elt['vote_average'],
                            ]
                        )
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

    response_movie = requests.get('https://api.themoviedb.org/3/movie/'+id+'?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    movie = response_movie.json()

    response_actors = requests.get('https://api.themoviedb.org/3/movie/'+id+'/credits?api_key=f972c58efb26ab0a5e82cda1f7352586')
    list_actors = response_actors.json()
    LIST_ACTORS_CREDIT = []
    LIST_SIMILAR_MOVIES = []

    response_similar_movie = requests.get('https://api.themoviedb.org/3/movie/'+id+'/similar?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')
    list_similar_movies = response_similar_movie.json()
    L_SIMILAR_MOVIES = list_similar_movies['results']
    b = len(list_similar_movies['results'])
    if b != 0:
        for i in (0, 1, 2, 3, 4, 5):
            if not L_SIMILAR_MOVIES[i]['id']:
                pass
            LIST_SIMILAR_MOVIES.append(
                [
                    L_SIMILAR_MOVIES[i]['id'],
                    L_SIMILAR_MOVIES[i]['title'],
                    L_SIMILAR_MOVIES[i]['poster_path']
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
                        elt.link_telegram,
                        elt.quality_video,
                        elt.quality_audio,
                        elt.subtitle,
                        elt.subtitle_language
                    ]
                )
    except movie_detail.DoesNotExist:
        m_details = None

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
        'COUNTEUR':             [1,2,3,4,5,6,7,8,9,10],
        'm_details':             M_DETAILS
    }
    return render(request, 'details_movie.html', context)

def details_actor(request, id):
    response_actor = requests.get(
        'https://api.themoviedb.org/3/person/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor = response_actor.json()

    response_actor_movies = requests.get(
        'https://api.themoviedb.org/3/person/'+ id + '/movie_credits?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor_movies = response_actor_movies.json()

    response_actor_tvs = requests.get(
        'https://api.themoviedb.org/3/person/'+ id + '/tv_credits?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
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
            LIST_MOVIES_ACTOR.append(
                [
                    L_MOVIES_ACTOR[i]['id'],
                    L_MOVIES_ACTOR[i]['title'],
                    L_MOVIES_ACTOR[i]['poster_path'],
                    L_MOVIES_ACTOR[i]['character'],
                    L_MOVIES_ACTOR[i]['overview'],
                    release_date,
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
            LIST_TV_ACTOR.append(
                [
                    L_TV_ACTOR[i]['id'],
                    L_TV_ACTOR[i]['name'],
                    L_TV_ACTOR[i]['poster_path'],
                    L_TV_ACTOR[i]['character'],
                    L_TV_ACTOR[i]['overview'],
                    first_air_date,
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
        'https://api.themoviedb.org/3/person/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor = response_actor.json()

    response_actor_movies = requests.get(
        'https://api.themoviedb.org/3/person/' + id + '/movie_credits?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor_movies = response_actor_movies.json()

    LIST_MOVIES_ACTOR = []
    L_MOVIES_ACTOR = actor_movies['cast']
    for elt in L_MOVIES_ACTOR:
        try:
            try:
                release_date = datetime.strptime(elt['release_date'], "%Y-%m-%d").date()
            except ValueError:
                release_date = None
        except TypeError:
            release_date = None

        try:
            character = elt['character']
        except TypeError:
            character = None

        if elt['id'] == None or elt['title'] == None or not elt['character'] or elt['release_date'] == None:
            pass
        LIST_MOVIES_ACTOR.append(
            [
                elt['id'],
                elt['title'],
                elt['poster_path'],
                character,
                release_date
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
        'https://api.themoviedb.org/3/person/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor = response_actor.json()

    response_actor_tvs = requests.get(
        'https://api.themoviedb.org/3/person/'+ id + '/tv_credits?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor_tvs = response_actor_tvs.json()

    LIST_TVS_ACTOR = []
    L_TVS_ACTOR = actor_tvs['cast']
    for elt in L_TVS_ACTOR:
        try:
            try:
                first_air_date = datetime.strptime(elt['first_air_date'], "%Y-%m-%d").date()
            except ValueError:
                first_air_date = None
        except TypeError:
            first_air_date = None

        try:
            character = elt['character']
        except TypeError:
            character = None

        LIST_TVS_ACTOR.append(
            [
                elt['id'],
                elt['name'],
                elt['poster_path'],
                character,
                elt['overview'],
                first_air_date,
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
        'https://api.themoviedb.org/3/genre/movie/list?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
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
        'https://api.themoviedb.org/3/movie/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    movie = response_movie.json()
    response_actors = requests.get(
        'https://api.themoviedb.org/3/movie/' + id + '/credits?api_key=f972c58efb26ab0a5e82cda1f7352586')
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
        'https://api.themoviedb.org/3/tv/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    tv = response_tv.json()
    response_actors = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '/credits?api_key=f972c58efb26ab0a5e82cda1f7352586')
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
        'https://api.themoviedb.org/3/tv/airing_today?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')
    list_tv_pop = response_pop.json()
    RESULT_POPULAR_ON_TV = list_tv_pop['results']
    POPULAR_ON_TV = []

    for elt in RESULT_POPULAR_ON_TV:
        POPULAR_ON_TV.append(
            [
                elt['id'],
                elt['name'],
                elt['overview'],
                elt['poster_path'],
                datetime.strptime(elt['first_air_date'], "%Y-%m-%d").date(),
                elt['vote_average'],
            ]
        )

    context = {
        'POPULAR_ON_TV':    POPULAR_ON_TV,
    }
    return render(request, 'home_tv.html', context)

def popular_tv(request, page=1):
    # La liste des séries & animes les plus populaires du moment
    response_pop = requests.get(
        'https://api.themoviedb.org/3/tv/popular?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page='+page)
    list_tv_pop = response_pop.json()
    RESULT_POPULAR_ON_TV = list_tv_pop['results']
    TOTAL_PAGES = int(list_tv_pop['total_pages'])
    POPULAR_ON_TV = []
    COUNTER = []
    page = int(page)
    page_next = page + 1
    page_prev = page - 1

    for elt in RESULT_POPULAR_ON_TV:
        POPULAR_ON_TV.append(
            [
                elt['id'],
                elt['name'],
                elt['overview'],
                elt['poster_path'],
                datetime.strptime(elt['first_air_date'], "%Y-%m-%d").date(),
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
        'https://api.themoviedb.org/3/movie/now_playing?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')
    list_movie_top = response_top.json()
    RESULT_TOP_MOVIES = list_movie_top['results']
    TOP_MOVIES = []

    for elt in RESULT_TOP_MOVIES:
        TOP_MOVIES.append(
            [
                elt['id'],
                elt['title'],
                elt['overview'],
                elt['poster_path'],
                datetime.strptime(elt['release_date'], "%Y-%m-%d").date(),
                elt['vote_average'],
            ]
        )

    context = {
        'TOP_MOVIES':   TOP_MOVIES,
    }
    return render(request, 'home_movie.html', context)

def popular_movie(request, page=1):
    # La liste des films les plus populaires du moment
    response_pop = requests.get(
        'https://api.themoviedb.org/3/movie/popular?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page='+page)
    list_movie_pop = response_pop.json()
    RESULT_POPULAR_MOVIES = list_movie_pop['results']
    TOTAL_PAGES = int(list_movie_pop['total_pages'])
    POPULAR_MOVIES = []
    COUNTER = []
    page = int(page)
    page_next = page + 1
    page_prev = page - 1
    for elt in RESULT_POPULAR_MOVIES:
        POPULAR_MOVIES.append(
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
        'https://api.themoviedb.org/3/movie/upcoming?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page='+page+'&region=FR')
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
    response_tv = requests.get(
        'https://api.themoviedb.org/3/tv/'+id+'?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    tv = response_tv.json()

    response_actors = requests.get(
        'https://api.themoviedb.org/3/tv/'+id+'/credits?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
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
        'https://api.themoviedb.org/3/tv/'+id+'/similar?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-Fr&page=1')
    list_similar_tv = response_similar_tv.json()
    L_SIMILAR_TV = list_similar_tv['results']
    b = len(list_similar_tv['results'])
    if b != 0:
        for i in (0, 1, 2, 3, 4, 5):
            if not L_SIMILAR_TV[i]['id']:
                pass
            LIST_SIMILAR_TV.append(
                [
                    L_SIMILAR_TV[i]['id'],
                    L_SIMILAR_TV[i]['name'],
                    L_SIMILAR_TV[i]['poster_path']
                ]
            )
            if (b - 1) == i:
                break
    SEASONS = []
    AUTHORS = []
    for season in tv['seasons']:
        if season['season_number'] == 0:
            pass
        SEASONS.append(
            [
                season['id'],
                season['name'],
                season['poster_path'],
                season['season_number']
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
        'COUNTEUR':             [1,2,3,4,5,6,7,8,9,10]
    }
    return render(request, 'details_tv.html', context)

def details_season_tv(request, id, season):
    response_tv = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    tv = response_tv.json()

    response_season = requests.get(
        'https://api.themoviedb.org/3/tv/' + id + '/season/' + season + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
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
                        elt.link_telegram,
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
        'season_number':    saison['season_number']
    }
    return render(request, 'details_tv_season.html', context)

def donwload_movie_content(request):
    movies = movie_detail.objects.all().order_by('title_movie','id_movie').distinct('id_movie')
    list_movie = []
    for elt in movies:
        id = str(elt.id_movie)
        response_movie = requests.get(
            'https://api.themoviedb.org/3/movie/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
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
                elt.link_telegram,
                elt.title_movie,
                overview
            ]
        )

    context = {
        'list_movie': list_movie,
        'nb_movie'  : len(list_movie),
        'descrption' : ' films disponibles en téléchargement gratuit sur LeChatongUniverse'
    }
    return render(request, 'donwload_movie_content.html', context)

def downloable_tv_content(request):
    name_map = {'id_tv':'id'}
    tvs = tv_detail.objects.all().order_by('id_tv', 'title_tv').distinct('id_tv')
    #tvs = tv_detail.objects.raw('SELECT DISTINCT tv.id_tv, (SELECT COUNT( DISTINCT t.nb_season) FROM "MoviesAndMe_tv_detail" t WHERE t.id_tv = tv.id_tv) as nb_season, tv.title_tv FROM "MoviesAndMe_tv_detail" tv ORDER BY tv.title_tv', name_map)
    list_tvs = []
    for elt in tvs:
        id = str(elt.id_tv)
        response_tv = requests.get(
            'https://api.themoviedb.org/3/tv/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
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
                name
            ]
        )
    context = {
        'list_tvs': list_tvs,
        'nb_tv': len(list_tvs),
        'descrption': ' Séries et animes disponibles en téléchargement gratuit sur LeChatongUniverse'
    }
    return render(request, 'download_tv_content.html', context)