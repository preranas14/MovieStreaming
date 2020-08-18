from django.shortcuts import render

from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from movie.models import *
from django.http import HttpResponse
import json
import math
from .models import Comments
from movie.initializer import search_cache, search_index



@csrf_protect
def detail(request, model, id):
    items = []
    try:
        if model.get_name() == 'movie' and id != 'None':
            try:
                d = Popularity.objects.get(movieid_id=id)
                weight = d.weight
                d.delete()
                new_record = Popularity(movieid_id=id, weight=weight + 1)
                new_record.save()
            except:
                new_record = Popularity(movieid_id=id, weight=1)
                new_record.save()
            label = 'actor'
            object = model.objects.get(movieid=id)
            records = Act.objects.filter(movieid_id=id)
           
        
    except:
        return render(request, '404.html')
    return render(request, '{}_list.html'.format(label), {'items': items, 'number': len(items), 'object': object})


def whole_list(request, model, page):
    if page is None:
        return render(request, '404.html')
    page = int(page)
    objects = model.objects.all()
    total_page = int(math.ceil(len(objects) / 10))
    if page > total_page:
        return render(request, '404.html')
    last_item_index = 10 * page if page != total_page else len(objects)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
    end_page_num = page + 5 if page > 5 else 10
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    data = {'items': objects[10 * (page - 1):last_item_index], 'current_page': page, 'page_number': total_page,
            'pages': pages}
    return render(request, '{}_list.html'.format(model.get_name()), data)


def search(request, item, query_string, page):
    if item is None or query_string is None or page is None:
        return render(request, '404.html')
    query_string = query_string.replace("%20", " ")
    if item == 'movie':
        result = [search_index.data_in_memory['movie_dict'][movie_id] for movie_id in
                  search_index.search_movie(query_string)]
    else:
        return render(request, '404.html')
    page = int(page)
    total_page = int(math.ceil(len(result) / 10))
    if page > total_page and total_page != 0:
        return render(request, '404.html')
    last_item_index = 10 * page if page != total_page else len(result)
    pages = []
    end_distance = total_page - page
    start_page_num = page - 5 if end_distance >= 5 else page - 10 + end_distance
    end_page_num = page + 5 if page > 5 else 10
    for i in range(start_page_num, end_page_num + 1):
        if 1 <= i <= total_page:
            pages.append(i)
    return render(request, item + '_search.html',
                  {'items': result[10 * (page - 1):last_item_index], 'length': len(result),
                   'query_string': query_string, 'current_page': page, 'page_number': total_page, 'pages': pages})


def search_suggest(request, query_string):
    result = search_cache.get(query_string)
    if result is not None:
        return HttpResponse(json.dumps(result, ensure_ascii=False))
    movie_list, actor_list = [], []
    search_result = search_index.search_suggest(query_string)
    for i, movie_id in enumerate(search_result[0]):
        movie = search_index.data_in_memory['movie_dict'].get(movie_id)
        movie_list.append({'movieid': movie.movieid, 'poster': movie.poster, 'title': movie.title})
        if i == 2:
            break
    result = {'movie': movie_list, 'text': query_string}
    search_cache.set(query_string, result)
    return HttpResponse(json.dumps(result, ensure_ascii=False))

def post_detail(request, slug):
    template_name = 'actor_list.html'
    movie = get_object_or_404(Movie, slug=slug)
    comments = movie.comments.objects.filter(movie=post)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.movie = movie
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'movie': movie,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})



