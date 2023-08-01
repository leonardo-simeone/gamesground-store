from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
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

