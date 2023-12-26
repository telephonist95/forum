from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Case, When, Count


class QuestionManager(models.Manager):
    def with_rating(self):
        return self.annotate(rating=Sum(Case(When(article__reaction__positive=True, then=1),
                                             When(article__reaction__positive=False, then=-1)), default=0))

    def hot(self):
        return self.with_rating().order_by('-rating')

    def newest(self):
        return self.with_rating().order_by('-article__created')

    def by_id(self, question_id):
        return self.with_rating().get(id=question_id)

    def by_tag(self, tag_name):
        return self.with_rating().filter(tags__name=tag_name)


class AnswerManager(models.Manager):
    def with_rating(self):
        return self.annotate(rating=Sum(Case(When(article__reaction__positive=True, then=1),
                                             When(article__reaction__positive=False, then=-1)), default=0))

    def to_question(self, question):
        return self.with_rating().filter(question=question).order_by('article__created')


class TagManager(models.Manager):
    def most_popular(self, count):
        return self.annotate(num_tags=Count("question__tags")).order_by("-num_tags")[:count]


class ProfileManager(models.Manager):
    def with_rating(self):
        return self.annotate(rating=Sum(Case(When(user__article__reaction__positive=True, then=1),
                                             When(user__article__reaction__positive=False, then=-1)), default=0))

    def most_popular(self, count):
        return self.with_rating().order_by('-rating')[:count]


class ReactionManager(models.Manager):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default='avatar.png', upload_to='avatar/%Y/%m/%d')

    objects = ProfileManager()


class Tag(models.Model):
    name = models.CharField(max_length=16)

    objects = TagManager()


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


class Question(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=32)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()


class Answer(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField()

    objects = AnswerManager()


class Reaction(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    positive = models.BooleanField()
