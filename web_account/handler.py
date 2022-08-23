from django.http import JsonResponse, HttpRequest
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.contrib.auth import (
    decorators,
    login as auth_login,
    authenticate,
    logout as auth_logout,
    mixins,
)
from django.urls.base import reverse
from django.views import View
from . import forms
from core import models


class Login(View):
    template_view = "web_account/login.html"
    ctx = {"form": forms.UserForm()}

    def get(self, req: HttpRequest):
        return render(req, self.template_view, self.ctx)

    def post(self, req: HttpRequest):
        form = forms.UserForm(req.POST)
        if not form.is_valid():
            self.ctx['form'] = form
            self.ctx['error'] = 'invalid'
            return self.get(req)

        data = form.cleaned_data
        user = authenticate(username=data["username"], password=data["password"])
        if user == None:
            self.ctx["form"] = form
            self.ctx["error"] = "user not found"
            return render(req, self.template_view, self.ctx)

        auth_login(req, user)

        return redirect(req.GET.get("next") if req.GET.get("next") else "/")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def logout(req: HttpRequest):
    auth_logout(req)
    return redirect("/")


class Register(View):
    template_view = "web_account/register.html"
    form = forms.UserForm()
    ctx = {"form": form}

    def get(self, req: HttpRequest):
        return render(req, self.template_view, self.ctx)

    def post(self, req: HttpRequest):
        form = forms.UserForm(req.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("bad request")

        data = form.cleaned_data
        try:
            user = models.User.objects.create_user(
                username=data["username"], password=data["password"]
            )
        except Exception as e:
            self.ctx["error"] = "failed"
            self.ctx["form"] = form
            return render(req, self.template_view, self.ctx)
        auth_login(req, user)
        return redirect(reverse("account:profile"))


class Profile(mixins.LoginRequiredMixin, View):
    template_view = "web_account/profile.html"
    ctx = {"form": forms.ProfileForm()}

    def get(self, req: HttpRequest):
        return render(req, self.template_view, self.ctx)

    def post(self, req: HttpRequest):
        form = forms.ProfileForm(req.POST, req.FILES)
        if not form.is_valid():
            self.ctx["error"] = "wrong value"
            return render(req, self.template_view, self.ctx)
        data = form.cleaned_data
        profile = models.Profile.objects.create(user=req.user, **data)
        profile.save()
        if data['role'] == 'T':
            return redirect(reverse('teacher:register'))
        if data['role'] == 'S':
            return redirect(reverse('student:register'))

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.profile != None: return redirect("/")
        except AttributeError as e:
            print(e)
        return super().dispatch(request, *args, **kwargs)


def reset(req: HttpRequest):
    try:
        profile = req.user.profile
    except Exception:
        profile = None
    print(profile)
    if profile != None:
        if profile.role_id:
            profile.role_id = None
            profile.save()
        else:
            profile.delete()
            return redirect("/")
    return redirect("/")
