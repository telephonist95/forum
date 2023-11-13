from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField()


class Tag(models.Model):
    name = models.CharField(max_length=16)


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=32)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    text = models.TextField()
    correct = models.BooleanField()


class Reaction(models.Model):
    positive = models.BooleanField()
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    answer = models.ManyToManyField(Answer)
    question = models.ManyToManyField(Question)
