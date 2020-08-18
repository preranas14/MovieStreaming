from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from movie.models import *
import operator
import random
from movie.initializer import search_index





@csrf_protect
def index(request):
    data = {}
    movie_dict = search_index.data_in_memory['movie_dict']
    if request.user.is_authenticated:
        data = {'username': request.user.get_username()}
    popular_movies = Popularity.objects.all().order_by('-weight')
    popular = []
    for movie in popular_movies[10:20]:
        try:
            popular.append({'movieid': movie.movieid_id, 'poster': movie_dict[movie.movieid_id].poster})
        except:
            continue
    data['popular'] = popular
    popular_movie_list = [movie_dict[movie.movieid_id] for movie in popular_movies[10:20]]
    return render(request, 'base.html', data)

