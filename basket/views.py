from django.shortcuts import render, redirect
from django.shortcuts import reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from games.models import *


# ----------------------------------------------------------------
def basket_summary(request):
    """
    A view to render the basket content page
    """

    return render(request, 'basket/basket.html')


# ----------------------------------------------------------------
def add_to_basket(request, game_id):
    """
    Add quantity of the specified game to the shopping basket
    """

    game = get_object_or_404(Game, pk=game_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if game_id in list(basket.keys()):
        basket[game_id] += quantity
    else:
        basket[game_id] = quantity

    if game.platform:
        messages.success(
            request, f'Added {game.name} {game.platform} to your basket'
            )
    else:
        messages.success(request, f'Added {game.name} to your basket')
    request.session['basket'] = basket
    return redirect(redirect_url)


# ----------------------------------------------------------------
def adjust_basket(request, game_id):
    """
    Adjust the quantity of the specified game to the specified amount
    """

    game = get_object_or_404(Game, pk=game_id)
    quantity = int(request.POST.get('quantity'))

    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[game_id] = quantity
        if game.platform:
            messages.success(
                request,
                f'Updated {game.name} {game.platform} quantity '
                f'to {basket[game_id]}'
                )
        else:
            messages.success(
                request,
                f'Updated {game.name} quantity to {basket[game_id]}')
    else:
        basket.pop(game_id)
        if game.platform:
            messages.success(
                request,
                f'Removed {game.name} {game.platform} from your basket'
                )
        else:
            messages.success(request, f'Removed {game.name} from your basket')

    request.session['basket'] = basket
    return redirect(reverse('basket_summary'))


# ----------------------------------------------------------------
def remove_from_basket(request, game_id):
    """
    Remove the game from the shopping basket
    """

    try:
        game = get_object_or_404(Game, pk=game_id)
        basket = request.session.get('basket', {})
        basket.pop(game_id)
        if game.platform:
            messages.success(
                request,
                f'Removed {game.name} {game.platform} from your basket'
                )
        else:
            messages.success(request, f'Removed {game.name} from your basket')

        request.session['basket'] = basket
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing game: {e}')
        return HttpResponse(status=500)
