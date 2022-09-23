from django.contrib.auth import mixins, decorators
from django.http.response import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
)
from django.urls.base import reverse
from django.utils.encoding import repercent_broken_unicode
from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest
from core.decorator import require_role
from core import models
import re


@decorators.login_required
@require_role(["teacher"])
def question_register(req: HttpRequest):
    if req.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    homework = get_object_or_404(
        models.HomeWork, id=req.POST.get("homework"), done=False
    )
    if homework._class.teacher != req.user.profile.get_role_model():
        raise Http404
    text = req.POST.get("text")
    if text == None or re.match("^[^\S]*$", text):
        return HttpResponseBadRequest("not enough argument")
    question = models.Question.objects.create(homework=homework, text=text)
    question.save()
    return redirect(reverse("homework:detail", kwargs={"homework_id": homework.id}))


@decorators.login_required
@require_role("teacher")
def question_delete(req: HttpRequest):
    if req.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    question = get_object_or_404(models.Question, id=req.POST.get("question"))
    if question.homework.done:
        raise Http404
    _class = question.homework._class
    if _class.teacher != req.user.profile.teacher:
        raise HttpResponseForbidden
    question.delete()
    return redirect(
        reverse("homework:detail", kwargs={"homework_id": question.homework.id})
    )

@decorators.login_required
@require_role(["teacher"])
def answer_register(req: HttpRequest):
    print(req.POST)
    if req.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    question = get_object_or_404(
        models.Question,
        id=req.POST.get("question"),
    )
    if (
        question.homework._class.teacher != req.user.profile.teacher
        or question.homework.done
    ):
        raise Http404
    text = req.POST.get("text")
    is_true = True if req.POST.get("is_true") == 'on' else False
    if is_true and question.answer_set.filter(is_true=True).first() != None:
        raise Http404
    if text == None:
        return HttpResponseBadRequest("not enough argument")
    answer = models.Answer.objects.create(
        question=question, text=text, is_true=is_true
    )
    answer.save()
    return redirect(
        reverse("homework:detail", kwargs={"homework_id": question.homework.id})
    )


@decorators.login_required
@require_role("teacher")
def answer_delete(req: HttpRequest):
    if req.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    answer = get_object_or_404(
        models.Answer, id=req.POST.get("answer")
    )
    question = answer.question
    if question.homework.done:
        raise Http404
    _class = question.homework._class
    if _class.teacher != req.user.profile.teacher:
        raise Http404
    answer.delete()
    return redirect(
        reverse("homework:detail", kwargs={"homework_id": question.homework.id})
    )
