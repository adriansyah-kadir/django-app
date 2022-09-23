from django.urls import reverse
from django.http import HttpRequest


class Middleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, req: HttpRequest):
        nav = self.get_nav_links(req) + self.get_class_links(req)
        try:
            req.nav += nav
        except Exception:
            req.nav = nav

        return self.next(req)

    def get_nav_links(self, req: HttpRequest):
        nav = []
        return nav

    def get_class_links(self, req: HttpRequest):
        try:
            profile = req.user.profile
            links = [
                {"url": reverse("class:register"), "name": "add class"},
            ]
            if profile.role == "teacher":
                links += [
                    {
                        "url": reverse("class:detail", args=[c.id]),
                        "name": c.class_name,
                    }
                    for c in req.user.profile.teacher.class_set.all()
                ]
            elif profile.role == "student":
                links += [{"url": reverse("class:requests"), "name": "requests"}] + [
                    {
                        "url": reverse("class:detail", args=[c.id]),
                        "name": c.class_name,
                    }
                    for c in req.user.profile.student.class_accepted.all()
                ]
            return [{"name": "CLASS", "links": links}]
        except Exception as e:
            print(e)
        return []
