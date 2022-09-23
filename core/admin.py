from django.contrib import admin
from core import models

# Register your models here.

admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.Class)
admin.site.register(models.Profile)
admin.site.register(models.HomeWork)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.HomeWorkAnswer)
admin.site.register(models.AnswerQuestion)
