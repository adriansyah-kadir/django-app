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
from django.views.generic import DetailView
from . import forms
from core import models, decorator


class Login(View):
    template_view = "skeleton/form.html"

    def get(self, req: HttpRequest):
        ctx = {"title": "login", "form": forms.UserForm()}
        return render(req, self.template_view, ctx)

    def post(self, req: HttpRequest):
        form = forms.UserForm(req.POST)
        ctx = {"title": "login", "form": form}
        if not form.is_valid():
            ctx["error"] = "invalid"
            return render(req, self.template_view, ctx)

        data = form.cleaned_data
        user = authenticate(username=data["username"], password=data["password"])
        if user == None:
            ctx["error"] = "user not found"
            return render(req, self.template_view, ctx)

        auth_login(req, user)

        return redirect(req.GET.get("next") if req.GET.get("next") else "/")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def logout(req: HttpRequest):
    auth_logout(req)
    return redirect(reverse("account:login"))


class Register(View):
    template_view = "skeleton/form.html"

    def get(self, req: HttpRequest):
        ctx = {"form": forms.UserForm()}
        return render(req, self.template_view, ctx)

    def post(self, req: HttpRequest):
        form = forms.UserForm(req.POST)
        ctx = {"form": form}
        if not form.is_valid():
            return render(req, self.template_view, ctx)

        data = form.cleaned_data
        try:
            user = models.User.objects.create_user(
                username=data["username"], password=data["password"]
            )
        except Exception as e:
            ctx["error"] = "user not found"
            return render(req, self.template_view, ctx)
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
        return redirect(profile.get_role_register_url())

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.profile != None:
                return redirect("/")
        except AttributeError as e:
            print(e)
        return super().dispatch(request, *args, **kwargs)


def reset(req: HttpRequest):
    pass


class Detail(mixins.LoginRequiredMixin, DetailView):
    model = models.User
    template_name = "web_account/profile_detail.html"


class SettingView(mixins.LoginRequiredMixin, View):
    template_name = "settings.html"

    def get(self, req: HttpRequest):
        return render(req, self.template_name)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
