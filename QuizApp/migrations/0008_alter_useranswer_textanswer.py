# Generated by Django 3.2.7 on 2021-09-15 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuizApp', '0007_alter_useranswer_textanswer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='textAnswer',
            field=models.CharField(blank=True, default=1, max_length=100),
            preserve_default=False,
        ),
    ]
