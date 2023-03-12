from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    starttime = models.DateTimeField(db_index=True)
    tickcount = models.IntegerField()
    tickinterval = models.DurationField()
    content = models.TextField()

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    tick = models.IntegerField(db_index=True)
    stage = models.IntegerField(db_index=True)
    submitTick = models.IntegerField(db_index=True)
    content = models.TextField()
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserToken(models.Model):
    token = models.TextField(unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class RoundScore(models.Model):
    round = models.IntegerField()
    rank = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    questionid = models.IntegerField()
    score = models.IntegerField()
    tick = models.IntegerField()

class RoundStageTickTime(models.Model):
    round = models.IntegerField(unique=True)
    stage = models.IntegerField()
    tick = models.IntegerField()
    time = models.DateTimeField()
    checked = models.BooleanField()