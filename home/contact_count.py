from .models import Contact


def contacts_count_context(request):
    contacts_count = Contact.objects.count()
    return {'contacts_count': contacts_count}
