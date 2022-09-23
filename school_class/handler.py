from itertools import combinations_with_replacement
from django import views
from django.http.response import Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.views.generic import DetailView, ListView
from django.http import HttpRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import mixins
from django.urls.base import reverse
from django.views.generic.base import View
from core import models
from . import forms
import json
from core.decorator import require_role


class ClassDetail(mixins.LoginRequiredMixin, DetailView):
    model = models.Class
    template_name = "school_class/class_detail.html"


class ClassRegister(mixins.LoginRequiredMixin, views.View):
    template_name = "skeleton/form.html"

    def get(self, req: HttpRequest):
        match req.user.profile.role:
            case "teacher":
                return self.teacher_get(req)
            case "student":
                return self.student_get(req)

    def post(self, req: HttpRequest):
        match req.user.profile.role:
            case "teacher":
                return self.teacher_post(req)
            case "student":
                return self.student_post(req)

    def teacher_get(self, req: HttpRequest):
        ctx = {}
        ctx["form"] = forms.ClassRegisterFormTeacher()
        return render(req, self.template_name, ctx)

    def student_get(self, req: HttpRequest):
        ctx = {}
        ctx["form"] = forms.ClassRegisterFormStudent(
            joined_class=[c.id for c in req.user.profile.student.class_accepted.all()]
            + [c.id for c in req.user.profile.student.class_request.all()]
        )
        return render(req, self.template_name, ctx)

    def teacher_post(self, req: HttpRequest):
        form = forms.ClassRegisterFormTeacher(req.POST, files=req.FILES)
        if not form.is_valid():
            print("class form not valid")
            return render(req, self.template_name, {"form": form})

        data = form.cleaned_data
        created_class = models.Class.objects.create(
            teacher=req.user.profile.teacher, **data
        )
        created_class.save()
        return redirect(reverse("class:register"))

    def student_post(self, req: HttpRequest):
        print("student_post")
        form = forms.ClassRegisterFormStudent(req.GET.get("teacher"), [], req.POST)
        print(form.data)
        if not form.is_valid():
            print(form.data, req.POST)
            return render(req, self.template_name, {"form": form})
        data = form.cleaned_data
        selected_class = models.Class.objects.filter(pk=data["class_choices"]).first()
        selected_class.requests.add(req.user.profile.student)
        selected_class.save()
        return redirect(reverse("class:detail", kwargs={"pk": selected_class.id}))

    def dispatch(self, request, *args, **kwargs):
        @require_role(["student", "teacher"])
        def handler(req, *args, **kwargs):
            return super(type(self), self).dispatch(request, *args, **kwargs)

        return handler(request, *args, **kwargs)


class StudentClassRequest(mixins.LoginRequiredMixin, ListView):
    template_name = "school_class/class_list.html"

    def dispatch(self, request, *args, **kwargs):
        @require_role(["student"])
        def handler(req, *args, **kwargs):
            self.queryset = req.user.profile.student.class_request.all()
            return super(type(self), self).dispatch(request, *args, **kwargs)

        return handler(request, *args, **kwargs)


class ClassRequests(mixins.LoginRequiredMixin, View):
    template_name = "school_class/class_request_list.html"

    def get(self, req: HttpRequest, id):
        _class = get_object_or_404(
            models.Class, id=id, teacher=req.user.profile.get_role_model()
        )
        ctx = {"class": _class, "object_list": _class.requests.all()}
        return render(req, self.template_name, ctx)

    def dispatch(self, request, id, *args, **kwargs):
        @require_role(["teacher"])
        def handler(req, *args, **kwargs):
            return super(type(self), self).dispatch(request, id, *args, **kwargs)

        return handler(request, *args, **kwargs)


class ClassMember(mixins.LoginRequiredMixin, View):
    template_name = "school_class/class_member_list.html"

    def get(self, req: HttpRequest, id):
        _class = get_object_or_404(
            models.Class,
            id=id,
        )
        ctx = {"class": _class, "object_list": _class.accepted.all()}
        return render(req, self.template_name, ctx)

    def dispatch(self, request, id, *args, **kwargs):
        @require_role(["teacher", "student"])
        def handler(req, *args, **kwargs):
            _class = get_object_or_404(models.Class, id=id)
            profile = req.user.profile
            match profile.role:
                case "student":
                    if _class.accepted.filter(id=profile.student.id).first() == None:
                        raise Http404
                case "teacher":
                    if _class.teacher != profile.teacher:
                        raise Http404
            return super(type(self), self).dispatch(request, id, *args, **kwargs)

        return handler(request, *args, **kwargs)


def accept_class(req: HttpRequest, id):
    if req.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    c = get_object_or_404(models.Class, id=id, teacher=req.user.profile.teacher)
    student = get_object_or_404(models.Student, id=req.POST.get("student"))
    c.requests.remove(student)
    c.accepted.add(student)
    return redirect(reverse("class:class_requests", kwargs={"id": id}))


def delete_class(req: HttpRequest, id):
    if req.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    c = get_object_or_404(
        models.Class,
        id=id,
    )
    profile = req.user.profile
    match profile.role:
        case "teacher":
            if c.teacher != profile.teacher:
                raise Http404
            student = get_object_or_404(models.Student, id=req.POST.get("student"))
            c.requests.remove(student)
            c.accepted.remove(student)
            nexturl = req.GET.get('next')
            if nexturl:
                return redirect(nexturl)
        case "student":
            if profile.student.id != req.POST.get('student'):
                raise HttpResponseForbidden(f"youre not {req.POST.get('student')}")
            c.requests.remove(profile.student)
            c.accepted.remove(profile.student)
    return redirect(reverse("class:detail", kwargs={"pk": id}))


# def exit_class(req: HttpRequest, id):
#     c = get_object_or_404(
#         models.Class,
#         id=id,
#     )
#     profile = req.user.profile
#     c.accepted.remove(req.user.profile.student)
#     c.requests.remove(req.user.profile.student)
#     return redirect(reverse('class:detail', kwargs={'pk':id}))
