# Generated by Django 5.1.5 on 2025-01-24 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='participant',
            field=models.ManyToManyField(related_name='event', to='events.participant'),
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='event', to='events.category'),
        ),
    ]
