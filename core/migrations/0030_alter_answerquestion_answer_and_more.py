# Generated by Django 4.0.6 on 2022-08-29 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0029_homeworkanswer_answerquestion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answerquestion",
            name="answer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.answer"
            ),
        ),
        migrations.AlterField(
            model_name="homeworkanswer",
            name="homework",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.homework"
            ),
        ),
    ]
