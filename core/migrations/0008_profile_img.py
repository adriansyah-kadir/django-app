# Generated by Django 4.0.6 on 2022-08-21 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_remove_student_user_remove_teacher_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
