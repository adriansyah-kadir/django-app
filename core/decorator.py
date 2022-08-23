from django.http import HttpRequest
from django.core.exceptions import RequestAborted
from django.urls.base import reverse
from django.shortcuts import redirect
from .models import Profile

def require_role(roles: list[str], prevent=True, redirect_to='/'):
    def actual_decorator(func):
        def handler(req: HttpRequest, *args, **kwargs):
            try:
                profile = req.user.profile
                if profile == None:
                    return redirect(reverse("account:profile"))
                role = profile.role
                print(role, roles)
                if role in roles:
                    if profile.get_role_model() != None:
                        if prevent and req.path==profile.get_role_register_url():
                            return redirect(redirect_to)
                        return func(req, *args, **kwargs)
                    if req.path == profile.get_role_register_url():
                        return func(req, *args, **kwargs)
                return redirect(profile.get_role_register_url())
            except AttributeError as e:
                print(e)
                return redirect("account:profile")

        return handler

    return actual_decorator
