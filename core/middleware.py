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
        nav = [
            {
                "name": "ACCOUNT",
                "links": [
                    {
                        "url": reverse("account:login"),
                        "name": "login",
                        "icon": '<i class="fa-regular fa-right-to-bracket"></i>',
                    },
                    {
                        "url": "/accounts/register/",
                        "name": "register",
                        "icon": '<i class="fa-regular fa-circle-user"></i>',
                    },
                ]
                if req.user.is_authenticated == False
                else [
                    {
                        "url": reverse("account:logout"),
                        "name": "logout",
                        "icon": '<i class="fa-regular fa-right-from-bracket"></i>',
                    }
                ],
            }
        ]
        return nav

    def get_class_links(self, req: HttpRequest):
        try:
            profile = req.user.profile
            links = [
                {
                    'url': reverse('class:register'),
                    'name': 'add class'
                },
            ]
            if profile.role == 'T':
                links += [
                    {
                        'url': reverse('class:detail', args=[c.id]),
                        'name': c.class_name,
                    } for c in req.user.profile.get_role_model().class_set.all()
                ]
            elif profile.role == 'S':
                links += [
                    {
                        'url': reverse('class:detail', args=[c.id]),
                        'name': c.class_name,
                    } for c in req.user.profile.get_role_model().student_class.all()
                ]
            return [{
                'name': 'CLASS',
                'links': links
            }]
        except Exception as e:
            print(e)
        return []
