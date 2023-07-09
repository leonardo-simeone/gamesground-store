from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from embed_video.fields import EmbedVideoField

# Create your models here.


class Platform(models.Model):

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Pegi(models.Model):

    class Meta:
        verbose_name_plural = 'Pegi Rating'

    age = models.IntegerField()

    def __str__(self):
        return 'Ages ' + str(self.age) + ' and over'


class Game(models.Model):

    GENRE_OPTIONS = (
        ('Action', 'Action'), ('Adventure', 'Adventure'),
        ('Fantasy', 'Fantasy'), ('Horror', 'Horror'),
        ('Shooter', 'Shooter'), ('Racing', 'Racing'), ('Rpg', 'Rpg'),
        ('Sports', 'Sports'),
        )

    name = models.CharField(max_length=254)
    genre = MultiSelectField(max_length=120, choices=GENRE_OPTIONS, null=True, blank=True)
    description = models.TextField()
    year = models.CharField(max_length=4)
    platform = models.ForeignKey('Platform', null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    models.ImageField(null=True, blank=True, default='default-image')
    pegi_rating = models.ForeignKey('Pegi', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(null=True, blank=True)
    available_in_other_consoles = models.BooleanField(default=False, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='game_likes', blank=True)
    trailer = EmbedVideoField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name + ' ' + self.platform.name
