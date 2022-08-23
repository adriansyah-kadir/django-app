from django.shortcuts import render
from django.contrib.auth import decorators
from .decorator import require_role
from django.views import View
from django.http import HttpRequest


@require_role(roles=["T", "S"])
@decorators.login_required()
def index(req):
    return render(req, "index.html")


class SettingView(View):
    template_name = "settings.html"

    def get(self, req: HttpRequest):
        @require_role(roles=["T", "S"])
        def handler(req: HttpRequest):
            return render(req, self.template_name)

        return handler(req)
