from django import forms
from core import models


class ClassRegisterFormTeacher(forms.ModelForm):
    class Meta:
        model = models.Class
        fields = ["class_name", "description", "excerpt", "img"]


class ClassRegisterFormStudent(forms.Form):
    class_choices = forms.IntegerField(widget=forms.Select)

    def __init__(self, teacher_id=None, joined_class=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        teacher = None
        try:
            teacher = models.Teacher.objects.get(id=teacher_id)
        except Exception as e:
            pass
        if teacher:
            choices = ((c.id, c) for c in models.Class.objects.filter(teacher=teacher))
        else:
            choices = (
                (c.id, c) for c in models.Class.objects.exclude(id__in=joined_class)
            )
        self.fields["class_choices"].widget.choices = choices
