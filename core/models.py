from django.db import models
from django.contrib.auth import get_user_model
from django.http import request
from django.urls.base import reverse
from django.utils import timezone
import datetime

import homework

User = get_user_model()

class Profile(models.Model):
    img = models.ImageField(upload_to="profile", blank=True, null=True)
    user = models.OneToOneField(User, models.CASCADE)
    role = models.CharField(
        max_length=10,
        choices=(("teacher", "teacher"), ("student", "student")),
        help_text="are you a student or teacher",
    )

    @property
    def role_name(self):
        match self.role:
            case "teacher":
                return self.teacher.name
            case "student":
                return self.student.name
        

    def get_role_model(self):
        try:
            if self.role == "teacher":
                return self.teacher
            else:
                return self.student
        except Exception:
            return None

    def get_role_register_url(self):
        match self.role:
            case "teacher":
                return reverse("teacher:register")
            case "student":
                return reverse("student:register")

    def delete(self, using=None, keep_parents=False):
        print("deleting")
        return super().delete(using, keep_parents)


class Teacher(models.Model):
    name = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=1, choices=(("m", "man"), ("w", "woman")))
    phone = models.CharField(max_length=10, blank=True, null=True)
    profile = models.OneToOneField(Profile, models.CASCADE)

    def __str__(self):
        return str(self.name)


class Student(models.Model):
    name = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(("m", "man"), ("w", "woman")))
    nisn = models.CharField(max_length=20, help_text="nomor induk siswa")
    profile = models.OneToOneField(Profile, models.CASCADE)

    def __str__(self):
        return self.name

    def has_answered_homework(self, homework):
        "return none if not answered"
        return self.homeworkanswer_set.filter(homework=homework).first() != None


class Class(models.Model):
    class_name = models.CharField(max_length=20)
    teacher = models.ForeignKey(Teacher, models.CASCADE)
    description = models.TextField(blank=True, null=True)
    requests = models.ManyToManyField(Student, "class_request", blank=True)
    accepted = models.ManyToManyField(Student, "class_accepted", blank=True)
    excerpt = models.CharField(max_length=100)
    img = models.ImageField(upload_to="class", blank=True, null=True)

    def __str__(self):
        return str(self.class_name + " {}".format(self.teacher))

    def student_accepted(self, student):
        "return true if student models exists in accepted field"
        if not student: return False
        return self.accepted.filter(id=student.id).first() != None


class HomeWork(models.Model):
    _class = models.ForeignKey(Class, models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    done = models.BooleanField(default=False)
    expire = models.DateTimeField()
    added_at = models.DateTimeField(auto_now_add=True)

    def created(self):
        timedelta: datetime.timedelta = timezone.now()-self.added_at
        if int(timedelta.days / 365):
            return f"{int(timedelta.days/365)}y"
        elif int(timedelta.days / 30):
            return f"{int(timedelta.days/30)}m"
        elif int(timedelta.days / 7):
            return f"{int(timedelta.days/7)}w"
        elif int(timedelta.days):
            return f"{timedelta.days}d"
        elif int(timedelta.seconds / (60 * 60)):
            return f"{int(timedelta.seconds/(60*60))}h"
        elif int(timedelta.seconds / 60):
            return f"{int(timedelta.seconds/60)}m"
        else:
            return f"{timedelta.seconds}s"

    def time_to_expire(self):
        timedelta: datetime.timedelta = self.expire-timezone.now()
        if int(timedelta.days / 365):
            return f"{int(timedelta.days/365)}y"
        elif int(timedelta.days / 30):
            return f"{int(timedelta.days/30)}m"
        elif int(timedelta.days / 7):
            return f"{int(timedelta.days/7)}w"
        elif int(timedelta.days):
            return f"{timedelta.days}d"
        elif int(timedelta.seconds / (60 * 60)):
            return f"{int(timedelta.seconds/(60*60))}h"
        elif int(timedelta.seconds / 60):
            return f"{int(timedelta.seconds/60)}m"
        else:
            return f"{timedelta.seconds}s"

    def students_homeworkanswer(self):
        pass

    def students_has_answer(self):
        "return student that has answered this homework"
        d=[]
        for x in self.homeworkanswer_set.all():
            d.append(x.student)
        return d

    def students_didnt_answer(self):
        "return student that didnt answered this homework"
        return self._class.accepted.exclude(id__in=[s.id for s in self.students_has_answer()])

    def homeworkanswer_from(self, student):
        return self.homeworkanswer_set.filter(student=student).first()

    def is_expire(self):
        return timezone.now() > self.expire

    def __str__(self):
        return self.name


class Question(models.Model):
    homework = models.ForeignKey(HomeWork, models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=100)
    question = models.ForeignKey(Question, models.CASCADE)
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class HomeWorkAnswer(models.Model):
    student = models.ForeignKey(Student, models.CASCADE)
    homework = models.ForeignKey(HomeWork, models.CASCADE)

    def selected_answer(self, question):
        d=self.answerquestion_set.filter(question=question).first()
        if d != None:
            return d.answer
        return None

    def right_answer(self):
        d=[]
        for a in self.answerquestion_set.all():
            if a.answer.is_true:
                d.append(a)
        return d


class AnswerQuestion(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
    answer = models.ForeignKey(Answer, models.CASCADE)
    homework_answer = models.ForeignKey(HomeWorkAnswer, models.CASCADE)
