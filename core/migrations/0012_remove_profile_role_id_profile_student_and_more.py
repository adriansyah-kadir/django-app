# Generated by Django 4.0.6 on 2022-08-25 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_alter_profile_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="role_id",
        ),
        migrations.AddField(
            model_name="profile",
            name="student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.student",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="teacher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.teacher",
            ),
        ),
    ]
