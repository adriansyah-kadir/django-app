from django import template
from django.conf import settings
import string

register = template.Library()

def get_char(n):
    l = len(string.ascii_uppercase)
    if n > l:
        n -= l
    return string.ascii_uppercase[n]

@register.simple_tag
def call(obj, method, *args, **kwargs):
    return type(obj).__dict__[method](obj, *args, **kwargs)

@register.simple_tag
def char(n):
    return get_char(int(n))

@register.simple_tag
def media(src):
    return str(settings.MEDIA_URL) + src
