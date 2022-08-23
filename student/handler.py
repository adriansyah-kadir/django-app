from django.views import View
from django.http import HttpRequest
from django.shortcuts import redirect, render
from .forms import StudentForm
from core import models
from core.decorator import require_role

class RegisterView(View):
    template_name = "student/register.html"
    ctx = {"form": StudentForm()}

    def get(self, req: HttpRequest):
        return render(req, self.template_name, self.ctx)

    def post(self, req: HttpRequest):
        form = StudentForm(req.POST)
        if not form.is_valid():
            self.ctx["form"] = form
            return render(req, self.template_name, self.ctx)
        data = form.cleaned_data
        profile = req.user.profile
        student = models.Student.objects.create(**data)
        profile.role_id = student.id
        student.save()
        profile.save()
        print(student)
        return redirect("/")

    def dispatch(self, request, *args, **kwargs):
        @require_role(['S'])
        def handler(req, *args, **kwargs):
            return super(type(self), self).dispatch(request, *args, **kwargs)
        return handler(request, *args, **kwargs)
