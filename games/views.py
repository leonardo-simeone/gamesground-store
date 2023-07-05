from django.shortcuts import render
from .models import *


def games(request):
    """
    A view to show all games, including sorting and search queries
    """

    games = Game.objects.all()

    context = {
        'games': games,
    }

    return render(request, 'games/games.html', context)
