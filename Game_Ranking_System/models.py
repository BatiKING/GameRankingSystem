from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Overriding standard User model in order to add a 'nickname' field"""

    nickname = models.CharField(max_length=150, null=False, default='', unique=True)
    pass

    def __unicode__(self):
        return self.nickname

    def __str__(self):
        return self.nickname


class GameMode(models.Model):
    """Model holding all used Game Modes and their visibility level"""

    mode = models.CharField(max_length=150)
    public_allowed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.mode

    def __str__(self):
        return self.mode


class GameTitle(models.Model):
    """Model holding all used Game Titles and their visibility level"""

    title = models.CharField(max_length=150)
    mode = models.ManyToManyField(GameMode)
    public_allowed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Score(models.Model):
    """Model storing the score data"""

    p1_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_id')
    p2_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opponent_id', null=True)
    p1_score = models.IntegerField(null=False)
    p2_score = models.IntegerField(null=False)
    p1_character = models.CharField(max_length=150)
    p2_character = models.CharField(max_length=150)
    date_time_created = models.DateTimeField(auto_now=True)
    game_title_id = models.ForeignKey(GameTitle, on_delete=models.CASCADE)
    game_mode_id = models.ForeignKey(GameMode, on_delete=models.CASCADE)
    score_confirmed = models.BooleanField(default=False)
    public_score = models.BooleanField(default=False)
    personal_opponent_nickname = models.CharField(max_length=150, null=True)
