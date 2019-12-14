from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from deferredCounters.models import CounterChanges


class Command(BaseCommand):
    help = 'Apply pending changes to counters'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                CounterChanges.objects.compact()
        except Exception as e:
            raise CommandError('There was an error processing the changes: %s' % e)

        self.stdout.write(self.style.SUCCESS('Successfully processed all the changes'))
