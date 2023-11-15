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

        # Reactions generation
        reactions = [
            Reaction(user=users[i//200],
                     positive=fake.pybool())
            for i in range(num*200)
        ]
        Reaction.objects.bulk_create(reactions)
        random.shuffle(reactions)
        self.stdout.write("Reactions are successfully generated")

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
            question.reactions.set(reactions[:5])
            del reactions[:5]
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
        answers = Answer.objects.all()
        # Initializing of ManyToMany fields
        for answer in answers:
            if len(reactions):
                count = fake.random_int(1, 2)
                answer.reactions.set(reactions[:count])
                del reactions[:count]
        self.stdout.write("Answers are successfully generated")
