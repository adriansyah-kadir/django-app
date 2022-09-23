from django import forms
from core import models


class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = models.HomeWork
        fields = ["name", "description", "expire"]
