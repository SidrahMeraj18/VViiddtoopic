import imp
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path("search/<str:keyword>/", views.search_result, name="search_result")
]
