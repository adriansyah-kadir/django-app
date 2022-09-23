from django.urls import path
from . import handler

app_name = "question"
urlpatterns = [
    path("register/", handler.question_register, name="register"),
    path("delete/", handler.question_delete, name="delete"),
    path("answer/register/", handler.answer_register, name="answer"),
    path("answer/delete/", handler.answer_delete, name="answer_delete"),
]
