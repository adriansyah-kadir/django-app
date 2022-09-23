from django.shortcuts import render
from django.contrib.auth import decorators
from .decorator import require_role
from django.views import View
from django.http import HttpRequest


def index(req):
    return render(req, "index.html")
