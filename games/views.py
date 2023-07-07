from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import *


# ----------------------------------------------------------------
def games(request):
    """
    A view to show all games, including sorting and search queries
    """

    games = Game.objects.all()
    query = None
    platforms = None
    pegi_ratings = None
    genres = None

    if 'platform' in request.GET:
        platforms = request.GET['platform'].split(',')
        games = games.filter(platform__name__in=platforms)
        platforms = Platform.objects.filter(name__in=platforms)

    if 'pegi_rating' in request.GET:
        pegi_ratings = request.GET['pegi_rating'].split(',')
        games = games.filter(pegi_rating__age__in=pegi_ratings)
        pegi_ratings = Pegi.objects.filter(age__in=pegi_ratings)

    if 'genre' in request.GET:
        g = request.GET['genre']
        genre = Q(genre__icontains=g)            
        games = games.filter(genre)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'Opps! You need to write something in the search bar...')
                return redirect(reverse('home'))
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(genre__icontains=query) | Q(platform__name__icontains=query)
            games = games.filter(queries)

    context = {
        'games': games,
        'search_term': query,
    }

    return render(request, 'games/games.html', context)


# ----------------------------------------------------------------

def game_detail(request, game_id):
    """
    A view to show individual game details
    """

    game = get_object_or_404(Game, pk=game_id)

    context = {
        'game': game,
    }

    return render(request, 'games/game_detail.html', context)
