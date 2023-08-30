from .models import Contact


def contacts_count_context(request):
    """
    A function to count the number of contact objects
    for contact model
    """
    contacts_count = Contact.objects.count()
    return {'contacts_count': contacts_count}
