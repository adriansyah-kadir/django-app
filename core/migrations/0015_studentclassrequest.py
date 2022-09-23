# Generated by Django 4.0.6 on 2022-08-25 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0014_remove_profile_student_remove_profile_teacher_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentClassRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "requested_class",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.class"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.student"
                    ),
                ),
            ],
        ),
    ]