from django import template
from distutils.version import LooseVersion, StrictVersion
from software_versions.models import Status, OurVersion, Software
from django.conf import settings

register = template.Library()

def getStatues():
    'Get all statues and return a dict'
    status = Status.objects.all()
    return dict([ (i.label, i.html_color_code) for i in status ])

@register.filter()
def get_ourversion(versions, release):
    if versions and release:
        return versions.get(release=release).__dict__.items()
    
@register.filter()
def get_status_color(versions, release):
    ourversion = get_ourversion(versions, release)
    if ourversion:
        status_id = dict(ourversion)['status_id']
        return Status.objects.get(id=status_id).html_color_code

@register.filter()
def get_status_text(versions, release):
    ourversion = get_ourversion(versions, release)
    if ourversion:
        status_id = dict(ourversion)['status_id']
        return Status.objects.get(id=status_id).label