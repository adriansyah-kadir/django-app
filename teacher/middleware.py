from django.http import HttpRequest
from django.urls.base import reverse
from core.models import Class, Teacher


class Middleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, req: HttpRequest):
        # try:
        #     profile = req.user.profile
        #     if profile.role == 'T':
        #         links = [
        #             {
        #                 'url': reverse('class:register'),
        #                 'name': 'add class'
        #             },
        #         ] + [
        #             {
        #                 'url': reverse('class:detail', args=[c.id]),
        #                 'name': c.class_name,
        #             } for c in Class.objects.filter(teacher=req.user.profile.get_role_model())
        #         ]
        #     req.nav += [
        #         {
        #             'name': 'Class',
        #             'links': links
        #         }
        #     ]
        # except Exception as e:
        #     print(e)
        return self.next(req)
