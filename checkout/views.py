from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There's nothing in your basket at the moment")
        return redirect(reverse('games'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51NE8ZKKjooDQ9vmaZwJKrCUEorVr5NDlnzUVmStcjmYZK954czqVg43qrQTPDJEBekZbCQ5ctIVprNvgassN8eMQ00P7IeHVRY',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
