from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    role = models.CharField(
        max_length=1,
        choices=(
            ('T', 'Teacher'),
            ('S', 'Student')
        )
    )
    role_id = models.BigIntegerField()

class Teacher(models.Model):
    user = models.ForeignKey(User, models.CASCADE) 
    name = models.CharField(max_length=30)
    gender = models.CharField(
        max_length=1,
        choices=( ('m', 'man'), ('w', 'woman') )
    )
    no_telepon = models.CharField(max_length=10)

class Class(models.Model):
    class_name = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teacher, models.CASCADE)

class Student(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    name = models.CharField(max_length=30)
    student_class = models.ForeignKey(Class, models.CASCADE)
    phone = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    gender = models.CharField(
        max_length=1,
        choices=( ('m', 'man'), ('w', 'woman') )
    )
    nisn = models.CharField(max_length=20)
