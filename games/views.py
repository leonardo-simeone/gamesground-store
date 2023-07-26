from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models import Count
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
    g = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                games = games.annotate(lower_name=Lower('name'))
            if sortkey == 'likes':
                sortkey = 'num_likes'
                games = games.annotate(num_likes=Count('likes'))
            if sortkey == 'platform':
                sortkey = 'platform__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            games = games.order_by(sortkey)

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
                return redirect(reverse('games'))
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(genre__icontains=query) | Q(platform__name__icontains=query)
            games = games.filter(queries)

    selected_sorting = f'{sort}_{direction}'

    context = {
        'games': games,
        'search_term': query,
        'selected_platforms': platforms,
        'selected_pegi': pegi_ratings,
        'g': g,
        'selected_sorting': selected_sorting,
    }

    return render(request, 'games/games.html', context)


# ----------------------------------------------------------------
def game_detail(request, game_id):
    """
    A view to show individual game details
    """

    game = get_object_or_404(Game, pk=game_id)
    liked = False

    if game.likes.filter(id=request.user.id).exists():
        liked = True

    context = {
        'game': game,
        'liked': liked,
    }

    return render(request, 'games/game_detail.html', context)


# ----------------------------------------------------------------
def like_game(request, game_id):
    """
    A view to control like/unlike games
    """

    game = get_object_or_404(Game, pk=game_id)
    liked = False

    if game.likes.filter(id=request.user.id).exists():
        game.likes.remove(request.user)
        liked = False
        messages.success(request, 'You have UNLIKED ' + game.name)
    else:
        game.likes.add(request.user)
        liked = True
        messages.success(request, 'You have LIKED ' + game.name)

    return redirect(game_detail, game_id)
