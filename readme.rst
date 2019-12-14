Deferred Counters
=====

Deferred Counters is a Django app that allows to count things
and keet a queue of pending counts increments or decrements
to avoid locking. Then you can compact the queue applying 
the pending changes.

A Deferred Counter has a value "current_value" that has the counter value since 
the last time it was compacted.

You can call compute_value() to get the value of the counter considering the changes
that have not yet been applied.

Also, it offers a manager with "with_computed_value" that add the field computed_value to the query set.

More information of the problem this app resolves and how it solves it can be read here:
https://www.depesz.com/2016/06/14/incrementing-counters-in-database/

Quick start
-----------

1. Add "deferredCounters" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'deferredCounters',
    ]


2. Run `python manage.py migrate` to create the Deferred Counters models.

3. Use it in your models with a foreign key to Deferred Counter.
