from django.http import HttpRequest
from django.core.exceptions import RequestAborted
from django.urls.base import reverse
from django.shortcuts import redirect

def require_role(roles: list[str]):
    def actual_decorator(func):
        def handler(req: HttpRequest, *args, **kwargs):
            try:
                if req.user.profile_set.count() <= 0:
                    return redirect(reverse('account:profile'))
                return func(req, *args, **kwargs)
            except Exception as e:
                return redirect('account:login')
        return handler

    return actual_decorator
