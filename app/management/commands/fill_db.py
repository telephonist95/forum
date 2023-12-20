from django.core.management import BaseCommand
from django.contrib.auth.models import User
from app.models import *

import random
import faker


fake = faker.Faker(use_weighting=False) # optimization


class Command(BaseCommand):
    help = 'Fills database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('num', type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['num']

        # Users generation
        users = [
            User(username=fake.unique.user_name(),
                 email=fake.email(),
                 password=fake.password(special_chars=False))
            for i in range(num)]
        User.objects.bulk_create(users)
        self.stdout.write("Users are successfully generated")

        # Profiles generation
        profiles = [
            Profile(user=users[i],
                    avatar=fake.file_name(extension='png'))
            for i in range(num)]
        Profile.objects.bulk_create(profiles)
        self.stdout.write("Profiles are successfully generated")

        # Tags generation
        tags = [
            Tag(name=fake.unique.pystr(max_chars=5))
            for i in range(num)
        ]
        Tag.objects.bulk_create(tags)
        self.stdout.write("Tags are successfully generated")

        # Questions generation
        questions = [
            Question(user=users[i//10],
                     title=fake.text(max_nb_chars=16),
                     text=fake.text())
            for i in range(num*10)
        ]
        Question.objects.bulk_create(questions)
        questions = Question.objects.all()
        # Initializing of ManyToMany fields
        for question in questions:
            question.tags.set(fake.random_sample(tags, fake.random_int(3, 7)))
        self.stdout.write("Questions are successfully generated")

        # Answers generation
        answers = [
            Answer(user=users[i//100],
                   text=fake.text(),
                   question=fake.random_element(questions),
                   correct=fake.pybool())
            for i in range(num*100)
        ]
        Answer.objects.bulk_create(answers)
        self.stdout.write("Answers are successfully generated")

        # Question reactions generation
        question_reactions = [
            QuestionReaction(user=users[i//20],
                             positive=fake.pybool())
            for i in range(num*20)
        ]
        for i in range(num):
            user_questions = fake.random_sample(questions, 20)
            for j in range(20):
                question_reactions[i*20 + j].question = user_questions[j]
        QuestionReaction.objects.bulk_create(question_reactions)
        self.stdout.write("Question reactions are successfully generated")

        # Answer reactions generation
        answer_reactions = [
            AnswerReaction(user=users[i//180],
                           positive=fake.pybool())
            for i in range(num*180)
        ]
        for i in range(num):
            user_answers = fake.random_sample(answers, 180)
            for j in range(180):
                answer_reactions[i*180 + j].answer = user_answers[j]
        AnswerReaction.objects.bulk_create(answer_reactions)
        self.stdout.write("Answer reactions are successfully generated")

