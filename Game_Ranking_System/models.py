from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=150, null=False, default='')
    pass


class GameMode(models.Model):
    mode = models.CharField(max_length=150)


class GameTitle(models.Model):
    title = models.CharField(max_length=150)
    mode = models.ManyToManyField(GameMode)


class Score(models.Model):
    p1_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_id')
    p2_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opponent_id')
    p1_score = models.IntegerField(null=False)
    p2_score = models.IntegerField(null=False)
    p1_character = models.CharField(max_length=150)
    p2_character = models.CharField(max_length=150)
    date_time_created = models.DateTimeField(auto_now=True)
    game_title_id = models.ForeignKey(GameTitle, on_delete=models.CASCADE)
    game_mode_id = models.ForeignKey(GameMode, on_delete=models.CASCADE)
    score_confirmed = models.BooleanField()
    public_score = models.BooleanField(default=False)


