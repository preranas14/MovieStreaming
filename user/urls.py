from django.conf.urls import url
from . import views
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    url(r'^login/', views.user_login, name='login'),
    #url(r'^logout/', views.user_logout, name='logout'),
    url(r'^register/', views.user_register, name='register'),
    url(r'^logout/', views.user_logout, name='logout'),
    #path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),


    
]
