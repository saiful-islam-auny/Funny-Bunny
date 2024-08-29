from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileUpdateView, UserProfileView, activate,CustomPasswordChangeView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update_profile/', UserProfileUpdateView.as_view(), name='update_profile'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
     path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
