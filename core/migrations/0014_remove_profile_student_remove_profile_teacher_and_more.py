# Generated by Django 4.0.6 on 2022-08-25 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0013_alter_profile_student_alter_profile_teacher"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="student",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="teacher",
        ),
        migrations.AddField(
            model_name="student",
            name="profile",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.profile",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="teacher",
            name="profile",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.profile",
            ),
            preserve_default=False,
        ),
    ]
