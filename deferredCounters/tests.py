# Create your tests here.
from django.test import TestCase

from deferredCounters.models import DeferredCounter, CounterChanges


class DeferredCounterlTestCase(TestCase):
    def setUp(self):
        self.counter = DeferredCounter.objects.create()
        self.counter2 = DeferredCounter.objects.create()

    def test_increment_immediate(self):
        self.assertEqual(self.counter.current_value, 0)
        self.counter.immediate_increment()
        self.assertEqual(self.counter.current_value, 1)
        self.counter.immediate_decrement()
        self.assertEqual(self.counter.current_value, 0)

    def test_increment(self):
        self.counter.increment()
        self.assertEqual(self.counter.current_value, 0)
        self.assertEqual(self.counter.compute_value(), 1)
        self.counter.decrement()
        self.assertEqual(self.counter.current_value, 0)
        self.assertEqual(self.counter.compute_value(), 0)

    def test_compact(self):
        self.counter.increment()
        self.counter.increment()
        self.counter2.increment()
        CounterChanges.objects.compact()
        self.counter.refresh_from_db()
        self.assertEqual(self.counter.current_value, 2)
        CounterChanges.objects.compact()
        self.counter.refresh_from_db()
        self.assertEqual(self.counter.current_value, 2)
        self.counter.decrement()
        self.counter.decrement()
        self.counter2.decrement()
        CounterChanges.objects.compact()
        self.counter.refresh_from_db()
        self.assertEqual(self.counter.current_value, 0)

    def test_with_computed_value(self):
        self.counter2.increment()
        c2 = DeferredCounter.objects.with_computed_value().filter(id=self.counter2.id)[0]
        self.assertEqual(c2.computed_value, 1)
        c = DeferredCounter.objects.with_computed_value().filter(id__in=(self.counter.id, self.counter2.id))
        for each in c:
            if each.id == self.counter.id:
                self.assertEqual(each.computed_value, 0)
            else:
                self.assertEqual(each.computed_value, 1)
