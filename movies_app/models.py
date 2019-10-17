from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)


class Genre(models.Model):
    name = models.CharField(max_length=32)


class Movie(models.Model):
    title = models.CharField(max_length=128)
    director = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='director_name')
    screenplay = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='screenplay_author')
    starring = models.ManyToManyField(Person, through="PersonMovie", related_name='role_in_movie')
    year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(1.0),MaxValueValidator(10.0)])
    genre = models.ManyToManyField(Genre, related_name='movie_genre')


class PersonMovie(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(null=True, max_length=128)




