from django.contrib import admin
from core import models

# Register your models here.

admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.Class)
admin.site.register(models.Profile)
