from django.db import models
from django.conf import settings
from django.db.models import Sum, Case, When


class QuestionManager(models.Manager):
    def with_rating(self):
        return self.annotate(rating=Sum(Case(When(reactions__positive=True, then=1),
                                             When(reactions__positive=False, then=-1))))


class AnswerManager(models.Manager):
    def with_rating(self):
        return self.annotate(rating=Sum(Case(When(reactions__positive=True, then=1),
                                             When(reactions__positive=False, then=-1))))


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField()


class Tag(models.Model):
    name = models.CharField(max_length=16)


class Reaction(models.Model):
    positive = models.BooleanField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=32)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    reactions = models.ManyToManyField(Reaction)

    objects = QuestionManager()


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    correct = models.BooleanField()
    reactions = models.ManyToManyField(Reaction)

    objects = AnswerManager()
