# Generated by Django 4.0.4 on 2022-06-20 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
    ]