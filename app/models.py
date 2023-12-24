from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Case, When


class QuestionManager(models.Manager):
    def with_rating(self):
        return self.annotate(rating=Sum(Case(When(questionreaction__positive=True, then=1),
                                             When(questionreaction__positive=False, then=-1)), default=0))

    def hot(self):
        return self.with_rating().order_by('-rating')

    def newest(self):
        return self.with_rating().order_by('created')

    def by_id(self, question_id):
        return self.with_rating().get(id=question_id)

    def by_tag(self, tag_name):
        return self.with_rating().filter(tags__name=tag_name)


class AnswerManager(models.Manager):
    def with_rating(self):
        return self.annotate(rating=Sum(Case(When(answerreaction__positive=True, then=1),
                                             When(answerreaction__positive=False, then=-1)), default=0))

    def to_question(self, question):
        return self.with_rating().filter(question=question).order_by('created')


class QuestionReactionManager(models.Manager):
    def like(self, user, question):
        if self.filter(user=user, question=question).exists():
            self.filter(user=user, question=question).delete()
        else:
            self.create(user=user, question=question, positive=True)

    def dislike(self, user, question):
        if self.filter(user=user, question=question).exists():
            self.filter(user=user, question=question).delete()
        else:
            self.create(user=user, question=question, positive=False)


class AnswerReactionManager(models.Manager):
    def like(self, user, answer):
        if self.filter(user=user, answer=answer).exists():
            self.filter(user=user, answer=answer).delete()
        else:
            self.create(user=user, answer=answer, positive=True)

    def dislike(self, user, answer):
        if self.filter(user=user, answer=answer).exists():
            self.filter(user=user, answer=answer).delete()
        else:
            self.create(user=user, answer=answer, positive=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default='avatar.png', upload_to='avatar/%Y/%m/%d')


class Tag(models.Model):
    name = models.CharField(max_length=16)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=32)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    correct = models.BooleanField()

    objects = AnswerManager()


class QuestionReaction(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    positive = models.BooleanField()


class AnswerReaction(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    positive = models.BooleanField()
