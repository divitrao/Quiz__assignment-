# Generated by Django 3.2.7 on 2021-09-26 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0009_alter_results_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='results',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_for_result', to='QuizApp.question'),
        ),
    ]
