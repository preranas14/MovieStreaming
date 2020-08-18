from django.contrib import admin
from movie.models import *


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'movieid', 'rate')





admin.site.register(Movie, MovieAdmin)

admin.site.register(Comments)
