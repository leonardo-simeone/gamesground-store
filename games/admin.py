from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'pegi_rating', 'available_in_other_consoles')


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Pegi)
class PegiAdmin(admin.ModelAdmin):
    list_display = ('age',)
