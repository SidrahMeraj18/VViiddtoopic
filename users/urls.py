import imp
from django.urls import path
from .views import *
urlpatterns = [
    path('auth/', display_view, name='auth'),
    path('logout/', logout_view, name='logout'),
    path('forgot-pass/', forgot_pass, name='forgot_pass'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/change-password/', change_password_view, name='change_password'),
    path('history/', history_view, name='history'),
    path('favourites/', favourites_view, name='favourites'),
]
