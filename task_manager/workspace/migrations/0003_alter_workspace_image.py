# Generated by Django 4.0.4 on 2022-06-20 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0002_alter_workspace_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='image',
            field=models.ImageField(null=True, upload_to='image'),
        ),
    ]
