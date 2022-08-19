from django.shortcuts import render
from django.contrib.auth import decorators
from .decorator import require_role

@require_role(['teacher', 'student'])
@decorators.login_required()
def index(req):
    return render(req, 'index.html')
