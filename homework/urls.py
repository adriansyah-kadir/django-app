from django.urls import path
from . import handler

app_name = "homework"

urlpatterns = [
    path("", handler.HomeWorkView.as_view(), name="index"),
    path("register/", handler.homework_register, name="register"),
    path("delete/", handler.homework_delete, name="delete"),
    path("done/", handler.homework_done, name="done"),
    path("<homework_id>/result/", handler.HomeWorkResult.as_view(), name="result"),
    path("<homework_id>/result/<int:student_id>/", handler.HomeWorkResult.as_view(), name="student_result"),
    path("<homework_id>/", handler.HomeWorkDetailView.as_view(), name="detail"),
    path("<homework_id>/start/", handler.HomeWorkStart.as_view(), name="start"),
]
