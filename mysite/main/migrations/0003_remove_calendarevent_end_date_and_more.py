# Generated by Django 4.2.4 on 2023-08-11 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_calendarevent_delete_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendarevent',
            name='end_date',
        ),
        migrations.AlterField(
            model_name='calendarevent',
            name='start_date',
            field=models.DateField(),
        ),
    ]