# Generated by Django 3.2.7 on 2021-09-25 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0004_auto_20210925_1804'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useranswer',
            old_name='currentScore',
            new_name='current_score',
        ),
    ]