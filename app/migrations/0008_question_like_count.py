# Generated by Django 3.2.25 on 2024-04-13 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20240413_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='like_count',
            field=models.IntegerField(default=0),
        ),
    ]
