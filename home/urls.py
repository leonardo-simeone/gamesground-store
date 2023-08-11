from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('contact_list/', views.contact_list, name='contact_list'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('about_us/', views.about_us, name='about_us'),
]
