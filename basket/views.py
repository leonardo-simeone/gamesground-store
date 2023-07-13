from django.shortcuts import render


def basket_summary(request):
    """
    A view to render the basket content page
    """

    return render(request, 'basket/basket.html')
