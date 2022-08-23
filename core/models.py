from django.db import models
from django.contrib.auth import get_user_model
from django.urls.base import reverse

User = get_user_model()


class Profile(models.Model):
    img = models.ImageField(upload_to='profile', blank=True, null=True)
    user = models.OneToOneField(User, models.CASCADE)
    role = models.CharField(
        max_length=1,
        choices=(("T", "Teacher"), ("S", "Student")),
        help_text="are you a student or teacher",
    )
    role_id = models.BigIntegerField(blank=True, null=True)

    def get_role_model(self):
        if self.role == "S":
            return Student.objects.filter(pk=self.role_id).first()
        else:
            return Teacher.objects.filter(pk=self.role_id).first()

    def get_role_register_url(self):
        match self.role:
            case 'T':
                return reverse('teacher:register')
            case 'S':
                return reverse('student:register')

    def delete(self, using=None, keep_parents=False):
        print("deleting")
        return super().delete(using, keep_parents)


class Teacher(models.Model):
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices=(("m", "man"), ("w", "woman")))
    phone = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Class(models.Model):
    class_name = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teacher, models.CASCADE)

    def __str__(self):
        return str(self.class_name)


class Student(models.Model):
    name = models.CharField(max_length=30)
    student_class = models.ManyToManyField(Class)
    phone = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(("m", "man"), ("w", "woman")))
    nisn = models.CharField(max_length=20, help_text="nomor induk siswa")
