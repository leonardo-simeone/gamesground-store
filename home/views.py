from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages


def index(request):
    """
    A view to render the home page
    """

    return render(request, 'home/index.html')


# --------------------------------------------------------------------------
def contact(request):
    """
    A view for users to contact the site admin
    """
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Thanks for contacting Gamesground!'
                )
            return redirect('home')
        messages.error(request, 'An error has occurred. Please try again.')
    template = 'home/contact.html'
    context = {
        'form': form,
    }
    return render(request, template, context)

