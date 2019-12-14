# Generated by Django 2.0.13 on 2019-12-14 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CounterChanges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DeferredCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_value', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='counterchanges',
            name='counter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deferredCounters.DeferredCounter'),
        ),
    ]
