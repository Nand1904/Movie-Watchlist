from django.db import models

# Create your models here.
class Watchlist(models.Model):
    username = models.CharField(max_length=100)
    movie_id = models.IntegerField()
    movie_title = models.CharField(max_length=100)
    release_date = models.DateField()
    adult = models.BooleanField()
    rating = models.FloatField()
    overview = models.CharField(max_length=500)
    movie_poster = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.username