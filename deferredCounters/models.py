from django.db import models
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import Coalesce


class DeferredCounterManager(models.Manager):

    def with_computed_value(self):
        return self.get_queryset().annotate(
            computed_value=models.F('current_value') + Coalesce(Sum('counterchanges__change'), 0))


class DeferredCounter(models.Model):
    objects = DeferredCounterManager()

    current_value = models.IntegerField(default=0)

    def increment(self, add=1):
        self.modify(add)

    def decrement(self, subs=1):
        self.modify(-1 * subs)

    def modify(self, value):
        if self.pk:
            change = CounterChanges(counter=self, change=value)
            change.save()
            self.counterchanges_set.add(change)
        else:
            self.current_value += value

    def immediate_modify(self, value):
        self.current_value += value

    def immediate_increment(self, add=1):
        self.immediate_modify(add)

    def immediate_decrement(self, subs=1):
        self.immediate_modify(-1 * subs)

    def compute_value(self):
        changes = self.counterchanges_set.all().aggregate(Sum('change'))['change__sum']
        return self.current_value + (changes if changes else 0)


class CounterChangesManager(models.Manager):

    @transaction.atomic
    def compact(self):
        queryset = self.get_queryset().values("counter").annotate(Sum("change")).iterator()
        changes = True
        batch_size = 2000
        while changes:
            changes_by_counter = {}
            for x in queryset:
                changes_by_counter[x['counter']] = x['change__sum']
                if len(changes_by_counter) >= batch_size: break
            changes = len(changes_by_counter) > 0
            counters = DeferredCounter.objects.filter(id__in=changes_by_counter.keys())
            for each in counters:
                each.current_value += changes_by_counter[each.id]
            DeferredCounter.objects.bulk_update(counters, ["current_value"])
            self.get_queryset().filter(counter__in=counters).delete()


class CounterChanges(models.Model):
    counter = models.ForeignKey(to=DeferredCounter, on_delete=models.CASCADE)
    change = models.IntegerField()

    objects = CounterChangesManager()
