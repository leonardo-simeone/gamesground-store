from django.shortcuts import render, redirect, reverse


def basket_summary(request):
    """
    A view to render the basket content page
    """

    return render(request, 'basket/basket.html')


def add_to_basket(request, game_id):
    """
    Add quantity of the specified game to the shopping basket
    """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if game_id in list(basket.keys()):
        basket[game_id] += quantity
    else:
        basket[game_id] = quantity

    request.session['basket'] = basket
    return redirect(redirect_url)


# ----------------------------------------------------------------
def adjust_basket(request, game_id):
    """Adjust the quantity of the specified game to the specified amount"""

    quantity = int(request.POST.get('quantity'))

    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[game_id] = quantity
    else:
        basket.pop(game_id)
    request.session['basket'] = basket
    return redirect(reverse('basket_summary'))
