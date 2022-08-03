from django.contrib import admin

# Register your models here.
from .models import Srtgen , Favourites


admin.site.register(Srtgen)
admin.site.register(Favourites)