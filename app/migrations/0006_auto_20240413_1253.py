# Generated by Django 3.2.25 on 2024-04-13 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20240413_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answerlike',
            name='like_count',
        ),
        migrations.RemoveField(
            model_name='questionlike',
            name='like_count',
        ),
    ]
