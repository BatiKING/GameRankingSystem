from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=150, null=False, default='')
    pass


class Score(models.Model):
    p1_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='p1_id')
    p2_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='p2_id')
    p1_score = models.IntegerField(null=False)
    p2_score = models.IntegerField(null=False)
    p1_character = models.CharField(max_length=150)
    p2_character = models.CharField(max_length=150)
    date_time_created = models.DateTimeField(auto_now=True)


class PrivateScore(models.Model):
    score = models.OneToOneField(Score, on_delete=models.CASCADE, primary_key=True, default=1)
    game_title = models.CharField(max_length=150)
    game_mode = models.CharField(max_length=150)


class GameMode(models.Model):
    mode = models.CharField(max_length=150)


class GameTitle(models.Model):
    title = models.CharField(max_length=150)
    mode = models.ManyToManyField(GameMode)


class PublicScore(models.Model):
    score = models.OneToOneField(Score, on_delete=models.CASCADE, primary_key=True, default=1)
    game_title_id = models.ForeignKey(GameTitle, on_delete=models.CASCADE)
    game_mode_id = models.ForeignKey(GameMode, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_id')
    opponent_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opponent_id')
    score_confirmed = models.BooleanField()
