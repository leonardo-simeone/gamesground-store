from django.shortcuts import render, redirect, reverse
from .forms import ContactForm, NewsletterForm
from django.contrib import messages
from .models import Contact
from django.contrib.auth.decorators import login_required


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
    form = ContactForm(request.POST or None, user=request.user)

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


# --------------------------------------------------------------------------
@login_required
def contact_list(request):
    """
    A view for store owner/admin to list users
    that have contacted site owner/admin and
    their corresponding messages
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    contacts = Contact.objects.all()
    template = 'home/contact_list.html'
    context = {
        'contacts': contacts,
    }
    return render(request, template, context)


# --------------------------------------------------------------------------
def newsletter(request):
    """
    A view for users to subscribe to the site's newsletter
    """
    form = NewsletterForm(request.POST or None, user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Thanks for subscribing to our newsletter!'
                )
            return redirect('home')
        messages.error(request, 'An error has occurred. Please try again.')
    template = 'home/newsletter.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# --------------------------------------------------------------------------
def about_us(request):

    """
    The about_us function takes request as an argument
    and it renders the about_us template.
    """

    return render(request, 'home/about_us.html')
