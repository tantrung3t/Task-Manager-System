# Generated by Django 4.0.4 on 2022-06-21 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 21, 13, 55, 45, 1354)),
        ),
    ]
