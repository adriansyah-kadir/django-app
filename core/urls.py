from django.urls import path
from . import handler

app_name = "core"
urlpatterns = [
    path("", handler.index, name="index"),
]
