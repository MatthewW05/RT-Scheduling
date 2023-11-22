# Generated by Django 4.2.7 on 2023-11-21 21:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0024_alter_initiateschedule_schedule_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selecteddate',
            name='row',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='selecteddate',
            name='selected_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='selecteddate',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]