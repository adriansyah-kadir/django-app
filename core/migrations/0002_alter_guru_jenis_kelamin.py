# Generated by Django 4.0.6 on 2022-08-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guru',
            name='jenis_kelamin',
            field=models.CharField(choices=[('l', 'lali-laki'), ('p', 'perempuan')], max_length=2),
        ),
    ]