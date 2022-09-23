from urllib.parse import parse_qsl
from django.db.utils import IntegrityError
from django.http import HttpRequest
from django.contrib.auth import mixins, decorators
from django.http.response import (
    Http404,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseServerError,
)
from django.utils import timezone
from core.decorator import require_role
from django.shortcuts import get_object_or_404, redirect, render, reverse
from core import models
from django.views import View
from django.views.generic import DetailView
from . import forms
import datetime


class HomeWorkView(mixins.LoginRequiredMixin, View):
    template_name = "school_class/home_work_list.html"

    def get(self, req: HttpRequest):
        _class = get_object_or_404(models.Class, id=req.GET.get("class"))
        profile = req.user.profile
        match profile.role:
            case "teacher":
                if _class.teacher != profile.teacher:
                    raise Http404
            case "student":
                if _class.accepted.filter(id=profile.student.id).first() == None:
                    raise Http404
        ctx = {
            "class": _class,
            "object_list": _class.homework_set.all(),
            "form": forms.HomeWorkForm(),
        }
        return render(req, self.template_name, ctx)

    def dispatch(self, request, *args, **kwargs):
        @require_role(["teacher", "student"])
        def handler(req, *args, **kwargs):
            return super(type(self), self).dispatch(request, *args, **kwargs)

        return handler(request, *args, **kwargs)


@decorators.login_required
@require_role(["teacher"])
def homework_register(req: HttpRequest):
    if req.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    exp: str = req.POST.get("expire")
    name = req.POST.get("name")
    desc = req.POST.get("description")
    if not (exp and name):
        return HttpResponseBadRequest("not enough argument")
    y, m, d = exp.split("-")
    _class = get_object_or_404(
        models.Class,
        id=req.POST.get("class"),
        teacher=req.user.profile.get_role_model(),
    )
    homework = models.HomeWork.objects.create(
        _class=_class,
        name=name,
        description=desc if desc else None,
        expire=datetime.datetime(int(y), int(m), int(d)),
    )
    homework.save()
    return redirect(reverse("homework:index") + "?class={}".format(_class.id))


# class HomeWorkRegisterView(mixins.LoginRequiredMixin, View):
#     template_name = 'school_class/home_work_register.html'

#     def get(self, req: HttpRequest, class_id , _class):
#         form = forms.HomeWorkForm()
#         ctx = {
#             'form': form
#         }
#         return render(req, self.template_name, ctx)

#     def post(self, req: HttpRequest, class_id, _class):
#         form = forms.HomeWorkForm(req.POST)
#         ctx = {
#             'class': _class,
#             'form': form
#         }
#         if not form.is_valid():
#             return render(req, self.template_name, ctx)
#         data = form.cleaned_data
#         homework = models.HomeWork.objects.create(
#             _class=ctx['class'],
#             **data
#         )
#         homework.save()
#         return redirect(reverse('homework:detail', kwargs={'class_id':class_id,'homework_id':homework.id}))

#     def dispatch(self, request, class_id, *args, **kwargs):
#         @require_role(['teacher',])
#         def handler(req, class_id, *args, **kwargs):
#             _class = get_object_or_404(models.Class, id=class_id, teacher=req.user.profile.get_role_model())
#             kwargs['_class'] = _class
#             return super(type(self), self).dispatch(request, class_id, *args, **kwargs)
#         return handler(request, class_id, *args, **kwargs)


class HomeWorkDetailView(mixins.LoginRequiredMixin, View):
    template_name = "homework/detail.html"

    def get(self, req: HttpRequest, homework, _class):
        ctx = {"class": _class, "homework": homework}
        return render(req, self.template_name, ctx)

    def dispatch(self, request, homework_id, *args, **kwargs):
        @require_role(["teacher", "student"])
        def handler(req, homework_id, *args, **kwargs):
            homework = get_object_or_404(models.HomeWork, id=homework_id)
            _class = homework._class
            kwargs["_class"] = _class
            kwargs["homework"] = homework
            profile = req.user.profile
            match profile.role:
                case "teacher":
                    if _class.teacher != profile.teacher:
                        raise Http404
                case "student":
                    if _class.accepted.filter(id=profile.student.id).first() == None:
                        raise Http404
            return super(type(self), self).dispatch(request, *args, **kwargs)

        return handler(request, homework_id, *args, **kwargs)


@decorators.login_required
@require_role(["teacher"])
def homework_delete(req: HttpRequest):
    homework = get_object_or_404(models.HomeWork, id=req.POST.get("homework"))
    if homework._class.teacher != req.user.profile.teacher:
        raise Http404
    if not homework.is_expire():
        return HttpResponseForbidden("cannot delete homework before expire")
    homework.delete()
    return redirect(reverse("homework:index") + "?class={}".format(homework._class.id))


@decorators.login_required
@require_role(["teacher"])
def homework_done(req: HttpRequest):
    if req.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    homework: models.HomeWork = get_object_or_404(models.HomeWork, id=req.POST.get("homework"))
    if homework._class.teacher != req.user.profile.get_role_model():
        raise Http404
    qindex = 0
    for question in homework.question_set.all():
        qindex+=1
        theres_no_true_answer = True
        for answer in question.answer_set.all():
            if answer.is_true:
                theres_no_true_answer = False
                continue
        if theres_no_true_answer:
            return HttpResponseBadRequest(
                f"q{qindex}. {question} doesnt have true answer"
            )
    homework.done = True
    homework.added_at = timezone.now()
    homework.save()
    return redirect(reverse("homework:index") + "?class={}".format(homework._class.id))


class HomeWorkStart(mixins.LoginRequiredMixin, View):
    template_name = "homework/answer.html"

    def get(self, req: HttpRequest, homework):
        ctx = {
            "homework": homework,
            "has_answered_homework": req.user.profile.student.has_answered_homework(
                homework
            ),
        }
        return render(req, self.template_name, ctx)

    def post(self, req: HttpRequest, homework: models.HomeWork):
        if req.user.profile.student.has_answered_homework(homework):
            raise Http404

        homework_answer = models.HomeWorkAnswer.objects.create(
            student=req.user.profile.student, homework=homework
        )
        homework_answer.save()
        for question in homework.question_set.all():
            selected = req.POST.get(str(question.id))
            if selected == None:
                return HttpResponseBadRequest("selected question not found")
            answer = get_object_or_404(models.Answer, id=int(selected))
            if homework_answer.answerquestion_set.filter(answer=answer).first() != None:
                continue
            answer_question = models.AnswerQuestion.objects.create(
                question=question, answer=answer, homework_answer=homework_answer
            )
            answer_question.save()

        return self.get(req, homework)

    def dispatch(self, request, homework_id, *args, **kwargs):
        @require_role("student")
        def handler(req: HttpRequest, homework_id, *args, **kwargs):
            homework = get_object_or_404(models.HomeWork, id=homework_id)
            if not homework.done:
                raise Http404
            if homework.is_expire():
                raise Http404
            if (
                homework._class.accepted.filter(id=req.user.profile.student.id).first()
                == None
            ):
                raise Http404
            kwargs["homework"] = homework
            return super(type(self), self).dispatch(req, *args, **kwargs)

        return handler(request, homework_id, *args, **kwargs)


class HomeWorkResult(mixins.LoginRequiredMixin, View):
    def get(self, req: HttpRequest, *args, **kwargs):
        profile = req.user.profile
        homework = get_object_or_404(
            models.HomeWork,
            id=kwargs.get('homework_id')
        )
        kwargs['homework'] = homework
        match profile.role:
            case 'student':
                student_id = kwargs.get('student_id')
                if student_id != profile.student.id:
                    if student_id == None:
                        return redirect(
                            reverse(
                                'homework:student_result',
                                kwargs={
                                    'homework_id': kwargs.get('homework_id'),
                                    'student_id': profile.student.id
                                }
                            )
                        )
                    raise Http404
                kwargs['student'] = profile.student
                return self.get_student(req, *args, **kwargs)
            case 'teacher':
                kwargs['teacher'] = profile.teacher
                return self.get_teacher(req, *args, **kwargs)

    def get_student(self, req: HttpRequest, *args, **kwargs):
        ctx = {}
        homework = kwargs.get('homework')
        if not homework._class.student_accepted(kwargs.get('student')):
            raise Http404
        homeworkanswer = get_object_or_404(
            models.HomeWorkAnswer,
            student=kwargs.get('student'),
            homework=homework
        )
        ctx['homework'] = homework
        ctx['homeworkanswer'] = homeworkanswer
        ctx['student'] = kwargs.get('student')
        return render(req, "homework/result/student.html", ctx)

    def get_teacher(self, req: HttpRequest, teacher, *args, **kwargs):
        ctx={}
        homework: models.HomeWork = kwargs.get('homework')
        if homework._class.teacher != teacher:
            raise Http404
        if kwargs.get('student_id') != None:
            student = get_object_or_404(
                models.Student,
                id=kwargs.get('student_id')
            )
            if not homework._class.student_accepted(student):
                raise Http404
            return self.get_student(req, student=student, homework=homework)
        ctx['homework']=homework
        ctx['teacher']=teacher
        ctx['students_has_answer']=homework.students_has_answer()
        ctx['students_didnt_answer']=homework.students_didnt_answer()
        return render(req, "homework/result/teacher.html", ctx)

    def post_student(self, req: HttpRequest, *args, **kwargs):
        pass

    def post_teacher(self, req: HttpRequest, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        @require_role(['student', 'teacher'])
        def handler(request, *args, **kwargs):
            return super(type(self), self).dispatch(request, *args, **kwargs)
        return handler(request, *args, **kwargs)
