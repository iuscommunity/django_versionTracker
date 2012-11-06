from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from tastypie.api import Api
from software_versions.api import SoftwareResource, StatusResource
from software_versions.api import OurVersionResource, ReleaseResource, UserResource

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(SoftwareResource())
v1_api.register(OurVersionResource())
v1_api.register(ReleaseResource())
v1_api.register(StatusResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
    # home page
    url(r'^$', 'software_versions.views.home', name='home_view'),
    
    # account view
    url(r'^account/$', 'software_versions.views.account', name='account_view'),
    url(r'^account/generate/$', 'software_versions.views.generate_api_key', name='generate_api_key_view'),
    
    # auth views
    url(r'^login/$', 'software_versions.views.mylogin', name='login_view'),
    url(r'^logout/$', 'software_versions.views.mylogout', name='logout_view'),
    
    # list and package views
    url(r'^packages/$', 'software_versions.views.packages',
        name='packages_view'),
    url(r'^packages/(?P<software_id>[\d]+)/$', 'software_versions.views.package',
        name='package_view'),
    url(r'^packages/(?P<software_id>[\d]+)/(?P<release_id>[\d]+)/$', 'software_versions.views.ourversion',
        name='ourversion_view'),
    
    
    # assign functions
    url(r'^packages/(?P<software_id>[\d]+)/assign/$',
        'software_versions.views.assign_software', name='assign_view'),
    url(r'^packages/(?P<software_id>[\d]+)/unassign/$',
        'software_versions.views.unassign_software', name='unassign_view'),
    
    # api views
    url(r'^api/', include(v1_api.urls)),

    # admin
    url(r'^admin/', include(admin.site.urls)),
)
