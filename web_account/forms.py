from django import forms
from django.core.exceptions import ValidationError
import re
from core import models


def validate_phone_num(value):
    v = re.match("+?[0-9]*")
    if v == None:
        raise ValidationError("{} not a phone number".format(value))


class StudentForm(forms.Form):
    phone = forms.CharField(
        max_length=10, validators=[validate_phone_num], required=False
    )
    email = forms.EmailField(required=False)
    nisn = forms.CharField(max_length=30)


class UserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ["role", "img"]
