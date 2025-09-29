from django.core.management.base import BaseCommand
from django.utils import timezone

from polls.models import Question, Choice


class Command(BaseCommand):

    help = 'Load examples to database'

    def handle(self, *args, **options):
        print('Load examples ...')

        q = Question(question_text="What's new?", pub_date=timezone.now())
        q.save()
        q.choice_set.create(choice_text="Not much", votes=0)
        q.choice_set.create(choice_text="Everything is wonderful", votes=0)
        q.save()


        self.stdout.write(
            self.style.SUCCESS('All examples have been loaded')
        )