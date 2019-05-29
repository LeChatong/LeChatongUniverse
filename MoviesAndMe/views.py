from django.shortcuts import render
import requests
from datetime import datetime
from twython import Twython, TwythonError

# Create your views here.


def home(request):
    response_genre = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    list_genre = response_genre.json()
    LIST_GENDER = []
    for elt in list_genre['genres']:
        LIST_GENDER.append(
            [
                elt['id'],
                elt['name']
            ]
        )

    # La liste des films les plus populaires
    response_top = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')
    list_movie_on_top = response_top.json()
    PAGE = list_movie_on_top['page']
    TOTAL_PAGES = list_movie_on_top['total_pages']
    RESULT_ON_TOP = list_movie_on_top['results']
    TOP_MOVIES_4 = []

    # La liste des tendances Hebdomadaires
    response_top_rated = requests.get('https://api.themoviedb.org/3/trending/movie/week?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')

    list_movie_top_rated = response_top_rated.json()
    RESULT_TOP_RATED = list_movie_top_rated['results']
    TOP_MOVIES_6 = []

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

    return render(request, 'index.html', locals())

def search_movies(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        if search != None :
            response_search = requests.get('https://api.themoviedb.org/3/search/multi?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&query='+search+'&page=1&include_adult=false')
            list_movie_elt_search = response_search.json()
            RESULT_AFTER_SEARCH = []
            for elt in list_movie_elt_search['results']:
                if elt['media_type'] == 'movie':
                    RESULT_AFTER_SEARCH.append(
                        [
                            elt['media_type'],
                            elt['id'],
                            elt['title'],
                            elt['poster_path'],
                            elt['overview'],
                            elt['release_date'],
                            elt['vote_average'],
                        ]
                    )
                else :
                    if elt['media_type'] == 'tv':
                        RESULT_AFTER_SEARCH.append(
                            [
                                elt['media_type'],
                                elt['id'],
                                elt['name'],
                                elt['poster_path'],
                                elt['overview'],
                                elt['first_air_date'],
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

            return render(request, 'search_result.html', locals())
        else:
            return render(request, 'search_result.html', locals())
    else:
        return render(request, 'index.html', locals())

def details_movie(request, id):
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
    response_movie = requests.get('https://api.themoviedb.org/3/movie/'+id+'?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    movie = response_movie.json()

    response_actors = requests.get('https://api.themoviedb.org/3/movie/'+id+'/credits?api_key=f972c58efb26ab0a5e82cda1f7352586')
    list_actors = response_actors.json()
    LIST_ACTORS_CREDIT = []
    LIST_SIMILAR_MOVIES = []

    response_similar_movie = requests.get('https://api.themoviedb.org/3/movie/'+id+'/similar?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page=1')
    list_similar_movies = response_similar_movie.json()
    L_SIMILAR_MOVIES = list_similar_movies['results']

    for i in (0,1,2,3,4,5):
        LIST_SIMILAR_MOVIES.append(
            [
                L_SIMILAR_MOVIES[i]['id'],
                L_SIMILAR_MOVIES[i]['title'],
                L_SIMILAR_MOVIES[i]['poster_path']
            ]
        )

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
        'LIST_GENDER':          LIST_GENDER,
        'LIST_SIMILAR_MOVIES':  LIST_SIMILAR_MOVIES,
        'COUNTEUR':             [1,2,3,4,5,6,7,8,9,10]
    }
    return render(request, 'details_movie.html', context)

def details_actor(request, id):
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
    response_actor = requests.get('https://api.themoviedb.org/3/person/'+id+'?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor = response_actor.json()

    response_actor_movies = requests.get('https://api.themoviedb.org/3/person/'+id+'/movie_credits?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor_movies = response_actor_movies.json()

    LIST_MOVIES_ACTOR = []
    L_MOVIES_ACTOR = actor_movies['cast']
    for i in (0, 1, 2, 3, 4):
        LIST_MOVIES_ACTOR.append(
            [
                L_MOVIES_ACTOR[i]['id'],
                L_MOVIES_ACTOR[i]['title'],
                L_MOVIES_ACTOR[i]['poster_path'],
                L_MOVIES_ACTOR[i]['character'],
                L_MOVIES_ACTOR[i]['overview'],
                datetime.strptime(L_MOVIES_ACTOR[i]['release_date'], "%Y-%m-%d").date(),
            ]
        )
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
        'LIST_GENDER':          LIST_GENDER
    }
    return render(request, 'details_actor.html', context)

def movies_on_actor(request, id):
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
    response_actor = requests.get(
        'https://api.themoviedb.org/3/person/' + id + '?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor = response_actor.json()

    response_actor_movies = requests.get(
        'https://api.themoviedb.org/3/person/' + id + '/movie_credits?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    actor_movies = response_actor_movies.json()

    LIST_MOVIES_ACTOR = []
    L_MOVIES_ACTOR = actor_movies['cast']
    for elt in L_MOVIES_ACTOR:
        if elt['release_date'] != None:
            elt['release_date'] = datetime.strptime(elt['release_date'], "%Y-%m-%d").date()
        LIST_MOVIES_ACTOR.append(
            [
                elt['id'],
                elt['title'],
                elt['poster_path'],
                elt['character'],
                elt['overview'],
                elt['release_date'],
            ]
        )
    context = {
        'id':                   actor['id'],
        'name':                 actor['name'],
        'profile_path':         actor['profile_path'],
        'LIST_MOVIES_ACTOR':    LIST_MOVIES_ACTOR,
        'LIST_GENDER':          LIST_GENDER
    }
    return render(request, 'movies_on_actor.html', context)

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

def home_tv(request, page=1):
    response_genre = requests.get(
        'https://api.themoviedb.org/3/genre/tv/list?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR')
    list_genre = response_genre.json()
    LIST_GENDER = []
    for elt in list_genre['genres']:
        LIST_GENDER.append(
            [
                elt['id'],
                elt['name']
            ]
        )
    #page_next = page + 1
    #page_prev = page - 1
    # La liste des séries & animes les plus populaires du moment
    response_pop = requests.get(
        'https://api.themoviedb.org/3/tv/popular?api_key=f972c58efb26ab0a5e82cda1f7352586&language=fr-FR&page='+page)
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
        'page':             page,
        'LIST_GENDER':      LIST_GENDER,
        'POPULAR_ON_TV':    POPULAR_ON_TV
    }
    return render(request, 'home_tv.html', context)