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
def get_status(software, release):
    status = getStatues()

    # get OurVersion object else see if a pending status
    try:
        ourversion = OurVersion.objects.get(software=software,
                                            release=release)
    except:
        return ('pending', status['pending'])
    
    if not software.version:
        return ('error', status['error'])
    
    # handle stable versions
    if ourversion.stable_version:
        if LooseVersion(software.version) == LooseVersion(ourversion.stable_version):
            return ('current', status['current'])
        elif LooseVersion(software.version) < LooseVersion(ourversion.stable_version):
            return ('newer', status['newer'])

    # handle testing versions
    if not settings.DISABLE_TESTING:
        if ourversion.testing_version:
            if LooseVersion(software.version) == LooseVersion(ourversion.testing_version):
                return ('testing', status['testing'])
            elif LooseVersion(software.version) < LooseVersion(ourversion.testing_version):
                return ('newer', status['newer'])
            
    # handle development versions
    if not settings.DISABLE_DEVELOPMENT:
        if ourversion.development_version:
            if LooseVersion(software.version) == LooseVersion(ourversion.development_version):
                return ('development', status['development'])
            elif LooseVersion(software.version) < LooseVersion(ourversion.development_version):
                return ('newer', status['newer'])
        
    return ('outdated', status['outdated'])

@register.filter() 
def get_status_color(software, release):
    status_tuple = get_status(software, release)
    if status_tuple:
        return status_tuple[1]

@register.filter() 
def get_status_text(software, release):
    status_tuple = get_status(software, release)
    if status_tuple:
        return status_tuple[0]