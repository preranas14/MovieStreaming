
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import render
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),

    url(r'^admin/', admin.site.urls),
    url(r'^movie/', include('movie.urls')),
    url(r'^user/', include('user.urls')),
    
    url(r'^$', views.index, name='index'),
    url(r'.*', lambda request: render(request, '404.html'), name='404'),
]
