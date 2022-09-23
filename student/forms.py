from django.forms import ModelForm
from core import models


class StudentForm(ModelForm):
    class Meta:
        model = models.Student
        fields = ["name", "phone", "gender", "nisn"]
