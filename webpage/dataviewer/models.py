from django.db import models

# Create your models here.

class Player(models.Model):
    timestamp = models.DateTimeField()
    gameID = models.PositiveIntegerField()
    charName = models.CharField(max_length=30)
    rank = models.PositiveSmallIntegerField()
    damage = models.PositiveSmallIntegerField()

class Games(models.Model):
    timestamp = models.CharField(max_length=30)  # this will be a datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
    gameID = models.PositiveIntegerField()
    player1 = models.CharField(max_length=30)
    player2 = models.CharField(max_length=30)
    player3 = models.CharField(max_length=30)
    player4 = models.CharField(max_length=30)
    player5 = models.CharField(max_length=30)
    player6 = models.CharField(max_length=30)
    player7 = models.CharField(max_length=30)
    player8 = models.CharField(max_length=30)