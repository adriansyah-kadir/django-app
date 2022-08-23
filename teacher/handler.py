from django import views
from django.http import HttpRequest
from django.shortcuts import redirect, render
from . import forms
from core import models
from django.contrib.auth import mixins
from core.decorator import require_role

import teacher

class Register(mixins.LoginRequiredMixin, views.View):
    template_name = 'teacher/register.html'
    ctx = {
        'form': forms.TeacherForm()
    }
    def get(self, req: HttpRequest):
        return render(req, self.template_name, self.ctx)

    def post(self, req: HttpRequest):
        form = forms.TeacherForm(req.POST, req.FILES)
        if not form.is_valid():
            self.ctx['error'] = 'validation error'
            return self.get(req)

        data = form.cleaned_data
        profile = req.user.profile
        teacher = models.Teacher.objects.create(**data)
        profile.role_id = teacher.id
        teacher.save()
        profile.save()
        return redirect("/")
    
    def dispatch(self, request, *args, **kwargs):
        @require_role(['T'])
        def handler(req, *args, **kwargs):
            return super(type(self), self).dispatch(request, *args, **kwargs)
        return handler(request, *args, **kwargs)
