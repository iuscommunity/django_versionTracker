from software_versions.models import Software, Status
from software_versions.models import Release, OurVersion
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.unregister(Site)
admin.site.unregister(Group)

class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('label', 'url', 'created', 'modified', 'enabled')
admin.site.register(Software, SoftwareAdmin)

class OurVersionAdmin(admin.ModelAdmin):
    list_display = ('label', 'stable_version', 'release', 'created',
                    'modified')
admin.site.register(OurVersion, OurVersionAdmin)

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('label', 'display_name', 'created', 'modified')
admin.site.register(Release, ReleaseAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('label', 'html_color_code')
admin.site.register(Status, StatusAdmin)

class UserModelAdmin(UserAdmin):
    inlines = [ApiKeyInline]
admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)
