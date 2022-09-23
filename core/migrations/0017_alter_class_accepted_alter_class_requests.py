# Generated by Django 4.0.6 on 2022-08-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0016_remove_student_student_class_class_accepted_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="class",
            name="accepted",
            field=models.ManyToManyField(
                related_name="class_accepted", to="core.student"
            ),
        ),
        migrations.AlterField(
            model_name="class",
            name="requests",
            field=models.ManyToManyField(
                related_name="class_request", to="core.student"
            ),
        ),
    ]
