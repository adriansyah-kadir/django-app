from django.http import HttpRequest
from django.core.exceptions import RequestAborted
from django.http.response import Http404, HttpResponseForbidden
from django.urls.base import reverse
from django.shortcuts import redirect
from .models import Profile


def require_role(roles: list[str], prevent=True, redirect_to=None):
    def actual_decorator(func):
        def handler(req: HttpRequest, *args, **kwargs):
            try:
                profile = req.user.profile
            except AttributeError as e:
                profile = None
            if profile == None:
                print(f"{req.user} doesnt have profile")
                return redirect(reverse("account:profile"))
            role = profile.role
            print(
                "profile role = " + str(role),
                "required roles = " + str(roles),
                sep=", ",
            )
            if role in roles or role == roles:
                if profile.get_role_model() != None:
                    if prevent and req.path == profile.get_role_register_url():
                        raise Http404
                    return func(req, *args, **kwargs)
                print("profile doesnt have role model")
                if req.path == profile.get_role_register_url():
                    return func(req, *args, **kwargs)
                return redirect(profile.get_role_register_url() + "?next=" + req.path)
            return HttpResponseForbidden(
                "your role not allowed required role = " + str(roles)
            )
        return handler
    return actual_decorator
