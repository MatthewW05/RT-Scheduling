# Generated by Django 4.2.4 on 2023-10-30 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_rename_column_selecteddate_row'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitiateSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_start_date', models.DateField()),
                ('schedule_start_date', models.DateField()),
            ],
        ),
    ]