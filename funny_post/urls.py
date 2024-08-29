from django.urls import path
from .views import home, submit_joke, edit_joke, delete_joke, like_joke, share_joke, add_comment, add_rating, user_profile,leaderboard

urlpatterns = [
    # path('', home, name='home'),
    path('submit/', submit_joke, name='submit_joke'),
    path('edit/<int:joke_id>/', edit_joke, name='edit_joke'),
    path('delete/<int:joke_id>/', delete_joke, name='delete_joke'),
    path('like/<int:joke_id>/', like_joke, name='like_joke'),
    path('share/<int:joke_id>/', share_joke, name='share_joke'),
    path('comment/<int:joke_id>/', add_comment, name='add_comment'),
    path('rating/<int:joke_id>/', add_rating, name='add_rating'),
    path('user_profile/', user_profile, name='profile'),
     path('leaderboard/', leaderboard, name='leaderboard'),
]
