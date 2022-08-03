import imp
from django.urls import path
from .views import *
urlpatterns = [
    path('uploadlink/', uploadlink, name='uploadlink'),
    path('preview/<int:srt_id>/',previewvideo,name="preview"),
    path('download/<str:driverFile>/',download_file2,name="downloadsrt"),
    path('search-results/<int:srt_id>/',search_results_view,name="search_results"),
    path("fav/<int:srt_id>/",fav,name="fav"),
    path("unfav/<int:srt_id>/",unfav,name="unfav"),
    path("downloadVideo/<int:obj>/<str:start>/<str:end>/",downloadVideo,name="downloadVideo"),
    path("srt/<int:srt_id>/", show_srt, name="show_srt")
]
