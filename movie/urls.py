from django.conf.urls import url
from . import views
from . import models
from django.urls import path, include

urlpatterns = [
    url(r'^movie_all/(?P<page>\d*)', views.whole_list, {'model': models.Movie}, name='whole_list'),
    url(r'^movie_detail/(?P<id>.*)', views.detail, {'model': models.Movie}, name='movie_detail'),
    url(r'^search/(?P<item>.*)/(?P<query_string>.*)/(?P<page>\d*).*', views.search, name='search'),
    url(r'^search_suggest/(?P<query_string>.*)', views.search_suggest, name='search_suggest'),
    path('<slug:slug>/', views.post_detail, name='post_detail')

   

]
