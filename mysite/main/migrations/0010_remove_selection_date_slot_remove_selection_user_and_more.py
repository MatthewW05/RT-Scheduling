# Generated by Django 4.2.4 on 2023-08-15 02:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_dateslot_schedule_selection_delete_calendarevent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selection',
            name='date_slot',
        ),
        migrations.RemoveField(
            model_name='selection',
            name='user',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='selected_dates',
        ),
        migrations.AddField(
            model_name='schedule',
            name='selected_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schedule',
            name='selected_row',
            field=models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='DateSlot',
        ),
        migrations.DeleteModel(
            name='Selection',
        ),
    ]
