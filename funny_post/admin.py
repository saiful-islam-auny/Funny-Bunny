from django.contrib import admin
from .models import Category, Joke, Like, Rating, Comment, SharedJoke
# Register your models here.
admin.site.register(Joke)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(SharedJoke)