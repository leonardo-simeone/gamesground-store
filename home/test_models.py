from django.test import TestCase
from .models import *
from datetime import datetime


class TestContactModel(TestCase):

    """
    The setUp method is used to create a contact object.
    We have two test methods: test_contact_creation and test_contact_ordering.
    - In test_contact_creation, we check if a Contact object is created
    correctly and if all its fields are correctly saved. We also check
    if the created field is an instance of datetime.
    - In test_contact_ordering, we test if the contacts are ordered by the
    created field in ascending order, as specified in the Meta class.
    We create two contacts and verify their ordering in the queryset.
    """

    def setUp(self):
        self.contact = Contact.objects.create(
            name='Test User',
            email='test@example.com',
            body='This is a test message.'
        )

    def test_contact_creation(self):
        self.assertEqual(str(self.contact), 'Test User')
        self.assertEqual(self.contact.name, 'Test User')
        self.assertEqual(self.contact.email, 'test@example.com')
        self.assertEqual(self.contact.body, 'This is a test message.')
        self.assertIsInstance(self.contact.created, datetime)

    def test_contact_ordering(self):
        contact2 = Contact.objects.create(
            name='Another User',
            email='another@example.com',
            body='Another test message.'
        )
        contacts = Contact.objects.all()
        self.assertEqual(contacts[0], self.contact)
        self.assertEqual(contacts[1], contact2)


class TestNewsletterModel(TestCase):

    """
    The setUp method is used to create a newsletter subscriber object.
    We have three test methods: test_subscriber_creation,
    test_verbose_name_plural, and test_subscriber_ordering.
    - In test_subscriber_creation, we check if a Newsletter subscriber
    object is created correctly and if all its fields are correctly saved.
    We also check if the created field is an instance of datetime.
    - In test_verbose_name_plural, we verify that the verbose_name_plural
    attribute in the Meta class is set correctly.
    - In test_subscriber_ordering, we test if the subscribers are ordered by
    the created field in ascending order, as specified in the Meta class.
    We create two subscribers and verify their ordering in the queryset.
    """

    def setUp(self):
        self.subscriber = Newsletter.objects.create(
            name='Test Subscriber',
            email='test@example.com'
        )

    def test_subscriber_creation(self):
        self.assertEqual(str(self.subscriber), 'Test Subscriber')
        self.assertEqual(self.subscriber.name, 'Test Subscriber')
        self.assertEqual(self.subscriber.email, 'test@example.com')
        self.assertIsInstance(self.subscriber.created, datetime)

    def test_verbose_name_plural(self):
        self.assertEqual(
            str(Newsletter._meta.verbose_name_plural),
            'Newsletter subscribers'
            )

    def test_subscriber_ordering(self):
        subscriber2 = Newsletter.objects.create(
            name='Another Subscriber',
            email='another@example.com'
        )
        subscribers = Newsletter.objects.all()
        self.assertEqual(subscribers[0], self.subscriber)
        self.assertEqual(subscribers[1], subscriber2)
