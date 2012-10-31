from tastypie.resources import ModelResource
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authentication import MultiAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL

from django.contrib.auth.models import User
from software_versions.models import Software, Status
from software_versions.models import OurVersion, Release

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_superuser']
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()

class ReleaseResource(ModelResource):
    class Meta:
        queryset = Release.objects.all()
        resource_name = 'release'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
                'label': ALL
        }
        
class StatusResource(ModelResource):
    class Meta:
        queryset = Status.objects.all()
        resource_name = 'status'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
                'label': ALL
        }

class SoftwareResource(ModelResource):
    releases = fields.ManyToManyField(ReleaseResource, 'releases')
    assigned = fields.ForeignKey(UserResource, 'assigned', null=True)
    class Meta:
        queryset = Software.objects.all()
        resource_name = 'software'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        filtering = {
                'label': ALL
        }
        
class OurVersionResource(ModelResource):
    software = fields.ForeignKey(SoftwareResource, 'software')
    release = fields.ForeignKey(ReleaseResource, 'release')
    status = fields.ForeignKey(StatusResource, 'status', null=True)
    class Meta:
        queryset = OurVersion.objects.all()
        resource_name = 'ourversion'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
                'software': ALL,
                'release': ALL,
                'status': ALL
        }
