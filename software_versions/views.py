from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from tastypie.models import ApiKey

from software_versions.models import Software, OurVersion
from software_versions.models import Release
from software_versions.decorators.secure import secure_required

def home(request):
    content = dict(settings=settings)
    releases = Release.objects.all()
    return render(request, 'home.html', content)   

def packages(request):
    # container to hold data passed to templates
    content = dict(settings=settings)
    releases = Release.objects.all()
    content['releases'] = releases
    return render(request, 'packages.html', content)
    
def package(request, software_id):
    # container to hold data passed to templates
    content = dict(settings=settings)
    software = Software.objects.get(id=software_id)
    content['software'] = software
    return render(request, 'package.html', content)

def ourversion(request, software_id, release_id):
    content = dict(settings=settings)
    ourversion = OurVersion.objects.get(software=software_id,
                                        release=release_id)
    content['ourversion'] = ourversion
    return render(request, 'ourversion.html', content)

@login_required   
def assign_software(request, software_id):
    software_obj = Software.objects.get(id=software_id)
    software_obj.assigned = request.user
    software_obj.save()
    return redirect(reverse('package_view', kwargs={'software_id':software_id}))
    
@login_required   
def unassign_software(request, software_id):
    software_obj = Software.objects.get(id=software_id)
    software_obj.assigned = None
    software_obj.save()
    return redirect(reverse('package_view', kwargs={'software_id':software_id}))

@login_required
def account(request):
    content = dict(settings=settings)
    return render(request, 'account.html', content)
    
@login_required
def generate_api_key(request):
    ApiKey.objects.create(user=request.user)
    return redirect(reverse('account_view'))
    
@secure_required
def mylogin(request):
    '''Login a User'''
    content = dict(settings=settings)
    if request.user.is_authenticated():
        return redirect(reverse('home_view'))
    if request.method == 'POST':
        auth_form = AuthenticationForm(None, request.POST or None)
        # check user is valid and active before letting them in
        if auth_form.is_valid():
            login(request, auth_form.get_user())
            return redirect(reverse('home_view'))
    return render(request, 'login.html', content)

@login_required
def mylogout(request):
    '''Logout a User'''
    logout(request)
    return redirect(reverse('home_view'))